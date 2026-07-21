# RakshakAI v2 Deployment Guide

## System Requirements

### Operating System

- Windows 11
- Ubuntu 22.04+
- Kali Linux
- Debian 12+

### Python

- Python 3.11+

### Database

- SQLite (Development)
- PostgreSQL (Production)

---

# Installation

## Clone Repository

```bash
git clone <repository_url>
cd RakshakAI
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux

```bash
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Environment

Create a `.env` file.

Example:

```env
SECRET_KEY=change_me
FLASK_ENV=production

DATABASE_URL=

VIRUSTOTAL_API_KEY=
ABUSEIPDB_API_KEY=
PHISHTANK_API_KEY=
OPENPHISH_API_KEY=

WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_VERIFY_TOKEN=

OPENAI_API_KEY=
```

---

# Run Database Migrations

```bash
flask db upgrade
```

---

# Build Frontend Assets

```bash
npm install
npm run build
```

---

# Start Application

Development

```bash
python app.py
```

Production (Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

# Reverse Proxy (Nginx)

Configure Nginx to forward requests to the Flask application.

Enable HTTPS using TLS certificates.

---

# Production Checklist

- DEBUG=False
- Strong SECRET_KEY
- HTTPS Enabled
- Security Headers Enabled
- Environment Variables Configured
- API Keys Configured
- Logging Enabled
- Backup Strategy Configured
- Monitoring Enabled

---

# Health Check

```
GET /health
```

Expected Response

```json
{
  "status": "healthy"
}
```

---

# Logs

Application logs are stored in:

```
logs/
```

---

# Backup

Back up:

- Database
- Reports
- Uploaded Files
- Threat Intelligence Cache
- User Data