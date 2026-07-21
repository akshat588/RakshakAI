"""
RakshakAI v2
JSON Report Generator

Creates JSON exports for investigation reports.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from .report_generator import report_generator


class JSONReport:
    """
    JSON Report Exporter.
    """

    def __init__(self) -> None:
        self.generator = report_generator

    # ==========================================================
    # Generate JSON Dictionary
    # ==========================================================

    def generate(
        self,
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.generator.generate(investigation)

    # ==========================================================
    # JSON String
    # ==========================================================

    def to_json(
        self,
        investigation: Dict[str, Any],
        indent: int = 4,
    ) -> str:

        report = self.generate(investigation)

        return json.dumps(
            report,
            indent=indent,
            ensure_ascii=False,
            default=str,
        )

    # ==========================================================
    # Save JSON
    # ==========================================================

    def save(
        self,
        investigation: Dict[str, Any],
        output_path: str | Path,
        indent: int = 4,
    ) -> str:

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            self.to_json(
                investigation,
                indent=indent,
            ),
            encoding="utf-8",
        )

        return str(output_path.resolve())


json_report = JSONReport()
