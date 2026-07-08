from flask import Blueprint, jsonify

from utils.history_manager import get_history

history_bp = Blueprint("history", __name__)


@history_bp.route("/api/history")
def history():

    return jsonify(
        {
            "success": True,
            "history": get_history(),
        }
    )
