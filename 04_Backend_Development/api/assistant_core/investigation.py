"""
Universal Investigation Engine
RakshakAI v2

Builds a unified investigation report from any analyzer.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict


class InvestigationEngine:
    """
    Builds a standardized investigation report for all analyzers.
    """

    # Predictions that indicate a threat
    THREAT_LABELS = {
        "scam",
        "spam",
        "phishing",
        "phishing email",
        "phishing url",
        "fraud",
        "fake",
        "malicious",
        "0",  # Some models use 0 for malicious
    }

    @classmethod
    def _is_threat(cls, prediction: Any, risk_score: float) -> bool:
        """
        Determine whether the result should be treated as a threat.
        """

        prediction_text = str(prediction).strip().lower()

        if prediction_text in cls.THREAT_LABELS:
            return True

        try:
            numeric_prediction = int(prediction)

            # Some binary models:
            # 0 = malicious
            # 1 = safe
            if numeric_prediction == 0:
                return True

        except Exception:
            pass

        return risk_score >= 40

    @classmethod
    def build(
        cls,
        analyzer: str,
        engine_result: Dict[str, Any],
        original_input: str,
    ) -> Dict[str, Any]:

        prediction = engine_result.get("prediction")

        result = engine_result.get("result")

        risk = engine_result.get("risk", "UNKNOWN")

        confidence = float(engine_result.get("confidence", 0))

        risk_score = float(engine_result.get("risk_score", 0))

        threat_detected = cls._is_threat(
            prediction=prediction,
            risk_score=risk_score,
        )

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "analyzer": analyzer,
            "original_input": original_input,
            "prediction": prediction,
            "result": result,
            "risk": risk,
            "confidence": confidence,
            "risk_score": risk_score,
            "status": ("Threat Detected" if threat_detected else "Appears Safe"),
            "evidence": [],
            "recommendations": [],
            "timeline": [],
        }
