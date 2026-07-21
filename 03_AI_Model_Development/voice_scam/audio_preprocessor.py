"""
RakshakAI v2
Voice Scam Detection
Audio Preprocessor
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import librosa
import numpy as np
import soundfile as sf


class AudioPreprocessor:
    """
    Handles preprocessing of audio before feature extraction.
    """

    def __init__(
        self,
        target_sample_rate: int = 16000,
        mono: bool = True,
        normalize: bool = True,
    ):
        self.target_sample_rate = target_sample_rate
        self.mono = mono
        self.normalize_audio = normalize

    def load_audio(self, audio_path: str):
        """
        Load audio from disk.
        """

        audio, sample_rate = librosa.load(
            audio_path,
            sr=self.target_sample_rate,
            mono=self.mono,
        )

        if self.normalize_audio:
            audio = self.normalize(audio)

        return audio, sample_rate

    def preprocess(self, audio_path: str):
        """
        Complete preprocessing pipeline.
        """

        audio, sample_rate = self.load_audio(audio_path)

        audio = self.remove_dc_offset(audio)
        audio = self.trim_silence(audio)

        if self.normalize_audio:
            audio = self.normalize(audio)

        return audio, sample_rate

    def trim_silence(self, audio: np.ndarray):
        """
        Remove leading and trailing silence.
        """

        trimmed, _ = librosa.effects.trim(audio)
        return trimmed

    def normalize(self, audio: np.ndarray):
        """
        Normalize audio amplitude.
        """

        peak = np.max(np.abs(audio))

        if peak == 0:
            return audio

        return audio / peak

    def remove_dc_offset(self, audio: np.ndarray):
        """
        Remove DC offset.
        """

        return audio - np.mean(audio)

    def resample(
        self,
        audio: np.ndarray,
        original_sr: int,
        target_sr: Optional[int] = None,
    ):
        """
        Resample audio.
        """

        target_sr = target_sr or self.target_sample_rate

        if original_sr == target_sr:
            return audio

        return librosa.resample(
            audio,
            orig_sr=original_sr,
            target_sr=target_sr,
        )

    def save_audio(
        self,
        output_path: str,
        audio: np.ndarray,
        sample_rate: Optional[int] = None,
    ):
        """
        Save processed audio.
        """

        sample_rate = sample_rate or self.target_sample_rate

        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        sf.write(
            output_path,
            audio,
            sample_rate,
        )

    def duration(self, audio: np.ndarray):
        """
        Audio duration in seconds.
        """

        return len(audio) / self.target_sample_rate

    def validate_audio(self, audio: np.ndarray):
        """
        Basic validation.
        """

        if audio is None:
            return False

        if len(audio) == 0:
            return False

        return True

    def preprocess_and_save(
        self,
        input_path: str,
        output_path: str,
    ):
        """
        Preprocess audio and save it.
        """

        audio, sample_rate = self.preprocess(input_path)

        self.save_audio(
            output_path,
            audio,
            sample_rate,
        )

        return output_path
