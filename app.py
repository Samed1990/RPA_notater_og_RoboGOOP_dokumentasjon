from flask import Flask, render_template, abort, request, jsonify
import os
import yaml
import markdown
from pathlib import Path
import re
from rank_bm25 import BM25Okapi
import unicodedata

# =========================
# Konfig
# =========================
DATA_ROOT = Path("data/md")
CATEGORIES = ["dev", "processes"]

# BM25-innstillinger
MAX_CANDIDATES = 30   # hent så mange kandidater fra BM25
TOP_K = 3             # hvor mange utdrag vi viser tilbake
MIN_BM25 = 2        # terskel: under dette sier vi at vi ikke fant noe relevant

app = Flask(__name__)

def load_markdown_file(filepath):
    """Load markdown file with YAML front matter"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split front matter and content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                front_matter = yaml.safe_load(parts[1])
                markdown_content = parts[2].strip()
            else:
                front_matter = {}
                markdown_content = content
        else:
            front_matter = {}
            markdown_content = content
        
        # Convert markdown to HTML
        html_content = markdown.markdown(markdown_content, extensions=['codehilite', 'fenced_code'])
        
        return {
            'metadata': front_matter,
            'content': html_content,
            'raw_content': markdown_content
        }
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def get_documents_in_category(category):
    """Get all documents in a category (dev or processes)"""
    category_path = Path(f'data/md/{category}')
    documents = []
    
    if category_path.exists():
        for md_file in category_path.glob('*.md'):
            doc = load_markdown_file(md_file)
            if doc:
                doc['filename'] = md_file.stem
                documents.append(doc)
    
    # Sort by name or order in metadata
    documents.sort(key=lambda x: x['metadata'].get('order', 999))
    return documents

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/dev/')
@app.route('/dev/<doc_id>')
def dev_docs(doc_id=None):
    """Technical solutions for developers"""
    documents = get_documents_in_category('dev')
    
    if doc_id:
        # Show specific document
        doc_path = Path(f'data/md/dev/{doc_id}.md')
        if not doc_path.exists():
            abort(404)
        
        current_doc = load_markdown_file(doc_path)
        if not current_doc:
            abort(404)
        current_doc['filename'] = doc_id
    else:
        # Show first document or empty state
        current_doc = documents[0] if documents else None
    
    return render_template('docs.html', 
                         documents=documents, 
                         current_doc=current_doc,
                         category='dev',
                         page_title='Tekniske løsninger - PA Desktop')

@app.route('/processes/')
@app.route('/processes/<doc_id>')
def process_docs(doc_id=None):
    """Automated processes documentation"""
    documents = get_documents_in_category('processes')
    
    if doc_id:
        # Show specific document
        doc_path = Path(f'data/md/processes/{doc_id}.md')
        if not doc_path.exists():
            abort(404)
        
        current_doc = load_markdown_file(doc_path)
        if not current_doc:
            abort(404)
        current_doc['filename'] = doc_id
    else:
        # Show first document or empty state
        current_doc = documents[0] if documents else None
    
    return render_template('docs.html', 
                         documents=documents, 
                         current_doc=current_doc,
                         category='processes',
                         page_title='Automatiserte prosesser')

# =========================
# RAG: Chunking + BM25 (lokalt)
# =========================

HDR_RE = re.compile(r'^(#{2,3})\s+(.*)', re.M)     # H2/H3
TOKEN_RE = re.compile(r"\w+", re.UNICODE)

def _normalize_text(s: str) -> str:
    if not s:
        return ""
    # NFC → NFKC normalisering + standardiser bindestreker/whitespace
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("–", "-").replace("—", "-").replace("-", "-")  # ulike dash-varianter
    s = s.replace("_", " ").replace("/", " ").replace("\\", " ")
    return s

def _tokenize(s: str):
    s = _normalize_text(s)
    return [t.lower() for t in TOKEN_RE.findall(s or "")]

def split_markdown_sections(text: str, max_chars: int = 1600):
    """
    Del opp pr H2/H3. Fallback til lengde-chunking om ingen headere.
    Returnerer liste av (section_title, chunk_text)
    """
    if not text:
        return []
    headers = list(HDR_RE.finditer(text))
    if not headers:
        chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
        return [("Chunk " + str(i), c) for i, c in enumerate(chunks)]
    sections = []
    for i, m in enumerate(headers):
        start = m.end()
        end = headers[i+1].start() if i+1 < len(headers) else len(text)
        title = m.group(2).strip() or f"Seksjon {i}"
        body = text[start:end].strip()
        if not body:
            continue
        # Splitt svært lange seksjoner i “del 1/2/3…”
        if len(body) > max_chars:
            subchunks = [body[j:j+max_chars] for j in range(0, len(body), max_chars)]
            for k, sc in enumerate(subchunks):
                sections.append((f"{title} (del {k+1})", sc))
        else:
            sections.append((title, body))
    return sections

def build_corpus():
    """
    Bygg dokumenter:
    - text: kun brødtekst (for visning)
    - index_text: filnavn(stem) + seksjon + ev. metadata-tittel + brødtekst (for søk)
    """
    docs = []
    for cat in CATEGORIES:
        cat_dir = DATA_ROOT / cat
        if not cat_dir.exists():
            continue
        for p in cat_dir.glob("*.md"):
            raw = load_markdown_file(p)
            if not raw:
                continue
            meta_title = (raw.get("metadata") or {}).get("title", "") or ""
            stem_words = p.stem.replace("_", " ").replace("-", " ")

            for i, (sec, body) in enumerate(split_markdown_sections(raw["raw_content"])):
                index_text = f"{stem_words}\n{sec}\n{meta_title}\n{body}"
                docs.append({
                    "id": f"{p.name}#sec{i}",
                    "file": p.name,
                    "section": sec,
                    "text": body,
                    "index_text": index_text,
                    "category": cat
                })
    return docs



class BM25Store:
    def __init__(self, docs, tokens):
        self.docs = docs
        self.tokens = tokens
        self.bm25 = BM25Okapi(tokens)

    def search(self, query, top_n=30):
        q_tokens = _tokenize(query)
        scores = self.bm25.get_scores(q_tokens)
        idx_sorted = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
        return [(self.docs[i], float(scores[i])) for i in idx_sorted]

# Bygg global indeks ved oppstart
DOCS = build_corpus()
TOKENS = [_tokenize(d.get("index_text") or d["text"]) for d in DOCS]
BM25 = BM25Store(DOCS, TOKENS)

def _format_sources(picked):
    return [
        {"file": c["file"], "section": c["section"], "bm25": float(bm25)}
        for (c, bm25) in picked
    ]

def _make_answer_from_chunks(picked, k=TOP_K):
    """
    Lag et enkelt, trygt svar: pen kilde-linje + markdown-innhold.
    """
    parts = []
    for doc, _score in picked[:k]:
        snippet = doc["text"].strip()
        src = f'Kilde: `{doc["file"]}` — _{doc["section"]}_'
        # vi lar kun markdown-innholdet rendres som markdown i UI-en
        parts.append(f"{src}\n\n{snippet}")
    return "Basert på dokumentasjonen:\n\n" + "\n\n---\n\n".join(parts)

def handle_smalltalk(q: str) -> str | None:
    """Returner standardsvar for enkel småprat; ellers None."""
    ql = (q or "").strip().lower()

    # hilsener
    if ql in {"hei", "hei!", "hallo", "hallå", "heisann"} or "hvordan går det" in ql:
        return (
            "**Hei!** Hyggelig å se deg 🙂\n\n"
            "Jeg er *Dokumentasjonsbot* og kan hjelpe deg å finne info i dokumentasjonen. "
            "Bruk gjerne **stikkord** som *Asta*, *historikksjekk*, *ekspedering av vedtak*, "
            "*Power Automate/Cloud/Desktop* for best treff."
        )

    # hvem er du?
    if "hva heter du" in ql or "hvem er du" in ql or "hva er du" in ql:
        return (
            "Jeg heter **Dokumentasjonsbot** 🤖, laget av **Samad Ismayilov**. "
            "Jeg svarer kun basert på innholdet i nettstedets `.md`-filer. "
            "Hvis noe ikke finnes i dokumentasjonen, sier jeg fra."
        )

    # hjelp
    if ql in {"hjelp", "help", "hvordan bruker jeg deg", "hva kan du"} or "hjelpe" in ql:
        return (
            "**Slik bruker du meg:**\n"
            "- Skriv korte **stikkord** (f.eks. *Asta*, *historikksjekk*, *Power Automate Desktop*).\n"
            "- Jeg henter relevante utdrag fra dokumentasjonen og viser kilder.\n"
            "- Jeg kan ikke finne ting som ikke står i dokumentene.\n\n"
            "_Nettsiden er under utvikling. Kontakt **Samad Ismayilov** ved spørsmål._"
        )

    return None



@app.post("/ask")
def ask():
    body = request.get_json(silent=True) or {}
    q = (body.get("question") or "").strip()
    if not q:
        return jsonify({"error": "Tomt spørsmål"}), 400

    if not DOCS:
        return jsonify({"answer": "Ingen dokumenter funnet.", "sources": []})
    
        # 0) Småprat / standard-svar
    small = handle_smalltalk(q)
    if small:
        return jsonify({"answer": small, "sources": []})


    # 1) BM25-kandidater
    candidates = BM25.search(q, top_n=MAX_CANDIDATES)

    # 1b) Forbedret fallback hvis query er kort / lav BM25-score
    if (not candidates) or (candidates[0][1] < MIN_BM25):
        q_norm = _normalize_text(q).lower()
        q_tokens = [t for t in _tokenize(q_norm) if len(t) >= 3]
        soft = []
        if q_tokens:
            for d in DOCS:
                name = _normalize_text(d["file"]).lower()
                sec  = _normalize_text(d["section"]).lower()
                # match hvis minst ett token finnes i filnavn eller seksjonstittel
                hits = sum(1 for t in q_tokens if (t in name or t in sec))
                if hits > 0:
                    # liten bonus hvis både "power" og "automate" finnes
                    bonus = 0.5 if ("power" in (name+sec) and "automate" in (name+sec)) else 0.0
                    soft.append((d, 2.2 + 0.3 * hits + bonus))  # kunstig score > MIN_BM25
        if soft:
            # sortér “soft”-kandidater høyest og ta med gode BM25-treff
            soft_sorted = sorted(soft, key=lambda x: x[1], reverse=True)
            candidates = soft_sorted + [c for c in candidates if c[1] >= MIN_BM25]

    if not candidates or candidates[0][1] < MIN_BM25:
        return jsonify({
            "answer": "Jeg finner ikke dette i dokumentasjonen vår.",
            "sources": []
        })

    # 2) Lag et sikkert svar av de beste chunkene
    answer = _make_answer_from_chunks(candidates, k=TOP_K)
    sources = _format_sources(candidates[:TOP_K])
    return jsonify({"answer": answer, "sources": sources})


if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('data/md/dev', exist_ok=True)
    os.makedirs('data/md/processes', exist_ok=True)
    
    app.run(debug=True)
