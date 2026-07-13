from flask import Blueprint, render_template, request, jsonify

assistant_bp = Blueprint("assistant", __name__)


@assistant_bp.route("/assistant")
def assistant():
    return render_template("assistant/index.html")


@assistant_bp.route("/api/assistant", methods=["POST"])
def assistant_api():
    return jsonify(
        {
            "success": True,
            "type": "placeholder",
            "message": (
                "RakshakAI AI Assistant is ready. "
                "Analyzer routing will be added in the next milestone."
            ),
        }
    )
