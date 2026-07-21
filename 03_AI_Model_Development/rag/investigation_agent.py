"""
RakshakAI v2
AI Investigation Agent
Investigation Agent
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .context_builder import ContextBuilder
from .knowledge_base import KnowledgeBase
from .retrieval_engine import RetrievalEngine


class InvestigationAgent:
    """
    Central RAG Investigation Agent.
    """

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        retrieval_engine: RetrievalEngine,
        context_builder: ContextBuilder,
        reasoning_pipeline: Optional[Any] = None,
    ):
        self.knowledge_base = knowledge_base
        self.retrieval_engine = retrieval_engine
        self.context_builder = context_builder
        self.reasoning_pipeline = reasoning_pipeline

    def investigate(
        self,
        query: str,
        investigation_context: Optional[Dict] = None,
        top_k: int = 5,
    ) -> Dict:
        """
        Perform a RAG investigation.
        """

        retrieved_documents = self.retrieval_engine.retrieve(
            query=query,
            top_k=top_k,
        )

        context = self.context_builder.build(
            query=query,
            retrieved_documents=retrieved_documents,
            investigation_context=investigation_context,
        )

        if self.reasoning_pipeline is None:
            reasoning = self._fallback_reasoning(context)
        else:
            reasoning = self.reasoning_pipeline.run(context)

        return {
            "query": query,
            "context": context,
            "reasoning": reasoning,
            "sources": self.context_builder.summarize_sources(retrieved_documents),
        }

    def _fallback_reasoning(self, context: Dict) -> Dict:
        """
        Placeholder reasoning until the dedicated reasoning
        pipeline is integrated.
        """

        return {
            "status": "pending",
            "summary": ("Reasoning pipeline has not been integrated."),
            "document_count": context["document_count"],
            "confidence": 0.0,
        }

    def health(self) -> Dict:
        """
        Health information.
        """

        return {
            "component": "InvestigationAgent",
            "knowledge_base_documents": self.knowledge_base.count(),
            "reasoning_pipeline_loaded": self.reasoning_pipeline is not None,
        }
