from flask import Blueprint, request, jsonify
from utils.response_builder import build_response
from utils.risk_mapper import get_risk
from utils.history_manager import save_scan
from utils.threat_scoring import calculate_result
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

        probabilities = model.predict_proba(features)[0]

        print("Social Classes:", model.classes_)

        result_data = calculate_result(
            prediction=prediction,
            probabilities=probabilities,
            classes=model.classes_,
            safe_label=model.classes_[1],
            phishing_label=model.classes_[0],
        )

        response = build_response(
            engine="Social Engineering Detector",
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

        return jsonify({"success": False, "error": str(e)}), 500
