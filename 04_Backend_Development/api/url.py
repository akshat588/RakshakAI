from flask import Blueprint, request, jsonify
from utils.response_builder import build_response
from utils.history_manager import save_scan
from utils.threat_scoring import calculate_result
from core.model_loader import (
    load_model,
    load_vectorizer,
)

url_bp = Blueprint("url", __name__)

model = load_model("url_detector")
vectorizer = load_vectorizer("url_vectorizer")


def analyze_url_ai(url: str):

    features = vectorizer.transform([url])

    prediction = int(model.predict(features)[0])

    probabilities = model.predict_proba(features)[0]

    result_data = calculate_result(
        prediction=prediction,
        probabilities=probabilities,
        classes=model.classes_,
        safe_label=1,
        phishing_label=0,
    )

    return {
        "prediction": result_data["prediction"],
        "result": "Safe URL" if result_data["result"] == 1 else "Phishing URL",
        "risk": result_data["risk"],
        "confidence": result_data["confidence"],
        "risk_score": result_data["risk_score"],
    }


@url_bp.route("/api/url", methods=["POST"])
def analyze_url():
    try:
        data = request.get_json()

        url = data.get("url", "").strip()

        if not url:
            return jsonify({"success": False, "message": "URL is required."}), 400

        features = vectorizer.transform([url])

        prediction = int(model.predict(features)[0])

        probabilities = model.predict_proba(features)[0]

        print("Prediction:", prediction)
        print("Probabilities:", probabilities)
        print("Classes:", model.classes_)

        result_data = calculate_result(
            prediction=prediction,
            probabilities=probabilities,
            classes=model.classes_,
            safe_label=1,
            phishing_label=0,
        )

        response = build_response(
            engine="URL Detector",
            prediction=result_data["prediction"],
            result="Safe URL" if result_data["result"] == 1 else "Phishing URL",
            risk=result_data["risk"],
            confidence=result_data["confidence"],
            risk_score=result_data["risk_score"],
        )

        save_scan(response)

        return jsonify(response)

    except Exception as e:
        import traceback

        traceback.print_exc()

        return (
            jsonify(
                {
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                }
            ),
            500,
        )
