from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request

from api.assistant_core.orchestrator import orchestrator

# Registers every analyzer automatically
from api.assistant_core import register_engines

assistant_bp = Blueprint("assistant", __name__)


@assistant_bp.route("/assistant")
def assistant():

    return render_template("assistant/index.html")


@assistant_bp.route("/api/assistant", methods=["POST"])
def assistant_api():

    try:

        data = request.get_json(silent=True) or {}

        content = (data.get("content", "")).strip()

        if not content:

            return jsonify({"success": False, "error": "No content provided."}), 400

        report = orchestrator.run(content)

        return jsonify({"success": True, "report": report})

    except Exception as exc:

        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(exc)}), 500

        # ==========================================================


# Health Endpoint
# ==========================================================


@assistant_bp.route("/api/assistant/health", methods=["GET"])
def assistant_health():

    from api.assistant_core.register_engines import health

    return jsonify(health())


# ==========================================================
# Debug Endpoint
# ==========================================================


@assistant_bp.route("/api/assistant/debug", methods=["GET"])
def assistant_debug():

    from api.assistant_core.register_engines import debug

    return jsonify(debug())


# ==========================================================
# Validation Endpoint
# ==========================================================


@assistant_bp.route("/api/assistant/validate", methods=["GET"])
def assistant_validate():

    from api.assistant_core.register_engines import validate

    return jsonify(validate())

    # ==========================================================


# Registered Engines Endpoint
# ==========================================================


@assistant_bp.route("/api/assistant/engines", methods=["GET"])
def assistant_engines():

    from api.assistant_core.register_engines import registered_engines, engine_count

    return jsonify(
        {"success": True, "engine_count": engine_count(), "engines": registered_engines()}
    )


# ==========================================================
# Reset Orchestrator Endpoint
# ==========================================================


@assistant_bp.route("/api/assistant/reset", methods=["POST"])
def assistant_reset():

    orchestrator.reset()

    from api.assistant_core.register_engines import initialize

    initialize()

    return jsonify(
        {"success": True, "message": "Universal Investigation Engine reset successfully."}
    )

    # ==========================================================


# Investigation Endpoint
# ==========================================================


@assistant_bp.route("/api/assistant/investigate", methods=["POST"])
def investigate():

    try:

        data = request.get_json(silent=True) or {}

        content = (data.get("content", "")).strip()

        if not content:

            return jsonify({"success": False, "error": "No content provided."}), 400

        report = orchestrator.run(content)

        return jsonify({"success": True, "report": report})

    except Exception as exc:

        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(exc)}), 500


# ==========================================================
# Analyzer Detection Endpoint
# ==========================================================


@assistant_bp.route("/api/assistant/detect", methods=["POST"])
def detect():

    try:

        data = request.get_json(silent=True) or {}

        content = (data.get("content", "")).strip()

        if not content:

            return jsonify({"success": False, "error": "No content provided."}), 400

        detected = orchestrator.detector.detect(content)

        engines = orchestrator.select_engines(detected, content)

        return jsonify({"success": True, "detected_type": detected, "selected_engines": engines})

    except Exception as exc:

        return jsonify({"success": False, "error": str(exc)}), 500

        # ==========================================================


# Investigation Summary Endpoint
# ==========================================================


@assistant_bp.route("/api/assistant/summary", methods=["POST"])
def investigation_summary():

    try:

        data = request.get_json(silent=True) or {}

        content = (data.get("content", "")).strip()

        if not content:

            return jsonify({"success": False, "error": "No content provided."}), 400

        report = orchestrator.run(content)

        summary = {
            "overall_risk": report.get("overall_risk"),
            "overall_score": report.get("overall_score"),
            "confidence": report.get("confidence"),
            "verdict": report.get("verdict"),
            "summary": report.get("summary"),
            "executed_engines": report.get("executed_engines", []),
        }

        return jsonify({"success": True, "summary": summary})

    except Exception as exc:

        import traceback

        traceback.print_exc()

        return jsonify({"success": False, "error": str(exc)}), 500


# ==========================================================
# Registered Engine Status Endpoint
# ==========================================================


@assistant_bp.route("/api/assistant/status", methods=["GET"])
def assistant_status():

    from api.assistant_core.register_engines import health

    status = health()

    return jsonify({"success": True, "status": status})

    # ==========================================================


# Version Endpoint
# ==========================================================


@assistant_bp.route("/api/assistant/version", methods=["GET"])
def assistant_version():

    return jsonify(
        {
            "success": True,
            "name": "RakshakAI Universal AI Security Assistant",
            "version": "2.0",
            "mode": "Multi-Analyzer Investigation",
            "framework": "Universal Investigation Engine",
        }
    )


# ==========================================================
# Routes Export
# ==========================================================

__all__ = ["assistant_bp"]
