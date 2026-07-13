from flask import Blueprint, request, jsonify
from utils.response_builder import build_response
from utils.history_manager import save_scan
from utils.threat_scoring import calculate_result
from core.model_loader import (
    load_model,
    load_vectorizer,
)

sms_bp = Blueprint("sms", __name__)

model = load_model("sms_detector")
vectorizer = load_vectorizer("sms_vectorizer")


def analyze_sms_ai(text: str):
    """
    Reusable SMS AI Engine.

    Used by:
    - Existing SMS API
    - Universal Assistant
    """

    features = vectorizer.transform([text])

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    result_data = calculate_result(
        prediction=prediction,
        probabilities=probabilities,
        classes=model.classes_,
        safe_label="legit",
        phishing_label="scam",
    )

    return {
        "prediction": result_data["prediction"],
        "result": ("Safe SMS" if result_data["result"] == "legit" else "Scam SMS"),
        "risk": result_data["risk"],
        "confidence": result_data["confidence"],
        "risk_score": result_data["risk_score"],
    }


@sms_bp.route("/api/sms", methods=["POST"])
def analyze_sms():
    try:
        data = request.get_json()

        text = data.get("text", "").strip()

        if not text:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "SMS text is required.",
                    }
                ),
                400,
            )

        result_data = analyze_sms_ai(text)

        response = build_response(
            engine="SMS Detector",
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
            jsonify(
                {
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                }
            ),
            500,
        )
