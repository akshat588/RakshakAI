"""
Universal Investigation Engine
RakshakAI v2
"""

from __future__ import annotations

from datetime import datetime


class InvestigationEngine:

    @staticmethod
    def build(
        analyzer: str,
        engine_result: dict,
        original_input: str,
    ) -> dict:

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "analyzer": analyzer,
            "original_input": original_input,
            "prediction": engine_result["prediction"],
            "result": engine_result["result"],
            "risk": engine_result["risk"],
            "confidence": engine_result["confidence"],
            "risk_score": engine_result["risk_score"],
            "status": ("Threat Detected" if engine_result["risk_score"] >= 70 else "Appears Safe"),
            "evidence": [],
            "recommendations": [],
            "timeline": [],
        }
