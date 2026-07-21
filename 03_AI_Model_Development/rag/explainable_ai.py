"""
RakshakAI v2
AI Investigation Agent
Explainable AI
"""

from __future__ import annotations

from typing import Dict, List


class ExplainableAI:
    """
    Generates human-readable explanations for RAG investigation results.
    """

    def build_explanation(
        self,
        reasoning_result: Dict,
    ) -> Dict:
        """
        Create explainable output.
        """

        findings = reasoning_result.get("findings", [])

        explanation = {
            "summary": reasoning_result.get("summary", ""),
            "confidence": reasoning_result.get("confidence", 0.0),
            "evidence": self._build_evidence(findings),
            "explanation_steps": self._build_steps(findings),
        }

        return explanation

    def _build_evidence(
        self,
        findings: List[Dict],
    ) -> List[Dict]:
        """
        Convert findings into evidence entries.
        """

        evidence = []

        for finding in findings:
            evidence.append(
                {
                    "source": finding.get("source"),
                    "category": finding.get("category"),
                    "relevance_score": finding.get("score"),
                }
            )

        return evidence

    def _build_steps(
        self,
        findings: List[Dict],
    ) -> List[str]:
        """
        Build reasoning steps.
        """

        steps = []

        if not findings:
            steps.append("No supporting knowledge was found.")
            return steps

        steps.append("Relevant knowledge documents were retrieved.")
        steps.append("Similarity scores were calculated.")
        steps.append("Evidence was ranked by relevance.")
        steps.append("Investigation reasoning was generated.")
        steps.append("Final explanation was prepared.")

        return steps

    def health(self) -> Dict:
        """
        Health status.
        """

        return {
            "component": "ExplainableAI",
            "status": "ready",
        }
