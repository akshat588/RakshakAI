"""RakshakAI v2 - Fake Job Analyzer"""

from flask import Blueprint, request, jsonify, render_template
from core.model_loader import load_model, load_vectorizer
from utils.response_builder import build_response
from utils.history_manager import save_scan

fake_job_bp = Blueprint("fake_job", __name__, url_prefix="/fake-job")

model = load_model("fake_job_detector")
vectorizer = load_vectorizer("fake_job_vectorizer")


def analyze_fake_job_ai(text: str) -> dict:
    """Analyze a job posting using the trained ML model."""

    features = vectorizer.transform([text])
    prediction = model.predict(features)[0]
    risk_score = round(max(model.predict_proba(features)[0]) * 100, 2)

    prediction_str = str(prediction).lower()

    # ----------------------------------
    # Prediction Mapping
    # ----------------------------------
    if prediction_str in ("1", "fake", "fraud", "scam", "malicious"):
        result = "Fake Job Detected"
        status = "Threat Detected"

        if risk_score >= 90:
            risk = "CRITICAL"
        elif risk_score >= 70:
            risk = "HIGH"
        else:
            risk = "MEDIUM"

    else:
        result = "Legitimate Job"
        status = "Appears Safe"
        risk = "LOW"

    # ----------------------------------
    # Explainable AI
    # ----------------------------------
    evidence = []
    recommendations = []
    iocs = []

    timeline = [
        "Job posting received.",
        "AI model analyzed the content.",
        "Fraud indicators evaluated.",
        "Investigation report generated.",
    ]

    lower = text.lower()

    suspicious_keywords = [
        "registration fee",
        "pay",
        "payment",
        "joining fee",
        "processing fee",
        "security deposit",
        "urgent hiring",
        "work from home",
        "earn",
        "guaranteed",
        "telegram",
        "whatsapp",
        "investment",
        "limited seats",
        "instant joining",
        "click here",
    ]

    for keyword in suspicious_keywords:
        if keyword in lower:
            evidence.append(f"Suspicious keyword detected: '{keyword}'")

    if "http://" in lower or "https://" in lower:
        iocs.append("Suspicious URL Found")

    if "@" in lower:
        iocs.append("Recruiter Email Present")

    if "+" in lower:
        iocs.append("Phone Number Present")

    if prediction_str in ("1", "fake", "fraud", "scam", "malicious"):
        recommendations.extend(
            [
                "Verify the company using its official website.",
                "Never pay registration or joining fees.",
                "Avoid communicating only through WhatsApp or Telegram.",
                "Research company reviews before applying.",
                "Report suspicious job advertisements.",
            ]
        )
    else:
        recommendations.extend(
            [
                "Continue verifying employer information.",
                "Cross-check the company website before applying.",
            ]
        )

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
    """Run complete fake job investigation."""
    report = analyze_fake_job_ai(text)
    report.update(
        {
            "analyzer": "fake_job",
            "original_input": text,
        }
    )
    return report


# ==========================================================
# Pages
# ==========================================================


@fake_job_bp.route("/", methods=["GET"])
def fake_job_page():
    return render_template("analyzers/fake_job.html")


@fake_job_bp.route("/result", methods=["GET"])
def fake_job_result():
    return render_template("analyzers/fake_job_result.html")


# ==========================================================
# API
# ==========================================================


@fake_job_bp.route("/api/fake-job", methods=["POST"])
def analyze_fake_job():
    try:
        data = request.get_json(silent=True) or {}

        text = (data.get("text") or data.get("content") or "").strip()

        if not text:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "No job description provided.",
                    }
                ),
                400,
            )

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
                # Explainable AI
                "evidence": report["evidence"],
                "explanation": report["evidence"],
                # Recommendations
                "recommendations": report["recommendations"],
                "recommendation": report["recommendations"],
                # Timeline
                "timeline": report["timeline"],
                # Indicators
                "iocs": report["iocs"],
                "flags": report["iocs"],
                # UI
                "engine": "Fake Job Detector",
            }
        )

        save_scan(response)

        return jsonify(response)

    except Exception as exc:
        import traceback

        traceback.print_exc()

        return (
            jsonify(
                {
                    "success": False,
                    "error": str(exc),
                }
            ),
            500,
        )
