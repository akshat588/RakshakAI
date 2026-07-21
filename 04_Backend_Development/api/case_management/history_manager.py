"""
RakshakAI v2
History Manager

Manages investigation history using the central investigation store.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .investigation_store import investigation_store


class HistoryManager:
    """
    Investigation history manager.
    """

    def __init__(self) -> None:

        self.store = investigation_store

    # ==========================================================
    # Save Investigation
    # ==========================================================

    def save(
        self,
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.store.save(investigation)

    # ==========================================================
    # Get Investigation
    # ==========================================================

    def get(
        self,
        case_id: str,
    ) -> Optional[Dict[str, Any]]:

        return self.store.get(case_id)

    # ==========================================================
    # List History
    # ==========================================================

    def list(
        self,
        limit: int | None = None,
    ) -> List[Dict[str, Any]]:

        investigations = self.store.all()

        investigations.sort(
            key=lambda item: item.get("created_at", ""),
            reverse=True,
        )

        if limit is not None:
            return investigations[:limit]

        return investigations

    # ==========================================================
    # Delete Investigation
    # ==========================================================

    def delete(
        self,
        case_id: str,
    ) -> bool:

        return self.store.delete(case_id)

    # ==========================================================
    # Statistics
    # ==========================================================

    def count(self) -> int:

        return self.store.count()

    # ==========================================================
    # Clear History
    # ==========================================================

    def clear(self) -> None:

        self.store.clear()


history_manager = HistoryManager()
