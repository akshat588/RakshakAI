"""
RakshakAI v2
Evidence Builder

Builds structured investigation evidence from analyzer outputs.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List


class EvidenceBuilder:
    """
    Creates a normalized evidence package for investigation reports.
    """

    def __init__(self) -> None:
        pass

    # ==========================================================
    # Analyzer Evidence
    # ==========================================================

    def build_analyzer_evidence(
        self,
        analyzers: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        evidence = []

        for analyzer in analyzers:

            evidence.append(
                {
                    "analyzer": analyzer.get("name"),
                    "status": analyzer.get("status"),
                    "prediction": analyzer.get("prediction"),
                    "confidence": analyzer.get("confidence", 0),
                    "severity": analyzer.get("severity"),
                    "summary": analyzer.get("summary"),
                }
            )

        return evidence

    # ==========================================================
    # IOC Evidence
    # ==========================================================

    def build_ioc_evidence(
        self,
        iocs: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        return {
            "count": len(iocs),
            "items": deepcopy(iocs),
        }

    # ==========================================================
    # Reputation Evidence
    # ==========================================================

    def build_reputation_evidence(
        self,
        reputation: Dict[str, Any],
    ) -> Dict[str, Any]:

        return deepcopy(reputation)

    # ==========================================================
    # Timeline Evidence
    # ==========================================================

    def build_timeline_evidence(
        self,
        timeline: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        return {
            "events": deepcopy(timeline),
            "event_count": len(timeline),
        }

    # ==========================================================
    # Complete Evidence Package
    # ==========================================================

    def build(
        self,
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "analyzers": self.build_analyzer_evidence(investigation.get("analyzers", [])),
            "ioc_evidence": self.build_ioc_evidence(investigation.get("iocs", [])),
            "reputation": self.build_reputation_evidence(investigation.get("reputation", {})),
            "timeline": self.build_timeline_evidence(investigation.get("timeline", [])),
            "mitre_attack": deepcopy(investigation.get("mitre_attack", [])),
            "campaign": deepcopy(investigation.get("campaign", {})),
        }


evidence_builder = EvidenceBuilder()
