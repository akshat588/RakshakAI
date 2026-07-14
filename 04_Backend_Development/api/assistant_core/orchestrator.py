"""
==========================================================
RakshakAI v2
Universal Investigation Orchestrator
==========================================================
"""

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Any

from api.assistant_core.detector import UniversalInputDetector
from api.assistant_core.intelligence import intelligence


class InvestigationOrchestrator:
    """
    Central orchestration engine.

    Responsibilities
    ----------------
    1. Detect the incoming content.
    2. Execute one or more analyzers.
    3. Merge all evidence.
    4. Calculate final threat score.
    5. Return one unified investigation report.
    """

    def __init__(self):

        self.detector = UniversalInputDetector()

        self.engines: Dict[str, Any] = {}

        self.execution_order: List[str] = [
            "email",
            "url",
            "sms",
            "whatsapp",
            "upi",
            "fake_job",
            "social_engineering",
            "qr",
            "deepfake",
            "voice",
        ]

    # =====================================================
    # Registration
    # =====================================================

    def register(self, name: str, analyzer):

        self.engines[name] = analyzer

    def has_engine(self, name: str) -> bool:

        return name in self.engines

    def available_engines(self) -> List[str]:

        return list(self.engines.keys())

        # =====================================================

    # Investigation Entry
    # =====================================================

    def investigate(self, content: str) -> Dict:

        detected_type = self.detector.detect(content)

        report = {
            "detected_type": detected_type,
            "executed_engines": [],
            "results": [],
            "evidence": [],
            "recommendations": [],
            "timeline": [],
            "iocs": [],
            "overall_risk": "SAFE",
            "overall_score": 0,
            "confidence": 0,
        }

        engines = self.select_engines(detected_type, content)

        for engine in engines:

            if not self.has_engine(engine):

                continue

            analyzer = self.engines[engine]

            try:

                result = analyzer(content)

            except Exception as exc:

                report["timeline"].append(f"{engine} failed: {exc}")

                continue

            report["executed_engines"].append(engine)

            report["results"].append(result)

        return self.merge_results(report)

        # =====================================================

    # Engine Selection
    # =====================================================

    def select_engines(self, detected_type: str, content: str) -> List[str]:

        engines = []

        # Primary analyzer

        if detected_type in self.execution_order:

            engines.append(detected_type)

        text = content.lower()

        # URL detection

        if "http://" in text or "https://" in text or "www." in text:

            if "url" not in engines:

                engines.append("url")

        # Email detection

        if "@" in text and "." in text:

            if "email" not in engines:

                engines.append("email")

        # UPI detection

        upi_keywords = ["@ybl", "@ibl", "@okaxis", "@okhdfcbank", "@oksbi", "@paytm", "@axl"]

        if any(keyword in text for keyword in upi_keywords):

            if "upi" not in engines:

                engines.append("upi")

        # Social Engineering is always useful
        # for text investigations

        if len(text) > 15:

            if "social_engineering" not in engines:

                engines.append("social_engineering")

        # Remove duplicates while preserving order

        unique = []

        for engine in engines:

            if engine not in unique:

                unique.append(engine)

        return unique

        # =====================================================

    # Merge Results
    # =====================================================

    def merge_results(self, report: Dict) -> Dict:

        if not report["results"]:

            report["overall_risk"] = "UNKNOWN"

            report["overall_score"] = 0

            report["confidence"] = 0

            return report

        scores = []

        confidences = []

        risk_priority = {"SAFE": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}

        highest_risk = "SAFE"

        for result in report["results"]:

            score = float(result.get("risk_score", 0))

            confidence = float(result.get("confidence", 0))

            scores.append(score)

            confidences.append(confidence)

            risk = str(result.get("risk", "SAFE")).upper()

            if risk_priority.get(risk, 0) > risk_priority.get(highest_risk, 0):

                highest_risk = risk

            report["evidence"].extend(result.get("evidence", []))

            report["recommendations"].extend(result.get("recommendations", []))

            report["timeline"].extend(result.get("timeline", []))

            report["iocs"].extend(result.get("iocs", []))

        report["overall_score"] = round(sum(scores) / len(scores), 2)

        report["confidence"] = round(sum(confidences) / len(confidences), 2)

        report["overall_risk"] = highest_risk

        return self.remove_duplicates(report)

        # =====================================================

    # Remove Duplicate Evidence
    # =====================================================

    def remove_duplicates(self, report: Dict) -> Dict:

        report["evidence"] = list(dict.fromkeys(report["evidence"]))

        report["recommendations"] = list(dict.fromkeys(report["recommendations"]))

        report["timeline"] = list(dict.fromkeys(report["timeline"]))

        report["iocs"] = list(dict.fromkeys(report["iocs"]))

        report["executed_engines"] = list(dict.fromkeys(report["executed_engines"]))

        report["summary"] = self.build_summary(report)

        return report

    # =====================================================
    # Executive Summary
    # =====================================================

    def build_summary(self, report: Dict) -> str:

        engine_count = len(report["executed_engines"])

        evidence_count = len(report["evidence"])

        return (
            f"RakshakAI investigated the submitted content "
            f"using {engine_count} analyzer(s). "
            f"{evidence_count} evidence item(s) and "
            f"{len(report['iocs'])} indicator(s) of compromise "
            f"were identified. "
            f"The investigation concluded with a "
            f"{report['overall_risk']} risk level "
            f"and an overall threat score of "
            f"{report['overall_score']}/100."
        )

        # =====================================================

    # Threat Score Normalization
    # =====================================================

    def normalize_score(self, score: float) -> float:

        score = max(0, min(100, float(score)))

        return round(score, 2)

    # =====================================================
    # Risk Mapping
    # =====================================================

    def score_to_risk(self, score: float) -> str:

        score = self.normalize_score(score)

        if score >= 90:

            return "CRITICAL"

        if score >= 70:

            return "HIGH"

        if score >= 40:

            return "MEDIUM"

        if score >= 15:

            return "LOW"

        return "SAFE"

    # =====================================================
    # Final Risk Evaluation
    # =====================================================

    def finalize_risk(self, report: Dict) -> Dict:

        calculated_risk = self.score_to_risk(report["overall_score"])

        priority = {"SAFE": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}

        if priority[calculated_risk] > priority[report["overall_risk"]]:

            report["overall_risk"] = calculated_risk

        report["overall_score"] = self.normalize_score(report["overall_score"])

        report["confidence"] = self.normalize_score(report["confidence"])

        return report

        # =====================================================

    # Investigation Metadata
    # =====================================================

    def build_metadata(self, report: Dict) -> Dict:

        report["metadata"] = {
            "engines_executed": len(report["executed_engines"]),
            "evidence_found": len(report["evidence"]),
            "recommendations_generated": len(report["recommendations"]),
            "timeline_events": len(report["timeline"]),
            "iocs_detected": len(report["iocs"]),
        }

        return report

    # =====================================================
    # Investigation Verdict
    # =====================================================

    def build_verdict(self, report: Dict) -> Dict:

        risk = report["overall_risk"]

        verdict_map = {
            "SAFE": "No immediate threat detected.",
            "LOW": "Minor suspicious indicators detected.",
            "MEDIUM": "Potential threat requires verification.",
            "HIGH": "High probability of cyber fraud.",
            "CRITICAL": "Critical cyber threat detected. Immediate action required.",
        }

        report["verdict"] = verdict_map.get(risk, "Investigation completed.")

        return report

    # =====================================================
    # Investigation Statistics
    # =====================================================

    def build_statistics(self, report: Dict) -> Dict:

        report["statistics"] = {
            "successful_engines": len(report["results"]),
            "failed_engines": len(report["executed_engines"]) - len(report["results"]),
            "overall_score": report["overall_score"],
            "overall_confidence": report["confidence"],
        }

        return report

        # =====================================================

    # Investigation Timeline
    # =====================================================

    def enrich_timeline(self, report: Dict) -> Dict:

        timeline = [
            "Investigation initiated.",
            f"Input detected as '{report['detected_type']}'.",
            f"Executed {len(report['executed_engines'])} analyzer(s).",
            f"Collected {len(report['evidence'])} evidence item(s).",
            f"Detected {len(report['iocs'])} indicator(s) of compromise.",
            f"Final threat score: {report['overall_score']}.",
            f"Risk level determined as {report['overall_risk']}.",
        ]

        report["timeline"] = list(dict.fromkeys(timeline + report["timeline"]))

        return report

    # =====================================================
    # Investigation Timestamp
    # =====================================================

    def add_timestamp(self, report: Dict) -> Dict:

        from datetime import datetime

        report["timestamp"] = datetime.utcnow().isoformat()

        return report

    # =====================================================
    # Processing Information
    # =====================================================

    def add_processing_info(self, report: Dict) -> Dict:

        report["processing"] = {
            "framework": "RakshakAI Universal Investigation Engine",
            "version": "2.0",
            "pipeline": "Detection → Orchestration → Evidence Fusion → Risk Assessment",
            "mode": "Multi-Analyzer",
        }

        return report

        # =====================================================

    # Final Report Assembly
    # =====================================================

    def build_final_report(self, report: Dict) -> Dict:

        report = self.finalize_risk(report)

        report = self.build_metadata(report)

        report = self.build_verdict(report)

        report = self.build_statistics(report)

        report = self.enrich_timeline(report)

        report = self.add_timestamp(report)

        report = self.add_processing_info(report)

        report = intelligence.enrich(report)

        report["success"] = True

        return report

    # =====================================================
    # Public API
    # =====================================================

    def run(self, content: str) -> Dict:

        report = self.investigate(content)

        return self.build_final_report(report)

        # =====================================================

    # Reset
    # =====================================================

    def reset(self):

        self.engines.clear()

    # =====================================================
    # Debug
    # =====================================================

    def debug(self):

        return {
            "registered_engines": self.available_engines(),
            "execution_order": self.execution_order,
            "engine_count": len(self.engines),
        }


# ==========================================================
# Global Orchestrator Instance
# ==========================================================

orchestrator = InvestigationOrchestrator()
