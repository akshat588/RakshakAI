"""RakshakAI v2 - Social Engineering Analyzer"""

from flask import Blueprint, request, jsonify
from core.model_loader import load_model, load_vectorizer
from utils.response_builder import build_response
from utils.history_manager import save_scan

social_bp = Blueprint("social", __name__)
model = load_model("social_engineering_detector")
vectorizer = load_vectorizer("social_engineering_vectorizer")


def analyze_social_engineering_ai(text: str) -> dict:
    x = vectorizer.transform([text])
    pred = model.predict(x)[0]
    score = round(max(model.predict_proba(x)[0]) * 100, 2)
    p = str(pred).lower()
    risk = "LOW"
    status = "Appears Safe"
    result = "No Social Engineering Detected"
    if p in ("attack", "social_engineering", "scam", "malicious", "phishing"):
        result = "Social Engineering Detected"
        status = "Threat Detected"
        risk = "CRITICAL" if score >= 90 else "HIGH" if score >= 70 else "MEDIUM"
    lower = text.lower()
    evidence = []
    timeline = ["Content received.", "AI model analyzed content."]
    iocs = []
    recs = []
    for k in [
        "urgent",
        "immediately",
        "verify",
        "password",
        "otp",
        "bank",
        "click",
        "limited time",
        "account blocked",
        "gift",
    ]:
        if k in lower:
            evidence.append(f"Suspicious indicator: '{k}'")
    if "http://" in lower or "https://" in lower:
        iocs.append("URL Detected")
    if "@" in lower:
        iocs.append("Email/UPI Detected")
    if status == "Threat Detected":
        recs += [
            "Do not share credentials.",
            "Verify sender independently.",
            "Avoid clicking unknown links.",
            "Report suspicious communication.",
        ]
    else:
        recs.append("No major indicators detected.")
    return {
        "prediction": pred,
        "result": result,
        "risk": risk,
        "confidence": score,
        "risk_score": score,
        "status": status,
        "evidence": evidence,
        "recommendations": recs,
        "timeline": timeline,
        "iocs": iocs,
    }


def investigate_social_engineering(text: str) -> dict:
    r = analyze_social_engineering_ai(text)
    r.update({"analyzer": "social_engineering", "original_input": text})
    return r


@social_bp.route("/api/social-engineering", methods=["POST"])
def analyze_social_engineering():
    try:
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or data.get("content") or "").strip()
        if not text:
            return jsonify({"success": False, "error": "No content provided."}), 400
        r = investigate_social_engineering(text)
        resp = build_response(
            engine="Social Engineering Detector",
            prediction=r["prediction"],
            result=r["result"],
            risk=r["risk"],
            confidence=r["confidence"],
            risk_score=r["risk_score"],
        )
        resp.update(
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
        save_scan(resp)
        return jsonify(resp)
    except Exception as exc:
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(exc)}), 500
