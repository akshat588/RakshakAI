"""
RakshakAI v2
Dashboard Formatter

Combines all dashboard components into a unified response object.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .statistics_engine import statistics_engine
from .threat_metrics import threat_metrics
from .activity_feed import activity_feed
from .trend_analyzer import trend_analyzer
from .risk_distribution import risk_distribution
from .recent_investigations import recent_investigations


class DashboardFormatter:
    """
    Formats dashboard data.
    """

    def __init__(self) -> None:

        self.statistics_engine = statistics_engine
        self.threat_metrics = threat_metrics
        self.activity_feed = activity_feed
        self.trend_analyzer = trend_analyzer
        self.risk_distribution = risk_distribution
        self.recent_investigations = recent_investigations

    # ==========================================================
    # Build Dashboard
    # ==========================================================

    def build(
        self,
        investigations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        return {
            "statistics": self.statistics_engine.generate(investigations),
            "metrics": self.threat_metrics.generate(investigations),
            "activity_feed": self.activity_feed.generate(investigations),
            "trends": self.trend_analyzer.generate(investigations),
            "risk_distribution": self.risk_distribution.generate(investigations),
            "recent_investigations": self.recent_investigations.generate(investigations),
        }


dashboard_formatter = DashboardFormatter()
