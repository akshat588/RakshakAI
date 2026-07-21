"""
RakshakAI v2
Voice Scam Detection
Model Loader
"""

from __future__ import annotations

import os
import joblib
from pathlib import Path
from typing import Any, Dict, Optional


class VoiceModelLoader:
    """
    Loads and manages all models required by the Voice Scam pipeline.
    """

    def __init__(self, model_directory: str):
        self.model_directory = Path(model_directory)

        self.models: Dict[str, Any] = {}

        self.model_files = {
            "voice_classifier": "voice_classifier.pkl",
            "acoustic_classifier": "acoustic_classifier.pkl",
            "transcript_classifier": "transcript_classifier.pkl",
            "feature_scaler": "feature_scaler.pkl",
            "label_encoder": "label_encoder.pkl",
        }

    def load_all(self) -> Dict[str, Any]:
        """
        Load all available models.
        """

        for model_name, filename in self.model_files.items():
            self.models[model_name] = self._load_model(filename)

        return self.models

    def get(self, model_name: str) -> Optional[Any]:
        """
        Retrieve loaded model.
        """

        return self.models.get(model_name)

    def is_loaded(self, model_name: str) -> bool:
        """
        Check whether a model is loaded.
        """

        return model_name in self.models and self.models[model_name] is not None

    def reload(self) -> Dict[str, Any]:
        """
        Reload every model.
        """

        self.models.clear()
        return self.load_all()

    def available_models(self) -> Dict[str, bool]:
        """
        Returns availability of model files.
        """

        result = {}

        for model_name, filename in self.model_files.items():
            result[model_name] = (self.model_directory / filename).exists()

        return result

    def _load_model(self, filename: str):
        """
        Internal loader.
        """

        model_path = self.model_directory / filename

        if not model_path.exists():
            return None

        try:
            return joblib.load(model_path)

        except Exception:
            return None

    def model_info(self) -> Dict[str, Dict]:
        """
        Returns model loading status.
        """

        info = {}

        for model_name, filename in self.model_files.items():
            path = self.model_directory / filename

            info[model_name] = {
                "filename": filename,
                "exists": path.exists(),
                "loaded": self.is_loaded(model_name),
                "path": str(path),
            }

        return info

    def unload(self):
        """
        Release loaded models.
        """

        self.models.clear()

    def __len__(self):
        return len(self.models)

    def __contains__(self, item):
        return item in self.models

    def __repr__(self):
        return (
            f"VoiceModelLoader("
            f"directory='{self.model_directory}', "
            f"loaded_models={len(self.models)})"
        )
