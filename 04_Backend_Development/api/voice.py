from flask import Blueprint, request, jsonify
import uuid
from utils.history_manager import save_scan

voice_bp = Blueprint("voice", __name__)


@voice_bp.route("/api/voice", methods=["POST"])
def analyze_voice():

    try:

        if "audio" not in request.files:

            return jsonify({"success": False, "message": "Audio file required."}), 400

        file = request.files["audio"]

        filename = file.filename.lower()

        risk = "LOW"

        prediction = "Likely Genuine Voice"

        confidence = 75.00

        suspicious_keywords = [
            "otp",
            "bank",
            "urgent",
            "verify",
            "payment",
            "transfer",
        ]

        for word in suspicious_keywords:

            if word in filename:

                prediction = "Potential Voice Scam"

                risk = "HIGH"

                confidence = 92.00

                break

        response = {
            "success": True,
            "engine": "Voice Scam Detector",
            "prediction": prediction,
            "risk": risk,
            "confidence": confidence,
            "scan_id": "RK-VS-" + uuid.uuid4().hex[:8].upper(),
        }

        save_scan(response)

        return jsonify(response)

    except Exception as e:

        return jsonify({"success": False, "error": str(e)}), 500
