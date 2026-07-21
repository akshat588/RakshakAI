"""
RakshakAI v2
Case Manager

High-level interface for investigation case management.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .history_manager import history_manager


class CaseManager:
    """
    Central case management service.
    """

    def __init__(self) -> None:

        self.history = history_manager

    # ==========================================================
    # Create / Update Case
    # ==========================================================

    def save_case(
        self,
        case: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.history.save(case)

    # ==========================================================
    # Retrieve Case
    # ==========================================================

    def get_case(
        self,
        case_id: str,
    ) -> Optional[Dict[str, Any]]:

        return self.history.get(case_id)

    # ==========================================================
    # Recent Cases
    # ==========================================================

    def recent_cases(
        self,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:

        return self.history.list(limit=limit)

    # ==========================================================
    # Delete Case
    # ==========================================================

    def delete_case(
        self,
        case_id: str,
    ) -> bool:

        return self.history.delete(case_id)

    # ==========================================================
    # Case Count
    # ==========================================================

    def total_cases(self) -> int:

        return self.history.count()

    # ==========================================================
    # Clear All Cases
    # ==========================================================

    def clear_cases(self) -> None:

        self.history.clear()


case_manager = CaseManager()
