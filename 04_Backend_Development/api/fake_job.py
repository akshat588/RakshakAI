from flask import Blueprint, request, jsonify, render_template
from utils.response_builder import build_response
from utils.risk_mapper import get_risk
from utils.history_manager import save_scan
from utils.threat_scoring import calculate_result
from core.model_loader import (
    load_model,
    load_vectorizer,
)

fake_job_bp = Blueprint("fake_job", __name__)

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


@fake_job_bp.route("/fake-job", methods=["GET"])
def fake_job_page():
    return render_template("analyzers/fake_job.html")


@fake_job_bp.route("/fake-job/result", methods=["GET"])
def fake_job_result():
    return render_template("analyzers/fake_job_result.html")


# ==========================================================
# API
# ==========================================================


@fake_job_bp.route("/api/fake-job", methods=["POST"])
def analyze_fake_job():
    try:
        data = request.get_json()

        text = data.get("text", "").strip()

        if not text:
            return (
                jsonify({"success": False, "message": "Job description is required."}),
                400,
            )

        features = vectorizer.transform([text])

        prediction = int(model.predict(features)[0])

        probabilities = model.predict_proba(features)[0]
        print("Prediction:", prediction)
        print("Probabilities:", probabilities)
        print("Classes:", model.classes_)
        print("Fake Job Classes:", model.classes_)

        result_data = calculate_result(
            prediction=prediction,
            probabilities=probabilities,
            classes=model.classes_,
            safe_label=0,
            phishing_label=1,
        )

        response = build_response(
            engine="Fake Job Detector",
            prediction=result_data["prediction"],
            result="Legitimate Job" if result_data["result"] == 0 else "Fake Job",
            risk=result_data["risk"],
            confidence=result_data["confidence"],
            risk_score=result_data["risk_score"],
        )
        save_scan(response)

        return jsonify(response)
    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(e)}), 500
