"""
RakshakAI v2
Voice Scam Detection
Speech-to-Text
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

import whisper


class SpeechToText:
    """
    Wrapper for Whisper Speech-to-Text.
    """

    def __init__(
        self,
        model_name: str = "base",
        device: Optional[str] = None,
    ):
        self.model_name = model_name
        self.device = device
        self.model = whisper.load_model(model_name, device=device)

    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
    ) -> Dict:
        """
        Transcribe an audio file.
        """

        result = self.model.transcribe(
            audio_path,
            language=language,
            fp16=False,
        )

        return {
            "text": result.get("text", "").strip(),
            "language": result.get("language"),
            "segments": result.get("segments", []),
        }

    def detect_language(self, audio_path: str) -> Optional[str]:
        """
        Detect the language of an audio file.
        """

        result = self.model.transcribe(
            audio_path,
            fp16=False,
        )

        return result.get("language")

    def transcript_only(
        self,
        audio_path: str,
        language: Optional[str] = None,
    ) -> str:
        """
        Return only transcript text.
        """

        return self.transcribe(
            audio_path,
            language=language,
        )["text"]

    def save_transcript(
        self,
        transcript: str,
        output_path: str,
    ) -> str:
        """
        Save transcript to a text file.
        """

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        output.write_text(
            transcript,
            encoding="utf-8",
        )

        return str(output)

    def supported_model(self) -> str:
        """
        Return currently loaded Whisper model.
        """

        return self.model_name
