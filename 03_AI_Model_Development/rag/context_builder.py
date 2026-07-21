"""
RakshakAI v2
AI Investigation Agent
Context Builder
"""

from __future__ import annotations

from typing import Dict, List


class ContextBuilder:
    """
    Builds the context supplied to the Investigation Agent
    from retrieved knowledge and investigation data.
    """

    def __init__(self, max_context_documents: int = 5):
        self.max_context_documents = max_context_documents

    def build(
        self,
        query: str,
        retrieved_documents: List[Dict],
        investigation_context: Dict | None = None,
    ) -> Dict:
        """
        Build structured context.
        """

        investigation_context = investigation_context or {}

        documents = []

        for item in retrieved_documents[: self.max_context_documents]:
            document = item.get("document", {})

            documents.append(
                {
                    "id": document.get("id"),
                    "source": document.get("source"),
                    "category": document.get("category"),
                    "content": document.get("content"),
                    "score": item.get("score", 0.0),
                }
            )

        return {
            "query": query,
            "documents": documents,
            "document_count": len(documents),
            "investigation_context": investigation_context,
        }

    def summarize_sources(
        self,
        retrieved_documents: List[Dict],
    ) -> List[str]:
        """
        Return unique document sources.
        """

        sources = []

        for item in retrieved_documents:
            source = item.get("document", {}).get("source")

            if source and source not in sources:
                sources.append(source)

        return sources

    def health(self) -> Dict:
        """
        Component health.
        """

        return {
            "component": "ContextBuilder",
            "status": "ready",
            "max_documents": self.max_context_documents,
        }
