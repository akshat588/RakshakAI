import json
import os
from datetime import datetime

import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

HISTORY_FILE = os.path.join(
    BASE_DIR,
    "data",
    "scan_history.json",
)


def json_converter(obj):
    """
    Convert NumPy objects into native Python types.
    """

    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, np.bool_):
        return bool(obj)

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:

            content = f.read().strip()

            if not content:
                return []

            return json.loads(content)

    except Exception:
        return []


def save_scan(result):

    history = load_history()

    normalized = {
        "scan_id": result.get("scan_id", "-"),
        "engine": result.get("engine", "-"),
        "analyzer": result.get(
            "analyzer",
            result.get("engine", "Unknown"),
        ),
        "prediction": result.get(
            "prediction",
            result.get("result", "-"),
        ),
        "result": result.get(
            "result",
            result.get("prediction", "-"),
        ),
        "risk": result.get("risk", "-"),
        "confidence": result.get("confidence"),
        "risk_score": result.get(
            "risk_score",
            result.get("ai_risk_score"),
        ),
        "timestamp": result.get(
            "timestamp",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    if "input_summary" in result:
        normalized["input_summary"] = result["input_summary"]

    history.insert(0, normalized)

    history = history[:100]

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:

        json.dump(
            history,
            f,
            indent=4,
            ensure_ascii=False,
            default=json_converter,
        )


def get_history():

    return load_history()
