"""
RakshakAI v2
AI Investigation Agent Blueprint
"""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from ai_models.rag.knowledge_base import KnowledgeBase
from ai_models.rag.retrieval_engine import RetrievalEngine
from ai_models.rag.context_builder import ContextBuilder
from ai_models.rag.reasoning_pipeline import ReasoningPipeline
from ai_models.rag.investigation_agent import InvestigationAgent
from ai_models.rag.explainable_ai import ExplainableAI

ai_agent_bp = Blueprint("ai_agent", __name__)

_knowledge_base = KnowledgeBase()
_retrieval_engine = RetrievalEngine(_knowledge_base)
_context_builder = ContextBuilder()
_reasoning_pipeline = ReasoningPipeline()
_explainable_ai = ExplainableAI()

_agent = InvestigationAgent(
    knowledge_base=_knowledge_base,
    retrieval_engine=_retrieval_engine,
    context_builder=_context_builder,
    reasoning_pipeline=_reasoning_pipeline,
)


@ai_agent_bp.route("/api/agent/query", methods=["POST"])
def query_agent():
    """
    Query the AI Investigation Agent.
    """

    data = request.get_json(silent=True) or {}

    query = data.get("query", "").strip()

    if not query:
        return jsonify({"success": False, "message": "Query is required."}), 400

    investigation_context = data.get(
        "investigation_context",
        {},
    )

    result = _agent.investigate(
        query=query,
        investigation_context=investigation_context,
    )

    explanation = _explainable_ai.build_explanation(result["reasoning"])

    return jsonify(
        {
            "success": True,
            "result": result,
            "explanation": explanation,
        }
    )


@ai_agent_bp.route("/api/agent/knowledge", methods=["POST"])
def add_knowledge():
    """
    Add a document to the knowledge base.
    """

    data = request.get_json(silent=True) or {}

    content = data.get("content", "").strip()

    if not content:
        return jsonify({"success": False, "message": "Document content is required."}), 400

    document_id = _knowledge_base.add_document(
        content=content,
        source=data.get("source", "manual"),
        category=data.get("category", "general"),
        metadata=data.get("metadata", {}),
    )

    _retrieval_engine.build_index()

    return jsonify(
        {
            "success": True,
            "document_id": document_id,
        }
    )


@ai_agent_bp.route("/api/agent/health", methods=["GET"])
def health():
    """
    AI Agent health endpoint.
    """

    return jsonify(
        {
            "status": "ready",
            "knowledge_base": _knowledge_base.count(),
            "retrieval": _retrieval_engine.health(),
            "reasoning": _reasoning_pipeline.health(),
            "explainable_ai": _explainable_ai.health(),
        }
    )
