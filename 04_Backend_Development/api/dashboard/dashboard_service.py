"""
RakshakAI v2
Dashboard Service

Primary service used by the API layer to generate dashboard data.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .dashboard_formatter import dashboard_formatter


class DashboardService:
    """
    Dashboard service facade.
    """

    def __init__(self) -> None:

        self.formatter = dashboard_formatter

    # ==========================================================
    # Dashboard
    # ==========================================================

    def get_dashboard(
        self,
        investigations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        return self.formatter.build(investigations)

    # ==========================================================
    # Empty Dashboard
    # ==========================================================

    def empty_dashboard(self) -> Dict[str, Any]:

        return self.formatter.build([])


dashboard_service = DashboardService()
