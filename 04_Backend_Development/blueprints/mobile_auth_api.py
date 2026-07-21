"""
RakshakAI v2
Android API
Authentication APIs
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

mobile_auth_bp = Blueprint("mobile_auth", __name__)


@mobile_auth_bp.route("/api/mobile/auth/login", methods=["POST"])
def mobile_login():
    """
    Mobile login endpoint.
    """

    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."}), 400

    return jsonify(
        {
            "success": True,
            "token": "",
            "refresh_token": "",
            "user": {},
        }
    )


@mobile_auth_bp.route("/api/mobile/auth/refresh", methods=["POST"])
def refresh_token():
    """
    Refresh access token.
    """

    return jsonify(
        {
            "success": True,
            "token": "",
        }
    )


@mobile_auth_bp.route("/api/mobile/auth/logout", methods=["POST"])
def logout():
    """
    Mobile logout.
    """

    return jsonify({"success": True, "message": "Logged out successfully."})


@mobile_auth_bp.route("/api/mobile/auth/profile", methods=["GET"])
def profile():
    """
    Mobile profile.
    """

    return jsonify(
        {
            "success": True,
            "profile": {},
        }
    )
