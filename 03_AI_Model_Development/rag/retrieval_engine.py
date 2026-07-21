"""
RakshakAI v2
AI Investigation Agent
Retrieval Engine
"""

from __future__ import annotations

from typing import Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .knowledge_base import KnowledgeBase


class RetrievalEngine:
    """
    Retrieves the most relevant knowledge base documents
    using TF-IDF similarity.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            lowercase=True,
        )
        self.document_matrix = None
        self.is_indexed = False

    def build_index(self):
        """
        Build or rebuild the search index.
        """

        documents = self.knowledge_base.all_documents()

        if not documents:
            self.document_matrix = None
            self.is_indexed = False
            return

        corpus = [doc["content"] for doc in documents]

        self.document_matrix = self.vectorizer.fit_transform(corpus)
        self.is_indexed = True

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict]:
        """
        Retrieve the most relevant documents.
        """

        if not self.is_indexed:
            self.build_index()

        if self.document_matrix is None:
            return []

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.document_matrix,
        )[0]

        ranked = sorted(
            enumerate(scores),
            key=lambda item: item[1],
            reverse=True,
        )

        results = []

        for index, score in ranked[:top_k]:
            document = self.knowledge_base.get_document(index)

            if document is None:
                continue

            results.append(
                {
                    "score": round(float(score), 4),
                    "document": document,
                }
            )

        return results

    def health(self) -> Dict:
        """
        Retrieval engine status.
        """

        return {
            "indexed": self.is_indexed,
            "documents": self.knowledge_base.count(),
        }
