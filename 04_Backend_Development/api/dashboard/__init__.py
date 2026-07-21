"""
RakshakAI v2
Dashboard Module
"""

from .statistics_engine import StatisticsEngine, statistics_engine
from .threat_metrics import ThreatMetrics, threat_metrics
from .activity_feed import ActivityFeed, activity_feed
from .trend_analyzer import TrendAnalyzer, trend_analyzer
from .risk_distribution import RiskDistribution, risk_distribution
from .recent_investigations import (
    RecentInvestigations,
    recent_investigations,
)
from .dashboard_formatter import (
    DashboardFormatter,
    dashboard_formatter,
)
from .dashboard_service import (
    DashboardService,
    dashboard_service,
)

__all__ = [
    "StatisticsEngine",
    "statistics_engine",
    "ThreatMetrics",
    "threat_metrics",
    "ActivityFeed",
    "activity_feed",
    "TrendAnalyzer",
    "trend_analyzer",
    "RiskDistribution",
    "risk_distribution",
    "RecentInvestigations",
    "recent_investigations",
    "DashboardFormatter",
    "dashboard_formatter",
    "DashboardService",
    "dashboard_service",
]
