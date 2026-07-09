"""
===============================================================================
RakshakAI
QR Code Threat Analyzer API
===============================================================================
"""

import joblib
from core.model_loader import load_model, load_vectorizer
from utils.response_builder import build_response
from utils.threat_scoring import calculate_result
from api.url import analyze_url_ai
import io
import re
import uuid
import base64
from datetime import datetime

import cv2
import numpy as np

from PIL import Image
from utils.history_manager import save_scan
from flask import Blueprint, request, jsonify

# =============================================================================
# Blueprint
# =============================================================================

qr_bp = Blueprint("qr", __name__)
model = load_model("qr_detector")
vectorizer = load_vectorizer("qr_vectorizer")

# =============================================================================
# Constants
# =============================================================================

SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "ow.ly",
    "buff.ly",
    "cutt.ly",
    "rb.gy",
    "tiny.one",
    "rebrand.ly",
    "lnkd.in",
    "shorturl.at",
}

SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "bank",
    "secure",
    "wallet",
    "reward",
    "gift",
    "kyc",
    "update",
    "otp",
    "password",
    "account",
    "payment",
    "upi",
    "free",
    "claim",
    "bonus",
    "confirm",
    "refund",
    "cashback",
]

TRACKING_PARAMETERS = [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "fbclid",
    "gclid",
    "ref",
    "source",
    "campaign",
]

# =============================================================================
# Helper Functions
# =============================================================================


def generate_scan_id():
    return "RK-QR-" + uuid.uuid4().hex[:8].upper()


def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def classify_payload(data: str):

    text = data.strip()

    lower = text.lower()

    if lower.startswith(("http://", "https://", "www.")):
        return "Website"

    if lower.startswith("upi://"):
        return "UPI"

    if lower.startswith("mailto:"):
        return "Email"

    if lower.startswith("tel:"):
        return "Phone"

    if lower.startswith("wifi:"):
        return "WiFi"

    return "Text"


def decode_image(file_storage):

    image = Image.open(file_storage.stream).convert("RGB")

    image = np.array(image)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    detector = cv2.QRCodeDetector()

    data, points, _ = detector.detectAndDecode(image)

    if points is None:
        return None

    if not data:
        return None

    return data
    return decoded[0].data.decode("utf-8")


def contains_tracking(url):

    lower = url.lower()

    for param in TRACKING_PARAMETERS:

        if param in lower:
            return True

    return False


def contains_unicode(url):

    try:
        url.encode("ascii")
        return False
    except Exception:
        return True


def detect_multiple_urls(text):

    urls = re.findall(r"(https?://[^\s]+)", text, flags=re.IGNORECASE)

    return len(urls) > 1


def contains_shortener(url):

    lower = url.lower()

    for service in SHORTENERS:

        if service in lower:
            return True

    return False


def contains_keywords(url):

    lower = url.lower()

    matched = []

    for word in SUSPICIOUS_KEYWORDS:

        if word in lower:
            matched.append(word)

    return matched


def payload_length_flag(text):

    return len(text) > 250


def hidden_parameters(url):

    return "?" in url or "&" in url


def detect_ip_address(url):

    pattern = r"(?:http[s]?://)?" r"(?:\d{1,3}\.){3}\d{1,3}"

    return re.search(pattern, url) is not None


def detect_encoded_characters(url):

    return "%" in url


def build_base_result():

    return {
        "success": True,
        "scan_id": generate_scan_id(),
        "timestamp": current_timestamp(),
        "engine": "RakshakAI QR Threat Analyzer",
    }


# =============================================================================
# QR Threat Analysis Engine
# =============================================================================


