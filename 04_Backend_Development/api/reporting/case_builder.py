"""
RakshakAI v2
Case Builder

Creates a standardized investigation case record that can be used
by the reporting, export, and case management modules.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
from uuid import uuid4


class CaseBuilder:
    """
    Builds standardized investigation case information.
    """

    def __init__(self) -> None:
        pass

    # ==========================================================
    # Case ID
    # ==========================================================

    @staticmethod
    def generate_case_id() -> str:

        timestamp = datetime.utcnow().strftime("%Y%m%d")

        return f"RK-{timestamp}-{uuid4().hex[:8].upper()}"

    # ==========================================================
    # Build Case
    # ==========================================================

    def build(
        self,
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {
            "case_id": self.generate_case_id(),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "status": "completed",
            "platform": "RakshakAI v2",
            "investigation_type": investigation.get(
                "detected_type",
                "unknown",
            ),
            "severity": investigation.get(
                "severity",
                "safe",
            ),
            "risk_score": investigation.get(
                "risk_score",
                0,
            ),
            "prediction": investigation.get(
                "prediction",
                "unknown",
            ),
            "confidence": investigation.get(
                "confidence",
                0,
            ),
            "campaign": investigation.get(
                "campaign",
                {},
            ),
            "reputation": investigation.get(
                "reputation",
                {},
            ),
            "ioc_count": len(investigation.get("iocs", [])),
            "mitre_count": len(investigation.get("mitre_attack", [])),
            "timeline_events": len(investigation.get("timeline", [])),
        }


case_builder = CaseBuilder()
