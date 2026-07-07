from flask import Blueprint, request, jsonify
from utils.response_builder import build_response
from core.model_loader import (
    load_model,
    load_vectorizer,
)

url_bp = Blueprint("url", __name__)

model = load_model("url_detector")
vectorizer = load_vectorizer("url_vectorizer")


@url_bp.route("/api/url", methods=["POST"])
def analyze_url():
    try:
        data = request.get_json()

        url = data.get("url", "").strip()

        if not url:
            return jsonify({"success": False, "message": "URL is required."}), 400

        features = vectorizer.transform([url])

        prediction = model.predict(features)[0]

        prediction = int(prediction)

        risk = "HIGH" if prediction == 1 else "LOW"

        return jsonify(
            build_response(
                engine="URL Detector",
                prediction=prediction,
                result="Phishing URL" if prediction == 1 else "Safe URL",
                risk=risk,
            )
        )

    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(e)}), 500
