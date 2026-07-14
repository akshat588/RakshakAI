"""RakshakAI v2 - Fake Job Analyzer"""

from flask import Blueprint, request, jsonify
from core.model_loader import load_model, load_vectorizer
from utils.response_builder import build_response
from utils.history_manager import save_scan

fake_job_bp = Blueprint("fake_job", __name__)

model = load_model("fake_job_detector")
vectorizer = load_vectorizer("fake_job_vectorizer")


def analyze_fake_job_ai(text: str) -> dict:
    features = vectorizer.transform([text])
    prediction = model.predict(features)[0]
    risk_score = round(max(model.predict_proba(features)[0]) * 100, 2)

    pred = str(prediction).lower()

    if pred in ("fake", "fraud", "scam"):
        result = "Fake Job Detected"
        status = "Threat Detected"
        risk = "CRITICAL" if risk_score >= 90 else "HIGH" if risk_score >= 70 else "MEDIUM"
    else:
        result = "Legitimate Job"
        status = "Appears Safe"
        risk = "LOW"

    evidence = []
    recommendations = []
    timeline = ["Job posting received.", "AI model analyzed posting."]
    iocs = []

    lower = text.lower()

    for k in [
        "registration fee",
        "pay",
        "urgent hiring",
        "work from home",
        "guaranteed",
        "earn",
        "whatsapp",
        "telegram",
        "investment",
    ]:
        if k in lower:
            evidence.append(f"Suspicious indicator: '{k}'")

    if "http://" in lower or "https://" in lower:
        iocs.append("URL Detected")

    if "@" in lower:
        iocs.append("Email Address Detected")

    if pred in ("fake", "fraud", "scam"):
        recommendations.extend(
            [
                "Verify the employer.",
                "Do not pay registration fees.",
                "Check the official company website.",
                "Report suspicious job postings.",
            ]
        )
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


def investigate_fake_job(text: str) -> dict:
    report = analyze_fake_job_ai(text)
    report.update({"analyzer": "fake_job", "original_input": text})
    return report


@fake_job_bp.route("/api/fake-job", methods=["POST"])
def analyze_fake_job():
    try:
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or data.get("content") or "").strip()

        if not text:
            return jsonify({"success": False, "error": "No job description provided."}), 400

        report = investigate_fake_job(text)

        response = build_response(
            engine="Fake Job Detector",
            prediction=report["prediction"],
            result=report["result"],
            risk=report["risk"],
            confidence=report["confidence"],
            risk_score=report["risk_score"],
        )

        response.update(
            {
                "analyzer": report["analyzer"],
                "status": report["status"],
                "original_input": report["original_input"],
                "evidence": report["evidence"],
                "recommendations": report["recommendations"],
                "timeline": report["timeline"],
                "iocs": report["iocs"],
            }
        )

        save_scan(response)
        return jsonify(response)

    except Exception as exc:
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(exc)}), 500
