from flask import Blueprint, request, jsonify
from utils.response_builder import build_response
from utils.risk_mapper import get_risk
from utils.history_manager import save_scan
from utils.threat_scoring import calculate_result

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

        probabilities = model.predict_proba(features)[0]

        print("WhatsApp Classes:", model.classes_)

        confidence = round(max(probabilities) * 100, 2)

        prediction = str(prediction)

        result = prediction

        risk_score = confidence

        if confidence >= 85:
            risk = "CRITICAL"
        elif confidence >= 65:
            risk = "HIGH"
        elif confidence >= 50:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        response = build_response(
            engine="WhatsApp Detector",
            prediction=prediction,
            result=result,
            risk=risk,
            confidence=confidence,
            risk_score=risk_score,
        )
        save_scan(response)

        return jsonify(response)

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(e)}), 500
