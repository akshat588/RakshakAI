from flask import Blueprint, request, jsonify
from utils.response_builder import build_response
from utils.risk_mapper import get_risk

from core.model_loader import (
    load_model,
    load_vectorizer,
)

whatsapp_bp = Blueprint("whatsapp", __name__)

model = load_model("whatsapp_detector")
vectorizer = load_vectorizer("whatsapp_vectorizer")


@whatsapp_bp.route("/api/whatsapp", methods=["POST"])
def analyze_whatsapp():
    try:
        data = request.get_json()

        text = data.get("text", "").strip()

        if not text:
            return (
                jsonify({"success": False, "message": "WhatsApp message is required."}),
                400,
            )

        features = vectorizer.transform([text])

        prediction = model.predict(features)[0]

        if isinstance(prediction, str):
            result = prediction
            risk = (
                "HIGH"
                if "phishing" in prediction.lower() or "spam" in prediction.lower()
                else "LOW"
            )
        else:
            prediction = int(prediction)
            result = "Scam Message" if prediction == 1 else "Safe Message"
            risk = "HIGH" if prediction == 1 else "LOW"

        return jsonify(
            build_response(
                engine="WhatsApp Detector",
                prediction=prediction,
                result=result,
                risk=risk,
            )
        )

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(e)}), 500
