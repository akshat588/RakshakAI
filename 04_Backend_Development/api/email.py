from flask import Blueprint, request, jsonify
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

        features = vectorizer.transform([text])

        print("Vectorization Successful")

        prediction = model.predict(features)[0]

        try:
            probabilities = model.predict_proba(features)[0]
            confidence = round(max(probabilities) * 100, 2)

        except AttributeError:
            confidence = None

        result = "Phishing Email" if prediction == 1 else "Safe Email"

        risk = get_risk(confidence)

        response = build_response(
            engine="Email Detector",
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

        return (
            jsonify(
                {"success": False, "error": str(e), "traceback": traceback.format_exc()}
            ),
            500,
        )
