from flask import Blueprint, render_template, request, jsonify

from api.assistant_core.detector import UniversalInputDetector
from api.assistant_core.router import UniversalRouter
from api.assistant_core.investigation import InvestigationEngine

assistant_bp = Blueprint("assistant", __name__)


@assistant_bp.route("/assistant")
def assistant():
    return render_template("assistant/index.html")


@assistant_bp.route("/api/assistant", methods=["POST"])
def assistant_api():
    try:
        data = request.get_json()

        content = data.get("content", "").strip()

        if not content:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Content is required.",
                    }
                ),
                400,
            )

        input_type = UniversalInputDetector.detect(content)

        engine_result = UniversalRouter.analyze(
            input_type=input_type,
            content=content,
        )

        report = InvestigationEngine.build(
            analyzer=input_type,
            engine_result=engine_result,
            original_input=content,
        )

        return jsonify(
            {
                "success": True,
                "detected_type": input_type,
                "report": report,
            }
        )

    except Exception as e:
        import traceback

        traceback.print_exc()

        return (
            jsonify(
                {
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                }
            ),
            500,
        )