def analyze_url_payload(url: str):

    score = 0

    flags = []

    explanation = []

    recommendations = []

    confidence = 50

    # ---------------------------------------------------------
    # HTTPS
    # ---------------------------------------------------------

    if not url.lower().startswith("https://"):

        score += 15

        flags.append("HTTP Connection")

        explanation.append("The QR redirects to a non-HTTPS website.")

    # ---------------------------------------------------------
    # URL Shortener
    # ---------------------------------------------------------

    if contains_shortener(url):

        score += 20

        flags.append("Shortened URL")

        explanation.append(
            "The QR contains a shortened URL which can hide the final destination."
        )

    # ---------------------------------------------------------
    # Tracking Parameters
    # ---------------------------------------------------------

    if contains_tracking(url):

        score += 8

        flags.append("Tracking Parameters")

        explanation.append("Tracking parameters detected inside the URL.")

    # ---------------------------------------------------------
    # Unicode
    # ---------------------------------------------------------

    if contains_unicode(url):

        score += 12

        flags.append("Unicode Characters")

        explanation.append("Unicode characters may be used for visual impersonation.")

    # ---------------------------------------------------------
    # Encoded Characters
    # ---------------------------------------------------------

    if detect_encoded_characters(url):

        score += 8

        flags.append("Encoded URL")

        explanation.append("Encoded characters detected.")

    # ---------------------------------------------------------
    # IP Address
    # ---------------------------------------------------------

    if detect_ip_address(url):

        score += 18

        flags.append("IP Address")

        explanation.append("Destination uses an IP address instead of a domain.")

    # ---------------------------------------------------------
    # Hidden Parameters
    # ---------------------------------------------------------

    if hidden_parameters(url):

        score += 6

        flags.append("Query Parameters")

        explanation.append("Hidden parameters detected.")

    # ---------------------------------------------------------
    # Long Payload
    # ---------------------------------------------------------

    if payload_length_flag(url):

        score += 10

        flags.append("Long URL")

        explanation.append("Unusually long URL.")

    # ---------------------------------------------------------
    # Suspicious Keywords
    # ---------------------------------------------------------

    keywords = contains_keywords(url)

    if keywords:

        score += min(20, len(keywords) * 4)

        flags.append("Suspicious Keywords")

        explanation.append("Sensitive phishing-related keywords detected.")

    # ---------------------------------------------------------
    # Multiple URLs
    # ---------------------------------------------------------

    if detect_multiple_urls(url):

        score += 20

        flags.append("Multiple URLs")

        explanation.append("More than one URL detected.")

    # ---------------------------------------------------------
    # Clamp Score
    # ---------------------------------------------------------

    score = min(score, 100)

    # ---------------------------------------------------------
    # Risk Level
    # ---------------------------------------------------------

    if score >= 80:

        risk = "CRITICAL"

        prediction = "Malicious"

        confidence = 98

    elif score >= 60:

        risk = "HIGH"

        prediction = "Suspicious"

        confidence = 95

    elif score >= 35:

        risk = "MEDIUM"

        prediction = "Potential Risk"

        confidence = 88

    else:

        risk = "LOW"

        prediction = "Likely Safe"

        confidence = 80

    # ---------------------------------------------------------

    if risk in ["CRITICAL", "HIGH"]:

        recommendations.extend(
            [
                "Do not open this QR code.",
                "Verify the destination manually.",
                "Never enter passwords after scanning.",
            ]
        )

    elif risk == "MEDIUM":

        recommendations.extend(
            ["Proceed carefully.", "Verify the website before sharing information."]
        )

    else:

        recommendations.append("No major threats detected.")

    return {
        "prediction": prediction,
        "risk": risk,
        "risk_score": score,
        "confidence": confidence,
        "flags": flags,
        "explanation": explanation,
        "recommendation": recommendations,
    }


# =============================================================================
# Payload Analysis
# =============================================================================
def analyze_qr_ai(qr_content: str):

    features = vectorizer.transform([qr_content])

    prediction = int(model.predict(features)[0])

    probability = model.predict_proba(features)[0]

    confidence = round(max(probability) * 100, 2)

    risk = "HIGH" if prediction == 1 else "LOW"

    result = "Malicious QR" if prediction == 1 else "Safe QR"

    return {
        "prediction": prediction,
        "result": result,
        "risk": risk,
        "confidence": confidence,
    }


