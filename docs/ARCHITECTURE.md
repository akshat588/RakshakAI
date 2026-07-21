# RakshakAI v2 Architecture Documentation

## High-Level Architecture

```
                    User
                      │
                      ▼
             Frontend (Tailwind)
                      │
                      ▼
              Flask Application
                      │
     ┌────────────────┼────────────────┐
     ▼                ▼                ▼
 Universal      AI Investigation   User Management
 Investigation      Agent
 Engine             (RAG)
     │                │
     └──────────┬─────┘
                ▼
        Multi Analyzer Engine
                │
 ┌──────────────┼────────────────────────────┐
 ▼              ▼            ▼               ▼
Email        URL         SMS/WhatsApp      Voice
Analyzer     Analyzer     Analyzers       Analyzer
 │              │            │               │
 └──────────────┴────────────┴───────────────┘
                │
                ▼
      Threat Intelligence Layer
                │
 ┌──────────────┼───────────────────────────┐
 ▼              ▼            ▼              ▼
Reputation   IOC Engine   Campaigns   Timeline
                │
                ▼
         Report Generation
                │
                ▼
      PDF / JSON / Export APIs
                │
                ▼
 Dashboard / Android APIs / WhatsApp Bot
```

---

## Core Components

- Universal Investigation Engine
- Multi-Analyzer Execution Engine
- Threat Intelligence Platform
- AI Investigation Agent (RAG)
- Report Generator
- Dashboard Services
- Case Management
- User Management
- WhatsApp Bot
- Android APIs

---

## AI Models

- Email Scam Detection
- URL Phishing Detection
- SMS Scam Detection
- WhatsApp Scam Detection
- UPI Fraud Detection
- Fake Job Detection
- Social Engineering Detection
- QR Threat Detection
- Voice Scam Detection

---

## External Threat Intelligence

- VirusTotal
- AbuseIPDB
- URLhaus
- PhishTank
- OpenPhish

---

## Reporting

- PDF Reports
- JSON Reports
- Evidence Builder
- Case Builder

---

## Security

- Authentication
- Role-Based Access Control
- Audit Logs
- API Keys
- Security Headers
- Production Configuration
- Performance Monitoring