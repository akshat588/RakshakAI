from flask import Blueprint, jsonify
from utils.history_manager import get_history
from utils.threat_scoring import calculate_result
from datetime import datetime

history_bp = Blueprint("history", __name__)


@history_bp.route("/api/history")
def history():

    scans = get_history()

    today = datetime.now().strftime("%Y-%m-%d")

    total = len(scans)

    today_scans = sum(1 for s in scans if s.get("saved_at", "").startswith(today))

    threats = sum(1 for s in scans if s.get("risk") in ["HIGH", "CRITICAL"])

    safe = total - threats

    return jsonify(
        {
            "total": total,
            "today": today_scans,
            "threats": threats,
            "safe": safe,
            "history": scans[:10],
        }
    )
