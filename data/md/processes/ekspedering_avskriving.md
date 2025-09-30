id: ekspedering_avskriving
name: "Ekspedering av vedtak - RoboGOOP"
description: "Automatisert prosess som håndterer ekspedering av vedtak i eSam/P360 med fallback til manuell behandling"
author: "RPA-team"
updated: "2025-04-29"
version: "1.0"
order: 1
tags: ["goop", "ekspedering", "vedtak", "saksbehandling"]
---

# Ekspedering av vedtak ✉️

Denne prosessen beskriver hvordan RoboGOOP ekspederer vedtak, samt hvilke begrensninger og anbefalinger som gjelder. 

# Saker som avsluttes av robot i eSam etter at vedtaket er ekspedert i P360:
- **Tidsrom for robotens kjøringer:** Roboten kjøres hverdager (mandag–fredag) kl. 18:00 og 03:00. På grunn av nattkjøringer kan noen oppleve at siste kjøring skjer natt til lørdag, og første kjøring starter natt til mandag. Derfor anbefales det å ikke generere vedtak på lørdager og søndager dersom det er usikkerhet, og man trenger kvalitetssikring av en erfaren kollega.  

- **Krav:** Saken skal være i Steg 4 i eSam, og alle åpne oppgaver må være ferdigstilt.  

- **Generelt om prosessen:** Roboten filtrerer saker som ligger i status «klar til å lukkes» og som skal utstedes med «vedtak om godkjenning» (dvs. ikke Turbo- og Råd-saker). Først leser roboten alle disse sakene, deretter åpner den sakene én og én. Den sjekker om det allerede er generert et vedtak av en saksbehandler. Dersom det ikke finnes, klikker den på knappen for å generere vedtaket. Deretter går roboten inn på P360-delen av saken og ekspederer vedtaket som nettopp ble generert. Til slutt sjekker den alle vedlegg for å se om noe må avskrives eller ekspederes i arkivet, og håndterer disse også.  

Ved ekspedering av vedtak sjekker roboten først om det ligger merknader i filen (ikke i hele P360-dokumentet, men kun i filen som inneholder vedtaket «Svar på søknad …»). Vanligvis gjelder dette merknader som er lagt inn av arkivet eller en saksbehandler. Dersom en merknad oppdages, skal roboten vente med å ekspedere vedtaket. Dette er en unntakssituasjon som ofte oppstår dersom saken allerede hadde et vedtak, men ekspedering til Sikker Digital Postkasse feilet. Da opprettes det en serviceticket til arkivet, og arkivet oppretter en sak til Tieto og avventer ekspedering til eSam-portalen.  

Dersom det ikke finnes merknader i vedtaksfilen (som oftest er tilfelle), ekspederer roboten vedtaket. Standardvalg er «Sikker Digital Postkasse» for søkere som har registrert seg med fødselsnummer. For egenregistrerte søkere (uten fødselsnummer) skal roboten velge eSam-portalen fremfor e-post.  

Roboten har et eget køsystem for saker som feiler under ekspedering. Det skjer av og til feil ved sending/levering til Sikker Digital Postkasse, og disse sakene markeres som «feilede saker ved ekspedering» og håndteres senere av roboten på nattkjøringen kl. 03:00. Roboten loggfører disse sakene i en Excel-database for å gjøre feilsøking enklere for superbrukere. I samme Excel-fil markerer roboten om feilede saker er løst. Hvis ikke, noteres de som «ikke løst» slik at superbrukere kan undersøke disse nærmere.  

Det er etablert en egen felleschat på Teams for superbrukere som får sanntidsmeldinger om feilede saker. De mottar også statusrapport etter hver kjøring via Outlook, med antall saker og hva som gjenstår, inkludert skjermdump fra eSam.  

Når alt er ekspedert og avskrevet i P360, returnerer roboten til eSam og avslutter sakene én etter én.  

**GRY (utligningstiltak):** Etter at vedtaket er generert og alt er ekspedert ferdig i P360, settes saken på vent (utligningstiltak).  

---

# Saker som ikke skal røres/ekspederes av robot:
## Turbo- og Råd-saker
Disse må håndteres av saksbehandlere.

  
## Gjenåpnede saker og saker som inneholder flere vedtak
- **Anbefaling:** Saksbehandler håndterer disse manuelt.  
- **Hvorfor:** Robot oppdager ikke nye vedtak hvis et tidligere vedtak finnes i saken og er ekspedert. 
- **Hvordan fungerer det:**  
  - Roboten sjekker om *Forhåndsvis vedtak*-knappen finnes i eSam.  
  - Hvis ja → betyr at vedtak er generert, og saken hoppes over for å unngå dobbeltvedtak.  
- **Best practice:** Gjenåpnede saker er sjeldne → ryddigst med manuell håndtering.  

---

## Saker med oppgaver i eSam
- Oppgaver må settes som **fullført** før en sak kan avsluttes i Steg 4.  
- Roboten rører ikke saker med åpne oppgaver.  
- **Anbefaling:** Saksbehandler fullfører manuelt (robot vurderer ikke innholdet).  

---

## Dokumenter som ikke ekspederes av roboten
- **Dokumenter uten filer i P360** → rapporteres til superbrukere via *RoboGOOP-nødkontakt*.  
- **E-postdokumenter** (f.eks. verifiseringsforespørsler) → ekspederes manuelt.  
- Begrensning: Roboten håndterer kun ekspedering til Digipost og eSam.  

---

## Typiske problemer og løsninger
- **F-nummer endringer**  
  - Problem: Bruker får nytt fødselsnummer → Digipost-feil.  
  - Løsning: Kontakt arkivet.  

- **Status oppdateres ikke**  
  - Problem: Vedtak er sendt, men status endres ikke.  
  - Løsning: Roboten oppdaterer manuelt til "ekspedert" (avklart med arkivet).  

- **Feil ved Sikker post** → ekspeder til eSam.  
- **Feil ved levering til eSam** → kontakt superbruker / arkivet.  

---

## Screenshots
### Ekspederingsflyt
![Ekspederingsflyt](screenshots/ekspedering_flow.png)  
*Eksempel på automatisk ekspederingsprosess*

### Typisk feilrapport
![Ekspederingsfeil](screenshots/ekspedering_error.png)  
*Eksempel på feil ved ekspedering*


## Kontaktinformasjon

**Prosessansvarlig**: 
**Teknisk support**:  
**Superbruker GOOP**: 

> **Tips for saksbehandlere**: 
