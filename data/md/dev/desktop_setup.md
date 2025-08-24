id: desktop_setup
name: "PA Desktop Oppsett og Installasjon"
description: "Komplett guide for installasjon og konfigurering av Power Automate Desktop"
author: "RPA Team"
updated: "2024-01-15"
version: "2.1"
order: 1
tags: ["installasjon", "oppsett", "konfigurasjon"]
---

# PA Desktop Oppsett og Installasjon

## Oversikt
Power Automate Desktop er Microsoft sin løsning for desktop-automatisering som lar deg automatisere repetitive oppgaver på Windows-maskiner.

## Systemkrav

### Minimum krav:
- **Operativsystem**: Windows 10 (versjon 1909 eller senere) / Windows 11
- **RAM**: 4 GB (8 GB anbefalt)
- **Lagringsplass**: 3 GB ledig diskplass
- **Prosessor**: Dual-core prosessor
- **.NET Framework**: 4.7.2 eller senere

### Nettverkskrav:
- Internettforbindelse for aktivering og oppdateringer
- Tilgang til Microsoft 365 eller Power Platform

## Installasjon

### Last ned Power Automate Desktop (Be om IT-avdlingen å gjøre den tilgjengelig i Firmaportalen)
1. Gå til [Microsoft Power Automate](https://powerautomate.microsoft.com/)
2. Klikk på "Try free" eller "Get started"
3. Logg inn med din organisasjonskonto
4. Last ned Power Automate Desktop installer


### Trinn 3: Første gangs oppsett
1. Start Power Automate Desktop
2. Logg inn med organisasjonskontoen din
3. Velg riktig miljø (Production/Test)- dette deles av IT eller Microsoft admin.
4. Aksepter tillatelser og betingelser

## Beste praksis

### Ytelse
- Optimaliser selektorer for UI-elementer
- Bruk delays forsiktig
- Test flows grundig før produksjonssetting

### Vedlikehold
- Hold Power Automate Desktop oppdatert
- Regelmessig backup av flows
- Dokumenter alle endringer


> **HK-dir reltaterte tips & tricks**: det er noen enkle tips som er viktig for automatiseringen 

## Teknologivalg – Power Automate
Vi benytter **Power Automate Desktop (PAD)** og **Power Automate Cloud** i våre prosesser.

- **Power Automate Desktop (PAD):**  
  Brukes hovedsakelig til **GUI-automatisering**, der roboten simulerer brukerhandlinger som tastetrykk, museklikk og skjermlesing.

- **Power Automate Cloud:**  
  Fungerer som en **orchestrator**. Her setter vi opp **schedules**, lager **HTTP-requests** slik at flyter kan trigges fra en app, og vi kan dele tilganger med superbrukere.  
  Bruken av Cloud gjør jobben enklere og reduserer lisenskostnader.

---

## Lisensmodeller
Det finnes to hovedtyper lisenser i Power Automate:

- **Attended license** – Robot kjører når en bruker er logget inn.  
  Vi har valgt denne lisensen som utgangspunkt fordi:
  - Gir bedre kontroll og sporbarhet  
  - Enklere feilsøking  
  - Anbefalt i utviklings- og testfaser  
  - Kan også brukes autonomt som *unattended*, men krever enkelte ekstra tiltak  

- **Unattended license** – Robot kan kjøre helt uavhengig av brukerøkter.  
  Dette blir aktuelt for oss når prosessene er modne og vi flytter kjøringer til virtuelle maskiner.

📌 Les mer om pris og lisenser her: [Power Automate Pricing](https://powerautomate.microsoft.com/pricing/)

---

## Infrastruktur og sikkerhet
- Vi kjører foreløpig på **fysiske maskiner** i lukkede rom uten ekstern fysisk adgang.  
- Minimum sikkerhetstiltak i henhold til **ISO** og **NSM** er ivaretatt.  
- For attended-kjøringer anbefaler vi å legge til ekstra sikkerhet, f.eks.:
  - Egen safe for laptop  
  - Maskiner med lukket lokk under kjøring  

Når vi går over til **unattended**, vil robotene kjøre på virtuelle maskiner med alle brukersesjoner logget av.  

Dette gir bedre skalerbarhet, men i test og feilsøkingsfase er attended mer fleksibelt.

---

## VPN-relaterte problemer
Et kjent hinder for automatisering er at enkelte systemer krever VPN-tilkobling. VPN kan være ustabilt og føre til at prosessene stopper.  

**Løsning:**  
Vi har laget egne **PowerShell-skript** som håndterer dette problemet.  
📌 Ta kontakt med RPA-teamet for detaljer om implementasjonen.

---

## Krav for kjøring på andre maskiner
- Last ned **Power Automate Machine Runtime** dersom prosessen skal kjøre på en annen maskin enn din egen.  
- Sørg for å gi nødvendige **tilganger og tillatelser**.

---

## Browser-automatisering
- Installer **Power Automate sine plugins** i de nettleserne du skal automatisere (Edge, Chrome, Firefox).  
- Vi anbefaler **Edge** for best ytelse og enklest oppsett.  
- Dersom prosessen håndterer mange faner, kan det være smart å fordele automatiseringen på Edge + Chrome/Firefox.

---

## Tips ved P360-automatisering
Når vi automatiserer opp mot **P360**, er følgende anbefalt:

1. Start prosessen med **Launch Browser (Maximized)**.  
2. Sett **zoom til 67 % eller 50 %**.  
   Dette gjør det lettere for roboten å håndtere lange lenker og klikkområder uten feil.  

![Eksempel P360 automation](screenshots/p360_example.png)

---

## Oppsummering
- Start med **attended** lisens for fleksibilitet og enkel feilsøking  
- Bygg robusthet mot **VPN-problemer** med PowerShell  
- Bruk **Edge med plugins** for best effekt  
- Optimaliser GUI-automatisering i P360 ved å justere vindu og zoom  

Disse retningslinjene gjør at vi kan utvikle prosesser raskt, sikkert og med høy stabilitet.



## Nyttige lenker
- [Offisiell dokumentasjon](https://docs.microsoft.com/en-us/power-automate/desktop-flows/)
- [Community forum](https://powerusers.microsoft.com/t5/Power-Automate-Desktop/bd-p/PADesktop)
- [Video tutorials](https://aka.ms/PADesktopVideos)

> **Tips**: Bruk alltid test-miljøet for utvikling og testing før deploy til produksjon.