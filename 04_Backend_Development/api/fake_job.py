from flask import Blueprint, request, jsonify
from utils.response_builder import build_response
from utils.risk_mapper import get_risk
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

        prediction = model.predict(features)[0]

        if isinstance(prediction, str):
            result = prediction
            risk = "HIGH" if "fake" in prediction.lower() else "LOW"
        else:
            prediction = int(prediction)
            result = "Fake Job" if prediction == 1 else "Legitimate Job"
            risk = "HIGH" if prediction == 1 else "LOW"

        return jsonify(
            build_response(
                engine="Fake Job Detector",
                prediction=prediction,
                result=result,
                risk=risk,
            )
        )
    except Exception as e:
        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(e)}), 500
