"""
RakshakAI v2
Voice Scam Detection
Voice Classifier
"""

from __future__ import annotations

from typing import Dict, Any

import numpy as np


class VoiceClassifier:
    """
    Performs acoustic voice classification using the trained model.
    """

    def __init__(
        self,
        classifier=None,
        scaler=None,
        label_encoder=None,
    ):
        self.classifier = classifier
        self.scaler = scaler
        self.label_encoder = label_encoder

    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Predict voice scam probability.
        """

        if features.ndim == 1:
            features = features.reshape(1, -1)

        processed_features = self._preprocess(features)

        if self.classifier is None:
            return self._fallback_result()

        prediction = self.classifier.predict(processed_features)[0]

        confidence = self._confidence(processed_features)

        label = self._decode_label(prediction)

        return {
            "prediction": label,
            "confidence": confidence,
            "model": "voice_classifier",
        }

    def _preprocess(self, features: np.ndarray) -> np.ndarray:
        """
        Apply feature scaling if available.
        """

        if self.scaler is None:
            return features

        return self.scaler.transform(features)

    def _confidence(self, features: np.ndarray) -> float:
        """
        Calculate confidence score.
        """

        if hasattr(self.classifier, "predict_proba"):
            probabilities = self.classifier.predict_proba(features)[0]
            return round(float(np.max(probabilities) * 100), 2)

        return 50.0

    def _decode_label(self, prediction):
        """
        Decode prediction label.
        """

        if self.label_encoder is None:
            return str(prediction)

        try:
            return self.label_encoder.inverse_transform([prediction])[0]
        except Exception:
            return str(prediction)

    @staticmethod
    def _fallback_result() -> Dict[str, Any]:
        """
        Returned when model is unavailable.
        """

        return {
            "prediction": "unknown",
            "confidence": 0.0,
            "model": "voice_classifier",
        }
