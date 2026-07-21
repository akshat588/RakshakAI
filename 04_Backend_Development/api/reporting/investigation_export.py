"""
RakshakAI v2
Investigation Export

Unified export interface for investigation reports.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .json_report import json_report
from .pdf_report import pdf_report


class InvestigationExport:
    """
    Unified investigation export interface.
    """

    def __init__(self) -> None:

        self.json_exporter = json_report
        self.pdf_exporter = pdf_report

    # ==========================================================
    # JSON Export
    # ==========================================================

    def export_json(
        self,
        investigation: Dict[str, Any],
        output_path: str | Path,
    ) -> str:

        return self.json_exporter.save(
            investigation=investigation,
            output_path=output_path,
        )

    # ==========================================================
    # PDF Export
    # ==========================================================

    def export_pdf(
        self,
        investigation: Dict[str, Any],
        output_path: str | Path,
    ) -> str:

        return self.pdf_exporter.save(
            investigation=investigation,
            output_path=output_path,
        )

    # ==========================================================
    # Export Both
    # ==========================================================

    def export_all(
        self,
        investigation: Dict[str, Any],
        output_directory: str | Path,
        filename: str = "investigation_report",
    ) -> Dict[str, str]:

        output_directory = Path(output_directory)

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        json_file = output_directory / f"{filename}.json"
        pdf_file = output_directory / f"{filename}.pdf"

        return {
            "json": self.export_json(
                investigation,
                json_file,
            ),
            "pdf": self.export_pdf(
                investigation,
                pdf_file,
            ),
        }


investigation_export = InvestigationExport()
