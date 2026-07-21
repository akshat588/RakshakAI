"""
RakshakAI v2
Android API
Dashboard APIs
"""

from __future__ import annotations

from flask import Blueprint, jsonify

mobile_dashboard_bp = Blueprint(
    "mobile_dashboard",
    __name__,
)


@mobile_dashboard_bp.route(
    "/api/mobile/dashboard",
    methods=["GET"],
)
def dashboard():
    """
    Mobile dashboard summary.
    """

    return jsonify(
        {
            "success": True,
            "dashboard": {
                "total_investigations": 0,
                "high_risk_cases": 0,
                "critical_cases": 0,
                "active_campaigns": 0,
                "known_iocs": 0,
                "recent_activity": [],
                "risk_distribution": {},
            },
        }
    )


@mobile_dashboard_bp.route(
    "/api/mobile/dashboard/statistics",
    methods=["GET"],
)
def statistics():
    """
    Dashboard statistics.
    """

    return jsonify(
        {
            "success": True,
            "statistics": {},
        }
    )


@mobile_dashboard_bp.route(
    "/api/mobile/dashboard/activity",
    methods=["GET"],
)
def activity():
    """
    Recent activity.
    """

    return jsonify(
        {
            "success": True,
            "activity": [],
        }
    )
