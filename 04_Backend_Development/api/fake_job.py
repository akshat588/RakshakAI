from flask import Blueprint, request, jsonify
from utils.response_builder import build_response
from utils.risk_mapper import get_risk
from utils.history_manager import save_scan
from utils.threat_scoring import calculate_result
from core.model_loader import (
    load_model,
    load_vectorizer,
)

fake_job_bp = Blueprint("fake_job", __name__)

model = load_model("fake_job_detector")
vectorizer = load_vectorizer("fake_job_vectorizer")


@fake_job_bp.route("/api/fake-job", methods=["POST"])
def analyze_fake_job():
    try:
        data = request.get_json()

        text = data.get("text", "").strip()

        if not text:
            return (
                jsonify({"success": False, "message": "Job description is required."}),
                400,
            )

        features = vectorizer.transform([text])

        prediction = int(model.predict(features)[0])

        probabilities = model.predict_proba(features)[0]
        print("Prediction:", prediction)
        print("Probabilities:", probabilities)
        print("Classes:", model.classes_)
        print("Fake Job Classes:", model.classes_)

        result_data = calculate_result(
            prediction=prediction,
            probabilities=probabilities,
            classes=model.classes_,
            safe_label=0,
            phishing_label=1,
        )

        response = build_response(
            engine="Fake Job Detector",
            prediction=result_data["prediction"],
            result="Legitimate Job" if result_data["result"] == 0 else "Fake Job",
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
