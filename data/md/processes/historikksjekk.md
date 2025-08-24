id: historikksjekk
name: "Historikksjekk - RoboGOOP"
description: "Automatisert prosess som validerer søkere mot historiske systemer (eSam, P360, ASTA)"
author: "RPA-team"
updated: "2025-04-29"
version: "1.0"
order: 2
tags: ["goop", "historikk", "validering", "kvalitetssikring"]
---

# Historikksjekk 🔎

Denne prosessen beskriver hvordan RoboGOOP utfører historikksjekk og hvilke forbedringer som er gjort basert på erfaringer.

---

## Systemer som sjekkes
- Historisk **eSam**, **P360**, **ASTA**  
- Ikke aktive eSam/P360 (unngår risiko for ferske saker)  
- Beslutning: Ingen søk i aktive systemer foreløpig.  

---

## Treffsikkerhet og forbedringer
- **95%+ treffsikkerhet** etter forbedringer.  
- Utfordring: Like fornavn/fødselsdato.  
- Forbedring: Ekstra kontroll på etternavn.  

---

## Bedre identifikasjon i historisk eSam
- Robot kopierer **etternavn + fornavn + fødselsdato**.  
- Fordel: Saksbehandler kan lettere validere treff.  
- Viktig: Hvis mismatch på etternavn → slett denne delen av notatet.  

---

## Viktig å være obs på
- Når roboten skriver et langt notat i eSam, betyr det som regel at data er funnet.  
- Risiko: ca. 5 % falske treff (samme navn + fødselsdato).  
- Tiltak: Dobbeltsjekk alltid navn og fødselsdato.  

---

## Eksempler på feil
### Ufullstendig notat
- Årsak: Robot startet å skrive før eSam-vinduet var ferdig lastet.  
- Tiltak: Hastigheten justert slik at roboten venter før skriving.  

![Ufullstendig robotnotat](/static/Screenshot_notat_1.jpg)  
*Eksempel på ufullstendig robotnotat i eSam*

### ASTA-søk feilet
- Av og til ser man en tomt notat fra ASTA, det betyr at robot ikke har klart å gjennomføre søk. 
- Årsak: Cache-minne i nettleser der ASTA kjører, og ASTA har git bare en hvit skjerm.   
- Tiltak (oppdatert 14.05.25): Robot tømmer cache hver gang ASTA åpnes og på denne måten klarer å søke på nytt etter at den har sikret at ASTA er responsiv. 
Hvis ikke ASTA gir noen respons etter flere forsøk, skal robot avslutte prosessen og ikke generere feilaktige resultater. 
for mer info sjekk dette innlegget på Teams:
<https://teams.microsoft.com/l/message/19:VCbcDGlFfZ_E9YUS6kcEM2eI4qjF3tqUAUHXkN5vvvg1@thread.tacv2/1747399619875?tenantId=1ec46890-73f8-4a2a-9b2c-9a6611f1c922&groupId=e41e056f-01d5-41d4-a3bc-fb2a6d2b5432&parentMessageId=1747399619875&teamName=AVD%20Utenlandsk%20utdanning&channelName=General&createdTime=1747399619875> 

![ASTA feilnotat](/static/Screenshot_notat_2.jpg)  
*Eksempel på mangelfullt notat fra ASTA-søk*
