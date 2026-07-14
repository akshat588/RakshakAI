"""
==========================================================
RakshakAI v2
Executive Summary Generator
==========================================================
"""

from __future__ import annotations

from typing import Dict


class ExecutiveSummary:

    def generate(self, report: Dict) -> Dict:

        risk = report.get("overall_risk", "UNKNOWN")

        score = report.get("overall_score", 0)

        confidence = report.get("confidence", 0)

        engines = report.get("executed_engines", [])

        evidence = report.get("evidence", [])

        iocs = report.get("iocs", [])

        verdict = report.get("verdict", "")

        summary = (
            f"RakshakAI completed a multi-analyzer cyber investigation "
            f"using {len(engines)} analyzer(s). "
            f"The investigation produced an overall "
            f"{risk} risk rating with a threat score "
            f"of {score}/100 and a confidence of "
            f"{confidence}%. "
            f"{len(evidence)} evidence item(s) and "
            f"{len(iocs)} indicator(s) of compromise "
            f"were identified. "
            f"{verdict}"
        )

        return {
            "title": "Executive Investigation Summary",
            "summary": summary,
            "risk": risk,
            "threat_score": score,
            "confidence": confidence,
            "analyzers_used": engines,
            "evidence_count": len(evidence),
            "ioc_count": len(iocs),
        }
