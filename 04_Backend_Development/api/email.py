from flask import Blueprint, request, jsonify
from utils.threat_scoring import calculate_result
from utils.response_builder import build_response
from utils.risk_mapper import get_risk
from utils.history_manager import save_scan
from core.model_loader import (
    load_model,
    load_vectorizer,
)

email_bp = Blueprint("email", __name__)

model = load_model("email_detector")
vectorizer = load_vectorizer("email_vectorizer")


def analyze_email_ai(text: str):
    """
    Reusable Email AI Engine.

    Used by:
    - Existing Email API
    - Universal Assistant
    """

    features = vectorizer.transform([text])

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    result_data = calculate_result(
        prediction=prediction,
        probabilities=probabilities,
        classes=model.classes_,
        safe_label="Safe Email",
        phishing_label="Phishing Email",
    )

    return {
        "prediction": result_data["prediction"],
        "result": result_data["result"],
        "risk": result_data["risk"],
        "confidence": result_data["confidence"],
        "risk_score": result_data["risk_score"],
    }


@email_bp.route("/api/email", methods=["POST"])
def analyze_email():
    try:
        data = request.get_json()

        print("Received Data:", data)

        text = data.get("text", "").strip()

        print("Text:", text)

        if not text:
            return (
                jsonify({"success": False, "message": "Email text is required."}),
                400,
            )

        result_data = analyze_email_ai(text)

        response = build_response(
            engine="Email Detector",
            prediction=result_data["prediction"],
            result=result_data["result"],
            risk=result_data["risk"],
            confidence=result_data["confidence"],
            risk_score=result_data["risk_score"],
        )

        save_scan(response)

        return jsonify(response)

    except Exception as e:
        import traceback

        traceback.print_exc()

        return (
            jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}),
            500,
        )
