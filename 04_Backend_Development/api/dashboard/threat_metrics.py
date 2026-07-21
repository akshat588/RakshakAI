"""
RakshakAI v2
Threat Metrics Engine

Generates dashboard threat metrics from investigation data.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List


class ThreatMetrics:
    """
    Computes high-level threat metrics.
    """

    def __init__(self) -> None:
        pass

    # ==========================================================
    # Generate Metrics
    # ==========================================================

    def generate(
        self,
        investigations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        severity_counter = Counter()
        prediction_counter = Counter()

        total_iocs = 0
        total_mitre = 0
        total_campaigns = 0

        for investigation in investigations:

            severity_counter[investigation.get("severity", "safe")] += 1

            prediction_counter[
                str(
                    investigation.get(
                        "prediction",
                        "unknown",
                    )
                ).lower()
            ] += 1

            total_iocs += len(investigation.get("iocs", []))

            total_mitre += len(investigation.get("mitre_attack", []))

            campaign = investigation.get("campaign", {})

            if campaign.get("campaign_detected"):
                total_campaigns += campaign.get(
                    "campaign_count",
                    1,
                )

        total = len(investigations)

        malicious = (
            prediction_counter.get("malicious", 0)
            + prediction_counter.get("fraud", 0)
            + prediction_counter.get("phishing", 0)
            + prediction_counter.get("scam", 0)
        )

        detection_rate = round((malicious / total) * 100, 2) if total else 0

        return {
            "total_investigations": total,
            "malicious_detections": malicious,
            "detection_rate": detection_rate,
            "total_iocs": total_iocs,
            "mapped_mitre_techniques": total_mitre,
            "identified_campaigns": total_campaigns,
            "severity_distribution": dict(severity_counter),
            "prediction_distribution": dict(prediction_counter),
        }


threat_metrics = ThreatMetrics()
