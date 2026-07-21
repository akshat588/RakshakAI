"""
RakshakAI v2
Voice Scam Detection Blueprint
"""

from __future__ import annotations

import os
import tempfile

from flask import Blueprint, current_app, jsonify, request
from werkzeug.utils import secure_filename

from services.voice_service import VoiceService

voice_bp = Blueprint("voice", __name__)

_voice_service = None


def get_voice_service():
    global _voice_service

    if _voice_service is None:
        model_directory = current_app.config.get(
            "VOICE_MODEL_DIRECTORY",
            "models/voice_scam",
        )

        investigation_engine = current_app.config.get("UNIVERSAL_INVESTIGATION_ENGINE")

        _voice_service = VoiceService(
            model_directory=model_directory,
            investigation_engine=investigation_engine,
        )

    return _voice_service


@voice_bp.route("/api/voice", methods=["POST"])
def analyze_voice():
    """
    Analyze uploaded voice recording.
    """

    if "audio" not in request.files:
        return jsonify({"success": False, "message": "No audio file uploaded."}), 400

    audio_file = request.files["audio"]

    if audio_file.filename == "":
        return jsonify({"success": False, "message": "Invalid audio file."}), 400

    language = request.form.get("language")

    temp_path = None

    try:
        filename = secure_filename(audio_file.filename)

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(filename)[1],
        ) as temp:
            audio_file.save(temp.name)
            temp_path = temp.name

        service = get_voice_service()

        result = service.analyze(
            audio_path=temp_path,
            language=language,
        )

        return jsonify(
            {
                "success": True,
                "result": result,
            }
        )

    except Exception as exc:
        return (
            jsonify(
                {
                    "success": False,
                    "message": str(exc),
                }
            ),
            500,
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@voice_bp.route("/api/voice/health", methods=["GET"])
def voice_health():
    """
    Voice module health endpoint.
    """

    service = get_voice_service()

    return jsonify(service.health())
