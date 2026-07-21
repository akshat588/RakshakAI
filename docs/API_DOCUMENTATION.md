# RakshakAI v2 API Documentation

## Base URL

```
http://<server>/api
```

---

# Authentication

Authentication endpoints

```
POST /auth/login
POST /auth/logout
POST /auth/refresh
GET  /profile
```

---

# Universal Investigation

```
POST /investigate
```

Supported Inputs

- Email
- URL
- SMS
- WhatsApp
- UPI
- QR
- Fake Job
- Social Engineering
- Voice

---

# AI Analyzers

```
POST /email
POST /url
POST /sms
POST /whatsapp
POST /upi
POST /qr
POST /fake-job
POST /social-engineering
POST /voice
```

---

# AI Investigation Agent

```
POST /agent/query
POST /agent/knowledge
GET  /agent/health
```

---

# Threat Intelligence

```
GET /dashboard
GET /statistics
GET /history
GET /campaigns
GET /reputation
```

---

# Reports

```
POST /report/generate
GET  /report/<case_id>
```

Supported formats

- PDF
- JSON

---

# Mobile APIs

```
POST /mobile/auth/login
POST /mobile/auth/logout

GET  /mobile/dashboard

POST /mobile/investigation/start

POST /mobile/report/generate

GET  /mobile/notifications
```

---

# Response Format

```json
{
    "success": true,
    "result": {}
}
```

---

# Status Codes

- 200 OK
- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 413 Payload Too Large
- 500 Internal Server Error