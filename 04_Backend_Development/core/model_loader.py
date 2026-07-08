"""
===============================================================================
RakshakAI Model Loader
===============================================================================
"""

import torch


def load_torch_model(model_path, model):

    checkpoint = torch.load(
        model_path,
        map_location=torch.device("cpu"),
    )

    model.load_state_dict(checkpoint["model_state_dict"])

    model.eval()

    return model


import joblib
from config import NLP_MODEL_DIR

MODELS = {}
VECTORIZERS = {}


def load_model(model_name):

    if model_name not in MODELS:
        MODELS[model_name] = joblib.load(NLP_MODEL_DIR / f"{model_name}.pkl")

    return MODELS[model_name]


def load_vectorizer(name):
    if name in MODELS:
        return MODELS[name]

    vectorizer = joblib.load(NLP_MODEL_DIR / f"{name}.pkl")

    MODELS[name] = vectorizer

    return vectorizer


def load_vectorizer(vectorizer_name):

    if vectorizer_name not in VECTORIZERS:
        VECTORIZERS[vectorizer_name] = joblib.load(
            NLP_MODEL_DIR / f"{vectorizer_name}.pkl"
        )

    return VECTORIZERS[vectorizer_name]


def load_preprocessor(name):

    if name in MODELS:
        return MODELS[name]

    preprocessor = joblib.load(NLP_MODEL_DIR / f"{name}.pkl")

    MODELS[name] = preprocessor

    return preprocessor
