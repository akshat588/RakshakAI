from flask import Blueprint, request, jsonify
from utils.response_builder import build_response
from utils.risk_mapper import get_risk
from core.model_loader import (
    load_model,
    load_vectorizer,
)

social_bp = Blueprint("social_engineering", __name__)

model = load_model("social_engineering_detector")
vectorizer = load_vectorizer("social_engineering_vectorizer")


@social_bp.route("/api/social-engineering", methods=["POST"])
def analyze_social():
    try:
        data = request.get_json()

        text = data.get("text", "").strip()

        if not text:
            return (
                jsonify({"success": False, "message": "Input text is required."}),
                400,
            )

        features = vectorizer.transform([text])

        prediction = model.predict(features)[0]

        if isinstance(prediction, str):
            result = prediction
            risk = (
                "HIGH"
                if "social" in prediction.lower() or "phishing" in prediction.lower()
                else "LOW"
            )
        else:
            prediction = int(prediction)
            result = "Social Engineering Attack" if prediction == 1 else "Safe"
            risk = "HIGH" if prediction == 1 else "LOW"

        return jsonify(
            build_response(
                engine="Social Engineering Detector",
                prediction=prediction,
                result=result,
                risk=risk,
            )
        )

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(e)}), 500
