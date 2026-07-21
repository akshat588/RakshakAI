"""
RakshakAI v2
Android API
Report APIs
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

mobile_report_bp = Blueprint(
    "mobile_report",
    __name__,
)


@mobile_report_bp.route(
    "/api/mobile/report/generate",
    methods=["POST"],
)
def generate_report():
    """
    Generate investigation report.
    """

    data = request.get_json(silent=True) or {}

    case_id = data.get("case_id", "").strip()
    report_format = data.get("format", "pdf")

    if not case_id:
        return jsonify({"success": False, "message": "Case ID is required."}), 400

    return jsonify(
        {
            "success": True,
            "case_id": case_id,
            "format": report_format,
            "status": "generated",
            "download_url": "",
        }
    )


@mobile_report_bp.route(
    "/api/mobile/report/<case_id>",
    methods=["GET"],
)
def report_status(case_id):
    """
    Report status.
    """

    return jsonify(
        {
            "success": True,
            "case_id": case_id,
            "status": "available",
        }
    )


@mobile_report_bp.route(
    "/api/mobile/report/history",
    methods=["GET"],
)
def report_history():
    """
    Report history.
    """

    return jsonify(
        {
            "success": True,
            "reports": [],
        }
    )
