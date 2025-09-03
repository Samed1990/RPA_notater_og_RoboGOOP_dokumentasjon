id: error_handling
name: "Feilhåndtering og Debugging"
description: "Beste praksis for feilhåndtering og debugging av RPA-flows"
author: "RPA Team"
updated: "2024-01-20"
version: "1.3"
order: 2
tags: ["feilhåndtering", "debugging", "logging", "best-practice"]
---

# Feilhåndtering og Debugging

## Oversikt
Robust feilhåndtering er kritisk for stabile RPA-prosesser. Denne guiden dekker beste praksis for å håndtere feil og debugge flows effektivt.

## Try-Catch Blokker

### Grunnleggende struktur
```power-automate
Try
    # Hovedlogikk her
    Get details of a UI element in window ...
    Click UI element ...
Catch
    # Feilhåndtering
    Log message "Feil oppstod: %LastError%"
    Take screenshot
    Send email notification
End Try
```

### Forskjellige feiltyper

#### UI-element ikke funnet
```power-automate
Try
    Wait for UI element in window 'Application' timeout 10
    Click UI element %UIElement%
Catch TimeoutException
    Log message "UI-element ikke funnet innen timeout"
    Take screenshot path: "C:\Logs\ui_error_%datetime%.png"
    # Alternatív handling eller avbryt
End Try
```

#### Fil-operasjoner
```power-automate
Try
    Copy file from "%SourcePath%" to "%DestinationPath%"
Catch FileNotFoundException
    Create folder "%DestinationFolder%"
    Retry copy operation
Catch UnauthorizedAccessException
    Log error "Ikke tilgang til fil: %SourcePath%"
    Send notification to admin
End Try
```

## Logging Strategi

### Strukturert logging
```power-automate
# Standard log entry
Set variable %LogMessage% to "Flow: %FlowName% | Step: %CurrentStep% | Status: %Status% | Time: %CurrentDateTime%"
Write text %LogMessage% to file "C:\Logs\rpa_log_%date%.txt"
```

### Log-nivåer
- **INFO**: Normal prosessflyt
- **WARNING**: Potensielle problemer
- **ERROR**: Kritiske feil
- **DEBUG**: Detaljert informasjon for utvikling

```power-automate
# Log function
Run subflow 'LogMessage'
    Input: Level="INFO", Message="Prosess startet", Module=%FlowName%
```

## Resilient Design Patterns

### Retry-mønster
```power-automate
Set variable %RetryCount% to 0
Set variable %MaxRetries% to 3
Set variable %Success% to False

Loop while %Success% = False AND %RetryCount% < %MaxRetries%
    Try
        # Kritisk operasjon her
        Get web data from URL %TargetURL%
        Set variable %Success% to True
    Catch
        Increase variable %RetryCount% by 1
        Wait 5 seconds
        Log warning "Retry attempt %RetryCount% of %MaxRetries%"
    End Try
End Loop

If %Success% = False
    # Eskalering - send alarm
    Send email to admin about failure
End If
```

### Circuit Breaker
```power-automate
# For å unngå cascade failures
If %ConsecutiveFailures% > 5
    Log error "Circuit breaker aktivert - stopper prosess"
    Wait 300 seconds
    Reset %ConsecutiveFailures% to 0
End If
```

## Debugging Teknikker

### Breakpoints og Step-through
1. **Bruk breakpoints** i Power Automate Desktop
2. **Variabel-inspeksjon** under kjøring
3. **Step-by-step kjøring** for komplekse flows

### Screenshot logging
```power-automate
# Ta screenshot ved kritiske punkter
Take screenshot path: "C:\Debug\step_%StepNumber%_%datetime%.png"
```

### Variabel dumping
```power-automate
# Log alle viktige variabler
Set variable %DebugInfo% to "User: %Username% | File: %CurrentFile% | Status: %ProcessStatus%"
Log message %DebugInfo%
```

## Overvåkning og Alerting

### E-post notifikasjoner
```power-automate
# Ved kritiske feil
Send email
    From: "placeholder"
    To: "placeholder"
    Subject: "RPA Feil: %FlowName%"
    Body: "
    Flow: %FlowName%
    Feil: %LastError%
    Tidspunkt: %CurrentDateTime%
    Maskin: %ComputerName%
    "
```

### Integration med monitoring systemer
- **Application Insights**: For Microsoft-miljøer
- **Slack/Teams**: For team-notifikasjoner
- **SIEM**: For sikkerhetshendelser

## Vanlige Feilscenarioer

### 1. Nettverksfeil
```power-automate
Try
    # Web request
Catch NetworkException
    Wait 30 seconds
    Try again with exponential backoff
    If still failing after 3 attempts
        Switch to offline mode or alternative process
End Try
```

### 2. Applikasjon ikke tilgjengelig
```power-automate
Try
    Launch application %AppPath%
    Wait for window %WindowTitle% timeout 30
Catch
    Log error "Applikasjon ikke tilgjengelig"
    Try alternative launcher or restart service
    Send notification to IT support
End Try
```

### 3. Data validering feil
```power-automate
# Valider input data
If %InputData% matches regex "^[0-9]{6}$"
    # Process data
Else
    Log warning "Invalid data format: %InputData%"
    Move file to quarantine folder
    Send validation error report
End If
```

## Performance Monitoring

### Tidsregistrering
```power-automate
Set variable %StartTime% to %CurrentDateTime%
# Hovedprosess her
Set variable %EndTime% to %CurrentDateTime%
Set variable %Duration% to %EndTime% - %StartTime%

Log message "Prosess fullført på %Duration% sekunder"

# Alert hvis prosess tar for lang tid
If %Duration% > 300  # 5 minutter
    Send performance alert
End If
```

### Ressursovervåkning
- CPU-bruk
- Minnebruk  
- Disk I/O
- Nettverkstrafikk

## Best Practices

### 1. Fail Fast Principle
- Valider input tidlig
- Sjekk forutsetninger før kjøring
- Ikke fortsett med korrupte data

### 2. Graceful Degradation
- Ha fallback-mekanismer
- Fortsett med redusert funksjonalitet hvis mulig
- Kommuniser status til brukere

### 3. Observability
- Detaljert logging på kritiske steder
- Metrics og performance counters
- Distributed tracing for komplekse flows

### 4. Testing
- Unit tests for subflows
- Integration tests med mock data
- Chaos engineering for resilience testing

> **Viktig**: Husk at god feilhåndtering handler ikke bare om å fange feil, men også om å gi meningsfulle feilmeldinger og recovery-strategier.
