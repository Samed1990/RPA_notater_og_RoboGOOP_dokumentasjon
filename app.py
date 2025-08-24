from flask import Flask, render_template, abort
import os
import yaml
import markdown
from pathlib import Path

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

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('data/md/dev', exist_ok=True)
    os.makedirs('data/md/processes', exist_ok=True)
    
    app.run(debug=True)