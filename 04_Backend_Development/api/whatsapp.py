"""RakshakAI v2 - WhatsApp Analyzer"""

from flask import Blueprint, request, jsonify
from core.model_loader import load_model, load_vectorizer
from utils.response_builder import build_response
from utils.history_manager import save_scan

whatsapp_bp = Blueprint("whatsapp", __name__)
model = load_model("whatsapp_detector")
vectorizer = load_vectorizer("whatsapp_vectorizer")


def analyze_whatsapp_ai(text: str) -> dict:
    features = vectorizer.transform([text])
    prediction = model.predict(features)[0]
    risk_score = round(max(model.predict_proba(features)[0]) * 100, 2)
    p = str(prediction).lower()
    if p == "scam":
        result = "Scam WhatsApp Message"
        status = "Threat Detected"
        risk = "CRITICAL" if risk_score >= 90 else "HIGH" if risk_score >= 70 else "MEDIUM"
    else:
        result = "Safe WhatsApp Message"
        status = "Appears Safe"
        risk = "LOW"
    evidence = []
    recommendations = []
    timeline = ["WhatsApp message received.", "AI model analyzed message."]
    iocs = []
    lower = text.lower()
    for k in [
        "urgent",
        "immediately",
        "click",
        "verify",
        "winner",
        "won",
        "lottery",
        "reward",
        "gift",
        "otp",
        "bank",
        "account blocked",
        "limited time",
    ]:
        if k in lower:
            evidence.append(f"Suspicious keyword detected: '{k}'")
    if "http://" in lower or "https://" in lower:
        evidence.append("Message contains URL")
        timeline.append("URL detected")
    if "@" in lower:
        iocs.append("Possible UPI ID or email detected")
    if p == "scam":
        recommendations += [
            "Do not click links.",
            "Do not share OTP or banking details.",
            "Verify the sender independently.",
            "Report and block the sender.",
        ]
    else:
        recommendations.append("No major indicators detected.")
    return {
        "prediction": prediction,
        "result": result,
        "risk": risk,
        "confidence": risk_score,
        "risk_score": risk_score,
        "status": status,
        "evidence": evidence,
        "recommendations": recommendations,
        "timeline": timeline,
        "iocs": iocs,
    }


def investigate_whatsapp(text: str) -> dict:
    r = analyze_whatsapp_ai(text)
    r.update({"analyzer": "whatsapp", "original_input": text})
    return r


@whatsapp_bp.route("/api/whatsapp", methods=["POST"])
def analyze_whatsapp():
    try:
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or data.get("content") or "").strip()
        if not text:
            return jsonify({"success": False, "error": "No WhatsApp message provided."}), 400
        r = investigate_whatsapp(text)
        response = build_response(
            engine="WhatsApp Detector",
            prediction=r["prediction"],
            result=r["result"],
            risk=r["risk"],
            confidence=r["confidence"],
            risk_score=r["risk_score"],
        )
        response.update(
            {
                "analyzer": r["analyzer"],
                "status": r["status"],
                "original_input": r["original_input"],
                "evidence": r["evidence"],
                "recommendations": r["recommendations"],
                "timeline": r["timeline"],
                "iocs": r["iocs"],
            }
        )
        save_scan(response)
        return jsonify(response)
    except Exception as exc:
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(exc)}), 500
