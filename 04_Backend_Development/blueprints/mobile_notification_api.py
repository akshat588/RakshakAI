"""
RakshakAI v2
Android API
Notification APIs
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

mobile_notification_bp = Blueprint(
    "mobile_notification",
    __name__,
)


@mobile_notification_bp.route(
    "/api/mobile/notifications",
    methods=["GET"],
)
def list_notifications():
    """
    Retrieve notifications.
    """

    return jsonify(
        {
            "success": True,
            "notifications": [],
        }
    )


@mobile_notification_bp.route(
    "/api/mobile/notifications/read",
    methods=["POST"],
)
def mark_read():
    """
    Mark a notification as read.
    """

    data = request.get_json(silent=True) or {}

    return jsonify(
        {
            "success": True,
            "notification_id": data.get("notification_id"),
            "status": "read",
        }
    )


@mobile_notification_bp.route(
    "/api/mobile/device/register",
    methods=["POST"],
)
def register_device():
    """
    Register a mobile device for push notifications.
    """

    data = request.get_json(silent=True) or {}

    return jsonify(
        {
            "success": True,
            "device_id": data.get("device_id"),
            "registered": True,
        }
    )


@mobile_notification_bp.route(
    "/api/mobile/device/unregister",
    methods=["POST"],
)
def unregister_device():
    """
    Unregister a mobile device.
    """

    data = request.get_json(silent=True) or {}

    return jsonify(
        {
            "success": True,
            "device_id": data.get("device_id"),
            "registered": False,
        }
    )
