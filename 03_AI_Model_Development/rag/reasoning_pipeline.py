"""
RakshakAI v2
AI Investigation Agent
Reasoning Pipeline
"""

from __future__ import annotations

from typing import Dict, List


class ReasoningPipeline:
    """
    Generates structured reasoning from retrieved context.
    """

    def __init__(self):
        pass

    def run(self, context: Dict) -> Dict:
        """
        Execute the reasoning pipeline.
        """

        documents = context.get("documents", [])

        findings = self._extract_findings(documents)

        confidence = self._calculate_confidence(documents)

        return {
            "status": "completed",
            "summary": self._build_summary(findings),
            "findings": findings,
            "confidence": confidence,
            "document_count": len(documents),
        }

    def _extract_findings(self, documents: List[Dict]) -> List[Dict]:
        """
        Convert retrieved documents into reasoning findings.
        """

        findings = []

        for document in documents:
            findings.append(
                {
                    "source": document.get("source"),
                    "category": document.get("category"),
                    "score": document.get("score"),
                    "content": document.get("content"),
                }
            )

        return findings

    def _calculate_confidence(self, documents: List[Dict]) -> float:
        """
        Average retrieval score.
        """

        if not documents:
            return 0.0

        total = sum(float(document.get("score", 0.0)) for document in documents)

        return round((total / len(documents)) * 100, 2)

    def _build_summary(self, findings: List[Dict]) -> str:
        """
        Generate a concise reasoning summary.
        """

        if not findings:
            return "No relevant knowledge was retrieved."

        categories = sorted(
            {finding["category"] for finding in findings if finding.get("category")}
        )

        return (
            f"Retrieved {len(findings)} relevant knowledge "
            f"document(s) covering: {', '.join(categories)}."
        )

    def health(self) -> Dict:
        """
        Component health.
        """

        return {
            "component": "ReasoningPipeline",
            "status": "ready",
        }
