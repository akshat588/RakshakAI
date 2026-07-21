"""
RakshakAI v2
Report Generator

Central reporting engine responsible for generating standardized
investigation reports.
"""

from __future__ import annotations

from typing import Any, Dict

from .report_formatter import report_formatter
from .evidence_builder import evidence_builder
from .case_builder import case_builder


class ReportGenerator:
    """
    Central Report Generator.
    """

    def __init__(self) -> None:

        self.formatter = report_formatter
        self.evidence_builder = evidence_builder
        self.case_builder = case_builder

    # ==========================================================
    # Full Investigation Report
    # ==========================================================

    def generate(
        self,
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:

        report = self.formatter.format_investigation(investigation)

        report["evidence"] = self.evidence_builder.build(investigation)

        report["case_information"] = self.case_builder.build(investigation)

        return report

    # ==========================================================
    # Executive Report
    # ==========================================================

    def executive(
        self,
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.formatter.format_executive(investigation)

    # ==========================================================
    # Technical Report
    # ==========================================================

    def technical(
        self,
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.formatter.format_technical(investigation)


report_generator = ReportGenerator()
