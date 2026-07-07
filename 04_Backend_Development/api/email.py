from flask import Blueprint, request, jsonify
from utils.response_builder import build_response
from utils.risk_mapper import get_risk
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

        return jsonify(
            build_response(
                engine="Email Detector",
                prediction=prediction,
                result=prediction,
                risk=get_risk(prediction),
            )
        )

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(e)}), 500
