"""RakshakAI v2 - Social Engineering Analyzer"""

from flask import Blueprint, request, jsonify, render_template
from core.model_loader import load_model, load_vectorizer
from utils.response_builder import build_response
from utils.history_manager import save_scan

social_bp = Blueprint(
    "social_engineering",
    __name__,
    url_prefix="/social-engineering",
)

model = load_model("social_engineering_detector")
vectorizer = load_vectorizer("social_engineering_vectorizer")


def analyze_social_engineering_ai(text: str) -> dict:

    features = vectorizer.transform([text])

    prediction = model.predict(features)[0]
    confidence = round(max(model.predict_proba(features)[0]) * 100, 2)

    prediction_str = str(prediction).lower()

    if prediction_str in ("1", "scam", "fraud", "social_engineering", "malicious"):
        result = "Social Engineering Attack Detected"
        status = "Threat Detected"

        if confidence >= 90:
            risk = "CRITICAL"
        elif confidence >= 70:
            risk = "HIGH"
        else:
            risk = "MEDIUM"

    else:
        result = "Conversation Appears Safe"
        status = "Appears Safe"
        risk = "LOW"

    explanation = []
    recommendations = []
    flags = []

    timeline = [
        "Conversation received.",
        "AI model analyzed the content.",
        "Manipulation patterns detected.",
        "Investigation completed.",
    ]

    lower = text.lower()

    keywords = [
        "otp",
        "password",
        "bank",
        "verify",
        "urgent",
        "immediately",
        "click",
        "link",
        "gift",
        "lottery",
        "telegram",
        "whatsapp",
        "investment",
        "refund",
        "account blocked",
        "security team",
    ]

    for keyword in keywords:
        if keyword in lower:
            explanation.append(f"Suspicious keyword detected: '{keyword}'")

    if "http://" in lower or "https://" in lower:
        flags.append("Suspicious URL Found")

    if "@" in lower:
        flags.append("Email Address Present")

    if "+" in lower:
        flags.append("Phone Number Present")

    if prediction_str in ("1", "scam", "fraud", "social_engineering", "malicious"):

        recommendations.extend(
            [
                "Do not share OTPs or passwords.",
                "Verify the sender independently.",
                "Avoid clicking unknown links.",
                "Never transfer money under pressure.",
                "Report suspicious conversations.",
            ]
        )

    else:

        recommendations.extend(
            [
                "Continue verifying unexpected requests.",
                "Stay cautious when sharing sensitive information.",
            ]
        )

    return {
        "prediction": prediction,
        "result": result,
        "risk": risk,
        "confidence": confidence,
        "risk_score": confidence,
        "status": status,
        "engine": "Social Engineering Detector",
        "timeline": timeline,
        "explanation": explanation,
        "evidence": explanation,
        "flags": flags,
        "iocs": flags,
        "recommendation": recommendations,
        "recommendations": recommendations,
    }


@social_bp.route("/")
def social_engineering_page():
    return render_template("analyzers/social_engineering.html")


@social_bp.route("/result")
def social_engineering_result():
    return render_template("analyzers/social_engineering_result.html")


@social_bp.route("/api/social-engineering", methods=["POST"])
def analyze_social_engineering():

    try:

        data = request.get_json(silent=True) or {}

        text = (data.get("text") or data.get("content") or "").strip()

        if not text:

            return (
                jsonify(
                    {
                        "success": False,
                        "error": "No conversation provided.",
                    }
                ),
                400,
            )

        report = analyze_social_engineering_ai(text)

        response = build_response(
            engine=report["engine"],
            prediction=report["prediction"],
            result=report["result"],
            risk=report["risk"],
            confidence=report["confidence"],
            risk_score=report["risk_score"],
        )

        response.update(report)

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
