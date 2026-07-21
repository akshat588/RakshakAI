"""
RakshakAI v2
Voice Scam Detection
Transcript Analyzer
"""

from __future__ import annotations

from typing import Any, Dict, Optional


class TranscriptAnalyzer:
    """
    Uses the existing Universal Investigation Engine to analyze
    transcribed speech instead of creating a standalone detector.
    """

    def __init__(
        self,
        investigation_engine: Optional[Any] = None,
    ):
        self.investigation_engine = investigation_engine

    def analyze(
        self,
        transcript: str,
        metadata: Optional[Dict] = None,
    ) -> Dict:
        """
        Analyze transcript using the Universal Investigation Engine.
        """

        metadata = metadata or {}

        if self.investigation_engine is None:
            return self._fallback_result(transcript)

        return self.investigation_engine.investigate(
            input_data=transcript,
            input_type="voice_transcript",
            metadata=metadata,
        )

    def _fallback_result(self, transcript: str) -> Dict:
        """
        Fallback result when the investigation engine
        has not yet been injected.
        """

        return {
            "status": "pending",
            "input_type": "voice_transcript",
            "transcript": transcript,
            "message": ("Universal Investigation Engine is not available."),
            "confidence": 0.0,
            "risk_score": 0.0,
            "risk_level": "UNKNOWN",
            "prediction": "unknown",
            "findings": [],
            "recommendations": [],
        }

    def health(self) -> Dict:
        """
        Health status.
        """

        return {
            "component": "TranscriptAnalyzer",
            "investigation_engine_loaded": self.investigation_engine is not None,
        }
