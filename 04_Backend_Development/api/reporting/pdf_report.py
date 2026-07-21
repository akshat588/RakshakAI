"""
RakshakAI v2
PDF Report Generator

Generates a PDF investigation report.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from .report_generator import report_generator


class PDFReport:
    """
    PDF Investigation Report Generator.
    """

    def __init__(self) -> None:

        self.generator = report_generator
        self.styles = getSampleStyleSheet()

    # ==========================================================
    # Build PDF
    # ==========================================================

    def save(
        self,
        investigation: Dict[str, Any],
        output_path: str | Path,
    ) -> str:

        report = self.generator.generate(investigation)

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        document = SimpleDocTemplate(str(output_path))

        story = []

        story.append(
            Paragraph(
                "RakshakAI v2 Investigation Report",
                self.styles["Title"],
            )
        )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                f"<b>Case ID:</b> {report['case_information'].get('case_id', '-')}",
                self.styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Severity:</b> {report['severity'].get('severity', '-')}",
                self.styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Risk Score:</b> {report['severity'].get('risk_score', 0)}",
                self.styles["BodyText"],
            )
        )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                "<b>Executive Summary</b>",
                self.styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                report.get("executive_summary", "N/A"),
                self.styles["BodyText"],
            )
        )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                "<b>Indicators of Compromise</b>",
                self.styles["Heading2"],
            )
        )

        iocs = report.get("iocs", [])

        if iocs:
            for ioc in iocs:
                story.append(
                    Paragraph(
                        f"• {ioc}",
                        self.styles["BodyText"],
                    )
                )
        else:
            story.append(
                Paragraph(
                    "No indicators identified.",
                    self.styles["BodyText"],
                )
            )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                "<b>Recommendations</b>",
                self.styles["Heading2"],
            )
        )

        recommendations = report.get("recommendations", [])

        if recommendations:
            for recommendation in recommendations:
                story.append(
                    Paragraph(
                        f"• {recommendation}",
                        self.styles["BodyText"],
                    )
                )
        else:
            story.append(
                Paragraph(
                    "No recommendations available.",
                    self.styles["BodyText"],
                )
            )

        document.build(story)

        return str(output_path.resolve())


pdf_report = PDFReport()
