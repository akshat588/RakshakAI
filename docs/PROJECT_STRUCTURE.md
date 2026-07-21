# RakshakAI v2 Project Structure

```
RakshakAI/
│
├── 01_Dataset_Generation/
│   ├── email/
│   ├── url/
│   ├── sms/
│   ├── whatsapp/
│   ├── upi/
│   ├── qr/
│   ├── fake_job/
│   ├── social_engineering/
│   └── voice/
│
├── 02_Data_Preprocessing/
│
├── 03_AI_Model_Development/
│   ├── common/
│   ├── email/
│   ├── url/
│   ├── sms/
│   ├── whatsapp/
│   ├── upi/
│   ├── qr/
│   ├── fake_job/
│   ├── social_engineering/
│   ├── voice_scam/
│   └── ai_agent/
│
├── 04_Backend_Development/
│   ├── blueprints/
│   ├── services/
│   ├── models/
│   ├── middleware/
│   ├── config/
│   ├── utils/
│   └── database/
│
├── 05_Frontend/
│   ├── templates/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── icons/
│   └── assets/
│
├── 06_Testing/
│
├── docs/
│
├── logs/
│
├── reports/
│
├── uploads/
│
├── requirements.txt
├── package.json
├── app.py
├── config.py
└── README.md
```

---

## Major Modules

### AI & Analysis

- Universal Investigation Engine
- Multi-Analyzer Execution Engine
- AI Investigation Agent (RAG)
- Threat Intelligence Engine
- Reputation Engine
- Report Generator

### Detection Modules

- Email Analyzer
- URL Analyzer
- SMS Analyzer
- WhatsApp Analyzer
- UPI Analyzer
- QR Analyzer
- Fake Job Analyzer
- Social Engineering Analyzer
- Voice Scam Analyzer

### Platform Components

- Dashboard
- Case Management
- User Management
- Android APIs
- WhatsApp Bot
- Notification Services

---

## Documentation

The `docs/` directory contains:

- API Documentation
- Deployment Guide
- Architecture Documentation
- User Manual
- Project Structure