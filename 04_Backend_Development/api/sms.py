from flask import Blueprint, request, jsonify
from utils.response_builder import build_response
from utils.risk_mapper import get_risk
from utils.history_manager import save_scan
from core.model_loader import (
    load_model,
    load_vectorizer,
)

sms_bp = Blueprint("sms", __name__)

model = load_model("sms_detector")
vectorizer = load_vectorizer("sms_vectorizer")


@sms_bp.route("/api/sms", methods=["POST"])
def analyze_sms():
    try:
        data = request.get_json()

        text = data.get("text", "").strip()

        if not text:
            return jsonify({"success": False, "message": "SMS text is required."}), 400

        features = vectorizer.transform([text])

        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]

        confidence = round(max(probabilities) * 100, 2)

        if isinstance(prediction, str):
            result = prediction
            risk = (
                "HIGH"
                if "phishing" in prediction.lower() or "spam" in prediction.lower()
                else "LOW"
            )
        else:
            prediction = int(prediction)
            result = "Spam SMS" if prediction == 1 else "Safe SMS"
            risk = "HIGH" if prediction == 1 else "LOW"

        response = build_response(
            engine="SMS Detector",
            prediction=prediction,
            result=result,
            risk=risk,
            confidence=confidence,
        )

        save_scan(response)

        return jsonify(response)
    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(e)}), 500
