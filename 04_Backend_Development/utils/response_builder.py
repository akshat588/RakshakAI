from datetime import datetime
import uuid


def build_response(
    engine,
    prediction,
    result,
    risk,
    success=True,
    confidence=None,
    risk_score=None,  # NEW (optional)
):
    return {
        "success": success,
        "engine": engine,
        "prediction": prediction,
        "result": result,
        "risk": risk,
        "confidence": confidence,
        "risk_score": risk_score,  # NEW
        "scan_id": f"RK-{uuid.uuid4().hex[:8].upper()}",
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    }
