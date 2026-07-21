"""
RakshakAI v2
Voice Scam Detection
Voice Service
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ai_models.voice_scam.audio_preprocessor import AudioPreprocessor
from ai_models.voice_scam.audio_feature_extractor import AudioFeatureExtractor
from ai_models.voice_scam.speech_to_text import SpeechToText
from ai_models.voice_scam.transcript_analyzer import TranscriptAnalyzer
from ai_models.voice_scam.voice_classifier import VoiceClassifier
from ai_models.voice_scam.voice_pipeline import VoicePipeline
from ai_models.voice_scam.result_builder import VoiceResultBuilder
from ai_models.voice_scam.model_loader import VoiceModelLoader


class VoiceService:
    """
    Backend service for Voice Scam Detection.
    """

    def __init__(
        self,
        model_directory: str,
        investigation_engine: Optional[Any] = None,
    ):
        self.model_loader = VoiceModelLoader(model_directory)
        models = self.model_loader.load_all()

        self.preprocessor = AudioPreprocessor()
        self.feature_extractor = AudioFeatureExtractor()

        self.stt = SpeechToText()

        self.transcript_analyzer = TranscriptAnalyzer(
            investigation_engine=investigation_engine,
        )

        self.voice_classifier = VoiceClassifier(
            classifier=models.get("voice_classifier"),
            scaler=models.get("feature_scaler"),
            label_encoder=models.get("label_encoder"),
        )

        self.pipeline = VoicePipeline(
            stt=self.stt,
            transcript_analyzer=self.transcript_analyzer,
            voice_classifier=self.voice_classifier,
            preprocessor=self.preprocessor,
            feature_extractor=self.feature_extractor,
        )

        self.result_builder = VoiceResultBuilder()

    def analyze(
        self,
        audio_path: str,
        language: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze a voice recording.
        """

        pipeline_result = self.pipeline.analyze(
            audio_path=audio_path,
            language=language,
            metadata=metadata,
        )

        return self.result_builder.build(
            transcript_result=pipeline_result["transcript"],
            acoustic_result=pipeline_result["acoustic_analysis"],
            investigation_result=pipeline_result["investigation"],
        )

    def health(self) -> Dict[str, Any]:
        """
        Service health.
        """

        return {
            "service": "VoiceService",
            "status": "ready",
            "models": self.model_loader.model_info(),
        }
