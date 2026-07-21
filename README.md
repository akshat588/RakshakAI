# 🛡️ RakshakAI v2

> **AI-Powered Cyber Fraud Detection & Digital Trust Intelligence
> Platform**

RakshakAI v2 is a comprehensive AI-powered cybersecurity platform that
helps users detect, investigate, explain, and report modern cyber
threats through a single unified investigation engine.

------------------------------------------------------------------------

# 🚀 Highlights

-   Universal Investigation Engine
-   AI Investigation Agent (RAG)
-   Threat Intelligence Platform
-   Email, URL, SMS, WhatsApp, UPI, QR, Fake Job, Social Engineering,
    Voice & Deepfake Analysis
-   Explainable AI
-   IOC Correlation
-   MITRE ATT&CK Mapping
-   Reputation Engine
-   Threat Intelligence Dashboard
-   Case Management
-   PDF & JSON Reports
-   Android APIs
-   WhatsApp Bot
-   Tailwind CSS + Flask Architecture

------------------------------------------------------------------------

# 🏗️ Architecture

``` text
                 User
                   │
                   ▼
        Universal Investigation UI
                   │
                   ▼
             Flask Backend APIs
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
 Universal Engine      AI Investigation Agent
        │                     │
        └──────────┬──────────┘
                   ▼
        Multi-Analyzer Execution Engine
                   │
 ┌──────────────────────────────────────────────┐
 │ Email │ URL │ SMS │ WhatsApp │ UPI │ QR      │
 │ Fake Job │ Social Engineering │ Voice │ Deepfake │
 └──────────────────────────────────────────────┘
                   │
                   ▼
      Threat Intelligence & Reputation Engine
                   │
                   ▼
    IOC Correlation • MITRE Mapping • Reports
                   │
                   ▼
 Dashboard • Android APIs • WhatsApp Bot
```

------------------------------------------------------------------------

# 📦 Major Features

## Universal Investigation

Analyze any supported cyber threat through one interface.

## Detection Modules

-   Email Phishing
-   URL Phishing
-   SMS Scam
-   WhatsApp Scam
-   UPI Fraud
-   QR Code Threat
-   Fake Job Detection
-   Social Engineering Detection
-   Voice Scam Detection
-   Deepfake Image Detection

## AI Investigation Agent (RAG)

-   Knowledge Retrieval
-   Context-aware Investigation
-   Explainable AI
-   Investigation Reasoning
-   Executive Summaries

## Threat Intelligence

-   IOC Correlation
-   Reputation Checking
-   Threat Campaign Mapping
-   MITRE ATT&CK Mapping
-   Threat Timeline

## Reports

-   PDF
-   JSON
-   Executive Summary
-   Technical Findings
-   Recommendations

------------------------------------------------------------------------

# 🧠 AI Models

  Module               Model
  -------------------- ----------------------------------
  Email                Logistic Regression
  URL                  Linear SVM / Logistic Regression
  SMS                  Multinomial Naive Bayes
  WhatsApp             Logistic Regression
  Fake Job             Logistic Regression
  Social Engineering   Logistic Regression
  QR                   ML + Threat Analysis
  Voice                Speech + ML Pipeline
  Deepfake             CNN

------------------------------------------------------------------------

# 🛠️ Technology Stack

**Backend** - Python - Flask - REST APIs

**Frontend** - Tailwind CSS - Jinja2 - Vanilla JavaScript

**Machine Learning** - Scikit-learn - PyTorch - OpenCV - Pandas -
NumPy - Joblib

------------------------------------------------------------------------

# 📂 Project Structure

``` text
RakshakAI/
├── 01_Dataset_Generation/
├── 02_Data_Preprocessing/
├── 03_AI_Model_Development/
├── 04_Backend_Development/
├── 05_Frontend/
├── 06_Testing/
├── docs/
├── reports/
├── uploads/
├── app.py
└── README.md
```

------------------------------------------------------------------------

# ⚙️ Installation

``` bash
git clone https://github.com/akshat588/RakshakAI.git
cd RakshakAI
python -m venv venv
```

Windows

``` bash
venv\Scripts\activate
```

Linux

``` bash
source venv/bin/activate
```

Install:

``` bash
pip install -r requirements.txt
npm install
npm run build
```

Run:

``` bash
python app.py
```

------------------------------------------------------------------------

# 🧪 Testing

``` bash
python -m unittest discover 06_Testing
```

------------------------------------------------------------------------

# 📸 Screenshots

Add screenshots for:

-   Dashboard
-   Universal Investigation
-   Email Analyzer
-   URL Analyzer
-   QR Analyzer
-   Voice Analyzer
-   Deepfake Analyzer
-   AI Investigation Agent

------------------------------------------------------------------------

# 🗺️ Roadmap

-   Browser Extension
-   Cloud Deployment
-   SIEM Integration
-   SOC Dashboard
-   Threat Feed Automation

------------------------------------------------------------------------

# 📄 License

MIT License.

------------------------------------------------------------------------

::: {align="center"}
### ⭐ If you like this project, consider giving it a Star!

Made with ❤️ for Cybersecurity, AI & Digital Trust.
:::
