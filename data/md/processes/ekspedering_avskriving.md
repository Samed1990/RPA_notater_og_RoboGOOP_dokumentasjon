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

---

## Gjenåpnede saker og flere vedtak
- **Anbefaling:** Saksbehandler håndterer disse manuelt.  
- **Hvorfor:** Robot oppdager ikke nye vedtak hvis et tidligere vedtak finnes i saken.  
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
