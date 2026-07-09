<div align="center">

# 🛡️ RakshakAI

### AI Powered Cyber Threat Intelligence Platform

Detect • Analyze • Protect

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikitlearn)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)
![License](https://img.shields.io/badge/License-MIT-success)

An AI-powered cybersecurity platform that detects phishing attacks, malicious URLs, QR code scams, fake jobs, social engineering attacks, UPI fraud, SMS scams, WhatsApp scams and deepfake images using Machine Learning and Deep Learning.

</div>

---

# 📖 Overview

RakshakAI is a comprehensive AI-based cyber threat intelligence platform designed to identify and analyze modern cyber threats before users become victims.

Instead of focusing on only one attack vector, RakshakAI combines multiple AI-powered security engines into a single platform, providing a unified dashboard for cyber threat analysis.

The platform leverages Machine Learning, Natural Language Processing (NLP), Computer Vision, Explainable AI, and Threat Intelligence techniques to detect suspicious digital content.

---

# ✨ Features

✅ Email Phishing Detection

✅ URL Phishing Detection

✅ SMS Scam Detection

✅ WhatsApp Scam Detection

✅ Fake Job Detection

✅ Social Engineering Detection

✅ UPI Fraud Detection

✅ QR Code Threat Detection

✅ Deepfake Image Detection

✅ Explainable AI Results

✅ Threat Risk Scoring

✅ Live Dashboard

✅ Scan History

---

# 🏗️ System Architecture

```text
                    USER
                      │
                      ▼
              Web Dashboard
      (HTML + Tailwind + JavaScript)
                      │
                      ▼
                Flask Routes
                      │
                      ▼
             Analyzer APIs
───────────────────────────────────────
 Email Analyzer
 URL Analyzer
 SMS Analyzer
 WhatsApp Analyzer
 Fake Job Analyzer
 Social Engineering Analyzer
 UPI Analyzer
 QR Analyzer
 Deepfake Analyzer
───────────────────────────────────────
                      │
                      ▼
                AI Models
───────────────────────────────────────
 Logistic Regression
 Linear SVM
 Naive Bayes
 CNN (Deepfake Detection)
───────────────────────────────────────
                      │
                      ▼
               Threat Engine
───────────────────────────────────────
 Risk Score
 Confidence
 Severity
 Threat Explanation
 Recommendations
───────────────────────────────────────
                      │
                      ▼
              Scan History
                      │
                      ▼
            Dashboard Results
```

---

# 🧠 AI Models Used

| Module | Algorithm |
|---------|-----------|
| Email Detection | Logistic Regression |
| URL Detection | Linear SVM / Logistic Regression |
| SMS Detection | Multinomial Naive Bayes |
| WhatsApp Detection | Logistic Regression |
| Fake Job Detection | Logistic Regression |
| Social Engineering Detection | Logistic Regression |
| UPI Fraud Detection | Rule-Based + Machine Learning |
| QR Detection | URL Detection + Threat Analysis |
| Deepfake Detection | Convolutional Neural Network (CNN) |

---

# ⚙️ Machine Learning Pipeline

```text
Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Text Preprocessing
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Train/Test Split
      │
      ▼
Model Training
      │
      ▼
Evaluation
      │
      ▼
Best Model Selection
      │
      ▼
Joblib Serialization
      │
      ▼
Flask Integration
      │
      ▼
Real-Time Prediction
```

---

# 🛠️ Technology Stack

### Backend

- Python
- Flask
- REST APIs
- Jinja2

### Frontend

- HTML5
- Tailwind CSS
- Vanilla JavaScript

### Machine Learning

- Scikit-learn
- Pandas
- NumPy
- Joblib

### Computer Vision

- OpenCV
- CNN

---

# 📂 Project Structure

```
RakshakAI/

│
├── 01_Project_Planning_Research/
├── 02_Dataset_Design_Collection/
├── 03_AI_Model_Development/
├── 04_Backend_Development/
├── 05_Frontend_Development/
│
├── Assets/
│
├── docs/
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/akshat588/RakshakAI.git
```

Go inside the project

```bash
cd RakshakAI
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Flask

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

# 📊 Threat Analysis Workflow

```text
User Input

↓

Flask Route

↓

Analyzer API

↓

Data Preprocessing

↓

AI Model Prediction

↓

Threat Engine

↓

Risk Calculation

↓

Explainable AI

↓

Dashboard
```

---

# 🎯 Explainable AI

RakshakAI does not simply classify data as Safe or Malicious.

Each prediction includes:

- Threat Category
- Confidence Score
- Risk Level
- Risk Score
- AI Explanation
- Security Recommendations

This helps users understand *why* a prediction was made.

---

# 📈 Risk Levels

| Risk Score | Level |
|------------|-------|
| 0 – 25 | Low |
| 26 – 50 | Medium |
| 51 – 75 | High |
| 76 – 100 | Critical |

---

# 📸 Screenshots

## Dashboard

```
Assets/screenshots/dashboard.png
```

## Email Analyzer

```
Assets/screenshots/email.png
```

## URL Analyzer

```
Assets/screenshots/url.png
```

## QR Analyzer

```
Assets/screenshots/qr.png
```

## UPI Analyzer

```
Assets/screenshots/upi.png
```

## Deepfake Detection

```
Assets/screenshots/deepfake.png
```

*(Add screenshots here after uploading them to the repository.)*

---

# 📚 Datasets

The project uses multiple datasets for different cyber threat categories, including:

- Email Phishing
- Malicious URLs
- SMS Scams
- WhatsApp Scams
- Fake Job Postings
- Social Engineering Messages
- UPI Fraud
- QR Threat Detection
- Deepfake Images

---

# 🔮 Future Enhancements

- Voice Scam Detection
- Browser Extension
- Email Integration
- WhatsApp Integration
- Mobile Application
- Cloud Deployment
- Real-Time Threat Intelligence
- SIEM Integration
- AI Security Assistant
- Multilingual Support

---

# 📌 Advantages

- Modular Architecture
- Multiple Detection Engines
- Fast Predictions
- Explainable AI
- User-Friendly Dashboard
- Easy to Extend
- AI-Based Threat Analysis

---

# ⚠️ Limitations

- Performance depends on dataset quality.
- Models require periodic retraining.
- Deepfake detection depends on image quality.
- Voice scam detection is planned for future versions due to the lack of a sufficiently large multilingual dataset.

---


# 📄 License

This project is licensed under the MIT License.

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a Star ⭐

Made with ❤️ for Cybersecurity & AI

</div>