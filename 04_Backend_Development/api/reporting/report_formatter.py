"""
RakshakAI v2
Report Formatter

Formats investigation data into standardized report structures.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict

from .report_templates import report_templates


class ReportFormatter:
    """
    Standardizes investigation reports.
    """

    def __init__(self) -> None:

        self.templates = report_templates

    # ==========================================================
    # Metadata
    # ==========================================================

    @staticmethod
    def _metadata() -> Dict[str, Any]:

        return {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "generated_by": "RakshakAI v2",
        }

    # ==========================================================
    # Investigation Report
    # ==========================================================

    def format_investigation(
        self,
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:

        report = self.templates.get("investigation")

        report["metadata"].update(self._metadata())

        report["summary"] = deepcopy(investigation.get("summary", {}))

        report["executive_summary"] = investigation.get(
            "executive_summary",
            "",
        )

        report["analysis"] = deepcopy(investigation.get("analysis", {}))

        report["reputation"] = deepcopy(investigation.get("reputation", {}))

        report["campaign"] = deepcopy(investigation.get("campaign", {}))

        report["severity"] = {
            "risk_score": investigation.get(
                "risk_score",
                0,
            ),
            "severity": investigation.get(
                "severity",
                "safe",
            ),
        }

        report["mitre_attack"] = deepcopy(investigation.get("mitre_attack", []))

        report["iocs"] = deepcopy(investigation.get("iocs", []))

        report["recommendations"] = deepcopy(investigation.get("recommendations", []))

        report["timeline"] = deepcopy(investigation.get("timeline", []))

        report["evidence"] = deepcopy(investigation.get("evidence", {}))

        report["case_information"] = deepcopy(investigation.get("case_information", {}))

        return report

    # ==========================================================
    # Executive Report
    # ==========================================================

    def format_executive(
        self,
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:

        report = self.templates.get("executive")

        report["metadata"].update(self._metadata())

        report["executive_summary"] = investigation.get(
            "executive_summary",
            "",
        )

        report["risk_score"] = investigation.get(
            "risk_score",
            0,
        )

        report["severity"] = investigation.get(
            "severity",
            "safe",
        )

        report["key_findings"] = deepcopy(investigation.get("key_findings", []))

        report["recommendations"] = deepcopy(investigation.get("recommendations", []))

        return report

    # ==========================================================
    # Technical Report
    # ==========================================================

    def format_technical(
        self,
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:

        report = self.templates.get("technical")

        report["metadata"].update(self._metadata())

        report["analysis"] = deepcopy(investigation.get("analysis", {}))

        report["iocs"] = deepcopy(investigation.get("iocs", []))

        report["mitre_attack"] = deepcopy(investigation.get("mitre_attack", []))

        report["timeline"] = deepcopy(investigation.get("timeline", []))

        report["reputation"] = deepcopy(investigation.get("reputation", {}))

        report["campaign"] = deepcopy(investigation.get("campaign", {}))

        return report


report_formatter = ReportFormatter()
