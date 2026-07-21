"""
RakshakAI v2
Voice Scam Detection
Audio Feature Extractor
"""

from __future__ import annotations

import numpy as np
import librosa


class AudioFeatureExtractor:
    """
    Extracts acoustic features from audio for the Voice Scam Detection pipeline.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        n_mfcc: int = 40,
    ):
        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc

    def extract_features(self, audio: np.ndarray) -> np.ndarray:
        """
        Complete feature extraction pipeline.
        """

        feature_vector = []

        feature_vector.extend(self._mfcc(audio))
        feature_vector.extend(self._chroma(audio))
        feature_vector.extend(self._mel(audio))
        feature_vector.extend(self._spectral_centroid(audio))
        feature_vector.extend(self._spectral_bandwidth(audio))
        feature_vector.extend(self._spectral_rolloff(audio))
        feature_vector.extend(self._zero_crossing_rate(audio))
        feature_vector.extend(self._rms(audio))
        feature_vector.extend(self._pitch(audio))

        return np.asarray(feature_vector, dtype=np.float32)

    def _mfcc(self, audio):
        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=self.sample_rate,
            n_mfcc=self.n_mfcc,
        )
        return np.mean(mfcc, axis=1).tolist()

    def _chroma(self, audio):
        stft = np.abs(librosa.stft(audio))
        chroma = librosa.feature.chroma_stft(
            S=stft,
            sr=self.sample_rate,
        )
        return np.mean(chroma, axis=1).tolist()

    def _mel(self, audio):
        mel = librosa.feature.melspectrogram(
            y=audio,
            sr=self.sample_rate,
        )
        mel_db = librosa.power_to_db(mel)
        return np.mean(mel_db, axis=1).tolist()

    def _spectral_centroid(self, audio):
        feature = librosa.feature.spectral_centroid(
            y=audio,
            sr=self.sample_rate,
        )
        return [float(np.mean(feature))]

    def _spectral_bandwidth(self, audio):
        feature = librosa.feature.spectral_bandwidth(
            y=audio,
            sr=self.sample_rate,
        )
        return [float(np.mean(feature))]

    def _spectral_rolloff(self, audio):
        feature = librosa.feature.spectral_rolloff(
            y=audio,
            sr=self.sample_rate,
        )
        return [float(np.mean(feature))]

    def _zero_crossing_rate(self, audio):
        feature = librosa.feature.zero_crossing_rate(audio)
        return [float(np.mean(feature))]

    def _rms(self, audio):
        feature = librosa.feature.rms(y=audio)
        return [float(np.mean(feature))]

    def _pitch(self, audio):
        pitches, magnitudes = librosa.piptrack(
            y=audio,
            sr=self.sample_rate,
        )

        valid = pitches[magnitudes > np.median(magnitudes)]

        if len(valid) == 0:
            return [0.0]

        return [float(np.mean(valid))]

    def feature_dimension(self, audio: np.ndarray) -> int:
        """
        Returns extracted feature dimension.
        """

        return len(self.extract_features(audio))
