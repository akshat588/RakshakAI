"""
RakshakAI v2
Voice Scam Detection
Result Builder
"""

from __future__ import annotations

from typing import Any, Dict


class VoiceResultBuilder:
    """
    Builds the final unified result for the Voice Scam Detection module.
    """

    def build(
        self,
        transcript_result: Dict[str, Any],
        acoustic_result: Dict[str, Any],
        investigation_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Merge all analysis results into a single response.
        """

        transcript_confidence = float(investigation_result.get("risk_score", 0.0))

        acoustic_confidence = float(acoustic_result.get("confidence", 0.0))

        final_score = round(
            (transcript_confidence + acoustic_confidence) / 2,
            2,
        )

        if final_score >= 90:
            risk = "CRITICAL"
        elif final_score >= 70:
            risk = "HIGH"
        elif final_score >= 40:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        prediction = "voice_scam" if final_score >= 50 else "genuine_voice"

        return {
            "detected_type": "voice",
            "analyzer": "voice_scam",
            "prediction": prediction,
            "risk": risk,
            "risk_score": final_score,
            "confidence": final_score,
            "language": transcript_result.get("language"),
            "transcript": transcript_result.get("text", ""),
            "segments": transcript_result.get("segments", []),
            "acoustic_analysis": acoustic_result,
            "investigation": investigation_result,
            "status": "completed",
        }
