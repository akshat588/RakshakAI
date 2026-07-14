"""
==========================================================
RakshakAI v2
Investigation Intelligence Engine
==========================================================
"""

from __future__ import annotations

from typing import Dict

from api.assistant_core.ioc_engine import IOCEngine
from api.assistant_core.mitre_mapper import MITREMapper
from api.assistant_core.threat_explainer import ThreatExplainer
from api.assistant_core.recommendation_engine import RecommendationEngine
from api.assistant_core.executive_summary import ExecutiveSummary


class InvestigationIntelligence:

    def __init__(self):

        self.ioc = IOCEngine()

        self.mitre = MITREMapper()

        self.explainer = ThreatExplainer()

        self.recommendation = RecommendationEngine()

        self.summary = ExecutiveSummary()

    def enrich(self, report: Dict) -> Dict:

        report["ioc_analysis"] = self.ioc.analyze(report)

        report["mitre_attack"] = self.mitre.map(report)

        report["threat_explanation"] = self.explainer.explain(report)

        report["recommended_actions"] = self.recommendation.generate(report)

        report["executive_summary"] = self.summary.generate(report)

        return report


intelligence = InvestigationIntelligence()
