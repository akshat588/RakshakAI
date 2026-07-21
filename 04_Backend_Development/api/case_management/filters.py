"""
RakshakAI v2
Case Filters

Provides filtering utilities for investigation cases.
"""

from __future__ import annotations

from typing import Any, Dict, List


class CaseFilters:
    """
    Investigation filtering engine.
    """

    def __init__(self) -> None:
        pass

    # ==========================================================
    # Filter by Severity
    # ==========================================================

    def severity(
        self,
        investigations: List[Dict[str, Any]],
        severity: str,
    ) -> List[Dict[str, Any]]:

        severity = severity.lower()

        return [
            item for item in investigations if str(item.get("severity", "")).lower() == severity
        ]

    # ==========================================================
    # Filter by Type
    # ==========================================================

    def investigation_type(
        self,
        investigations: List[Dict[str, Any]],
        detected_type: str,
    ) -> List[Dict[str, Any]]:

        detected_type = detected_type.lower()

        return [
            item
            for item in investigations
            if str(
                item.get(
                    "detected_type",
                    "",
                )
            ).lower()
            == detected_type
        ]

    # ==========================================================
    # Filter by Prediction
    # ==========================================================

    def prediction(
        self,
        investigations: List[Dict[str, Any]],
        prediction: str,
    ) -> List[Dict[str, Any]]:

        prediction = prediction.lower()

        return [
            item
            for item in investigations
            if str(
                item.get(
                    "prediction",
                    "",
                )
            ).lower()
            == prediction
        ]


case_filters = CaseFilters()