def analyze_payload(payload):

    payload_type = classify_payload(payload)

    result = build_base_result()

    result["qr_type"] = payload_type

    result["decoded_content"] = payload

    # ---------------------------------------------------------

    if payload_type == "Website":

        ai_result = analyze_qr_ai(payload)

        heuristic = analyze_url_payload(payload)

        result.update()
        ai_score = int(ai_result["confidence"])

        risk_score = max(heuristic["risk_score"], ai_score)

        result.update(
            {
                "prediction": ai_result["result"],
                "risk": "HIGH" if ai_result["prediction"] == 1 else heuristic["risk"],
                "confidence": ai_result["confidence"],
                "risk_score": risk_score,
                "flags": heuristic["flags"],
                "explanation": heuristic["explanation"],
                "recommendation": heuristic["recommendation"],
            }
        )

        if ai_result["prediction"] == 1:

            result["recommendation"] = [
                "Do not scan or open this QR code.",
                "Avoid entering credentials or payment details.",
                "Verify the destination through an official source.",
                "Report this QR code if received unexpectedly.",
            ]

    elif payload_type == "UPI":

        result.update(
            {
                "prediction": "UPI QR",
                "risk": "INFO",
                "risk_score": 15,
                "confidence": 100,
                "flags": ["UPI Payment QR"],
                "explanation": ["UPI payment QR detected."],
                "recommendation": ["Verify merchant before payment."],
            }
        )

    elif payload_type == "Email":

        result.update(
            {
                "prediction": "Email QR",
                "risk": "LOW",
                "risk_score": 5,
                "confidence": 100,
                "flags": [],
                "explanation": ["Email QR detected."],
                "recommendation": ["Verify recipient."],
            }
        )

    elif payload_type == "Phone":

        result.update(
            {
                "prediction": "Phone QR",
                "risk": "LOW",
                "risk_score": 5,
                "confidence": 100,
                "flags": [],
                "explanation": ["Telephone QR detected."],
                "recommendation": ["Verify phone number before calling."],
            }
        )

    elif payload_type == "WiFi":

        result.update(
            {
                "prediction": "WiFi QR",
                "risk": "MEDIUM",
                "risk_score": 35,
                "confidence": 90,
                "flags": ["WiFi Credentials"],
                "explanation": ["QR contains WiFi configuration."],
                "recommendation": ["Only join trusted networks."],
            }
        )

    else:

        result.update(
            {
                "prediction": "Plain Text",
                "risk": "LOW",
                "risk_score": 0,
                "confidence": 100,
                "flags": [],
                "explanation": ["No obvious threat detected."],
                "recommendation": ["Review the content manually."],
            }
        )

    return result


# =============================================================================
# API Route
# =============================================================================


@qr_bp.route("/api/qr", methods=["POST"])
def analyze_qr():

    try:

        # -------------------------------------------------------------
        # Validate Upload
        # -------------------------------------------------------------

        if "file" not in request.files:

            return jsonify({"success": False, "message": "No image uploaded."}), 400

        file = request.files["file"]

        if file.filename == "":

            return jsonify({"success": False, "message": "No file selected."}), 400

        # -------------------------------------------------------------
        # Decode QR
        # -------------------------------------------------------------

        payload = decode_image(file)

        if payload is None:

            return jsonify({"success": False, "message": "No QR Code detected."}), 400

        # -------------------------------------------------------------
        # Analyze Payload
        # -------------------------------------------------------------

        result = analyze_payload(payload)

        # -------------------------------------------------------------
        # Extra UI Fields
        # -------------------------------------------------------------

        result["threat_indicators"] = result.get("flags", [])

        result["summary"] = (
            f"RakshakAI classified this QR Code as "
            f"{result['risk']} with a confidence of "
            f"{result['confidence']}%."
        )

        result["timeline"] = [
            "Image Uploaded",
            "QR Decoded",
            "Threat Analysis Completed",
            "AI Decision Generated",
            "Report Ready",
        ]

        save_scan(result)

        return jsonify(result)

    except Exception as e:

        return jsonify({"success": False, "message": str(e)}), 500
