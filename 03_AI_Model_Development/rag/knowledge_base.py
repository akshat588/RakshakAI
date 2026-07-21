"""
RakshakAI v2
AI Investigation Agent
Knowledge Base
"""

from __future__ import annotations

from typing import Dict, List, Optional


class KnowledgeBase:
    """
    Central knowledge repository for the AI Investigation Agent.
    """

    def __init__(self):
        self.documents: List[Dict] = []
        self.metadata: List[Dict] = []

    def add_document(
        self,
        content: str,
        source: str,
        category: str,
        metadata: Optional[Dict] = None,
    ) -> int:
        """
        Add a document to the knowledge base.
        """

        document = {
            "id": len(self.documents),
            "content": content,
            "source": source,
            "category": category,
        }

        self.documents.append(document)
        self.metadata.append(metadata or {})

        return document["id"]

    def get_document(self, document_id: int) -> Optional[Dict]:
        """
        Retrieve a document by ID.
        """

        if 0 <= document_id < len(self.documents):
            return {
                **self.documents[document_id],
                "metadata": self.metadata[document_id],
            }

        return None

    def all_documents(self) -> List[Dict]:
        """
        Return all stored documents.
        """

        results = []

        for index, document in enumerate(self.documents):
            results.append(
                {
                    **document,
                    "metadata": self.metadata[index],
                }
            )

        return results

    def count(self) -> int:
        """
        Number of indexed documents.
        """

        return len(self.documents)

    def clear(self):
        """
        Remove all documents.
        """

        self.documents.clear()
        self.metadata.clear()
