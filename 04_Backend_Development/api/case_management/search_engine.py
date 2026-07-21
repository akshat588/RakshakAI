"""
RakshakAI v2
Case Search Engine

Provides search capabilities across stored investigation cases.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .investigation_store import investigation_store


class SearchEngine:
    """
    Search engine for investigation cases.
    """

    def __init__(self) -> None:

        self.store = investigation_store

    # ==========================================================
    # Search
    # ==========================================================

    def search(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:

        query = query.strip().lower()

        if not query:
            return []

        results: List[Dict[str, Any]] = []

        for case in self.store.all():

            searchable = " ".join(str(value).lower() for value in case.values())

            if query in searchable:
                results.append(case)

        return results

    # ==========================================================
    # Search by Severity
    # ==========================================================

    def by_severity(
        self,
        severity: str,
    ) -> List[Dict[str, Any]]:

        severity = severity.lower()

        return [
            case
            for case in self.store.all()
            if str(
                case.get(
                    "severity",
                    "",
                )
            ).lower()
            == severity
        ]

    # ==========================================================
    # Search by Investigation Type
    # ==========================================================

    def by_type(
        self,
        investigation_type: str,
    ) -> List[Dict[str, Any]]:

        investigation_type = investigation_type.lower()

        return [
            case
            for case in self.store.all()
            if str(
                case.get(
                    "detected_type",
                    "",
                )
            ).lower()
            == investigation_type
        ]


search_engine = SearchEngine()
