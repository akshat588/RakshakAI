"""
RakshakAI v2
Voice Scam Detection
Voice Pipeline
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .audio_preprocessor import AudioPreprocessor
from .audio_feature_extractor import AudioFeatureExtractor
from .speech_to_text import SpeechToText
from .transcript_analyzer import TranscriptAnalyzer
from .voice_classifier import VoiceClassifier


class VoicePipeline:
    """
    End-to-end Voice Scam Detection pipeline.
    """

    def __init__(
        self,
        stt: SpeechToText,
        transcript_analyzer: TranscriptAnalyzer,
        voice_classifier: VoiceClassifier,
        preprocessor: Optional[AudioPreprocessor] = None,
        feature_extractor: Optional[AudioFeatureExtractor] = None,
    ):
        self.preprocessor = preprocessor or AudioPreprocessor()
        self.feature_extractor = feature_extractor or AudioFeatureExtractor()

        self.stt = stt
        self.transcript_analyzer = transcript_analyzer
        self.voice_classifier = voice_classifier

    def analyze(
        self,
        audio_path: str,
        language: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Complete analysis pipeline.
        """

        metadata = metadata or {}

        audio, sample_rate = self.preprocessor.preprocess(audio_path)

        features = self.feature_extractor.extract_features(audio)

        acoustic_result = self.voice_classifier.predict(features)

        transcript_result = self.stt.transcribe(
            audio_path=audio_path,
            language=language,
        )

        investigation_result = self.transcript_analyzer.analyze(
            transcript=transcript_result["text"],
            metadata=metadata,
        )

        return {
            "audio": {
                "sample_rate": sample_rate,
                "duration": round(
                    self.preprocessor.duration(audio),
                    2,
                ),
            },
            "transcript": transcript_result,
            "acoustic_analysis": acoustic_result,
            "investigation": investigation_result,
        }

    def health(self) -> Dict[str, Any]:
        """
        Pipeline health.
        """

        return {
            "pipeline": "VoicePipeline",
            "status": "ready",
        }
