"""
===============================================================================
RakshakAI Model Loader
===============================================================================
"""

import joblib

from config import NLP_MODEL_DIR

MODELS = {}


def load_model(name):

    if name in MODELS:
        return MODELS[name]

    model = joblib.load(NLP_MODEL_DIR / f"{name}.pkl")

    MODELS[name] = model

    return model
