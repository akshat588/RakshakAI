"""
RakshakAI v2
Threat Timeline Builder

Builds a chronological investigation timeline from analyzer outputs.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


class TimelineBuilder:
    """
    Investigation Timeline Builder
    """

    def __init__(self) -> None:
        pass

    # ==========================================================
    # Timestamp
    # ==========================================================

    @staticmethod
    def current_timestamp() -> str:

        return datetime.utcnow().isoformat() + "Z"

    # ==========================================================
    # Single Event
    # ==========================================================

    def create_event(
        self,
        stage: str,
        title: str,
        description: str,
        severity: str = "info",
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        return {
            "timestamp": self.current_timestamp(),
            "stage": stage,
            "title": title,
            "description": description,
            "severity": severity,
            "metadata": metadata or {},
        }

    # ==========================================================
    # Investigation Timeline
    # ==========================================================

    def build(
        self,
        investigation: Dict[str, Any],
    ) -> List[Dict[str, Any]]:

        timeline: List[Dict[str, Any]] = []

        timeline.append(
            self.create_event(
                stage="input",
                title="Investigation Started",
                description="User submitted content for investigation.",
            )
        )

        analyzers = investigation.get("analyzers", [])

        for analyzer in analyzers:

            timeline.append(
                self.create_event(
                    stage="analysis",
                    title=f"{analyzer.get('name', 'Analyzer')} Completed",
                    description=analyzer.get(
                        "summary",
                        "Analysis completed.",
                    ),
                    severity=analyzer.get("severity", "info"),
                    metadata={
                        "confidence": analyzer.get("confidence"),
                    },
                )
            )

        reputation = investigation.get("reputation")

        if reputation:

            timeline.append(
                self.create_event(
                    stage="reputation",
                    title="Threat Intelligence Lookup",
                    description="Reputation lookup completed.",
                    severity=reputation.get("risk", "info"),
                    metadata=reputation,
                )
            )

        campaign = investigation.get("campaign")

        if campaign:

            timeline.append(
                self.create_event(
                    stage="campaign",
                    title="Campaign Correlation",
                    description="Threat campaign mapping completed.",
                    severity=campaign.get("severity", "info"),
                    metadata=campaign,
                )
            )

        timeline.append(
            self.create_event(
                stage="result",
                title="Investigation Finished",
                description="Threat investigation completed successfully.",
                severity=investigation.get("severity", "info"),
                metadata={
                    "risk_score": investigation.get("risk_score"),
                },
            )
        )

        return timeline


timeline_builder = TimelineBuilder()
