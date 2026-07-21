"""
RakshakAI v2
Report Templates

Provides reusable report templates for investigation reports.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict


class ReportTemplates:
    """
    Central repository for report templates.
    """

    def __init__(self) -> None:

        self._templates = {
            "investigation": {
                "metadata": {
                    "report_type": "Investigation Report",
                    "version": "2.0",
                },
                "summary": {},
                "executive_summary": "",
                "analysis": {},
                "reputation": {},
                "campaign": {},
                "severity": {},
                "mitre_attack": [],
                "iocs": [],
                "recommendations": [],
                "timeline": [],
                "evidence": {},
                "case_information": {},
            },
            "executive": {
                "metadata": {
                    "report_type": "Executive Report",
                    "version": "2.0",
                },
                "executive_summary": "",
                "risk_score": 0,
                "severity": "safe",
                "key_findings": [],
                "recommendations": [],
            },
            "technical": {
                "metadata": {
                    "report_type": "Technical Report",
                    "version": "2.0",
                },
                "analysis": {},
                "iocs": [],
                "mitre_attack": [],
                "timeline": [],
                "reputation": {},
                "campaign": {},
            },
        }

    def get(self, template_name: str = "investigation") -> Dict[str, Any]:
        """
        Return a deep copy of the requested template.
        """

        return deepcopy(
            self._templates.get(
                template_name,
                self._templates["investigation"],
            )
        )

    def available_templates(self) -> Dict[str, str]:
        """
        List available templates.
        """

        return {key: value["metadata"]["report_type"] for key, value in self._templates.items()}


report_templates = ReportTemplates()
