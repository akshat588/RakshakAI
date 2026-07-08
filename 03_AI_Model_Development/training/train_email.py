"""
===============================================================================
RakshakAI - Email Phishing Model Trainer
===============================================================================
"""

from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split

from config.config import (
    RANDOM_STATE,
    TEST_SIZE,
)

from preprocessing.text_preprocessor import TextPreprocessor
from feature_engineering.tfidf import TFIDFEngine
from training.base_trainer import BaseTrainer

# =============================================================================
# DATASET PATH
# =============================================================================

from config.paths import (
    EMAIL_DATASET,
    NLP_MODELS,
)

DATASET_PATH = EMAIL_DATASET / "Phishing_Email.csv"

MODEL_PATH = NLP_MODELS / "email_detector.pkl"

VECTORIZER_PATH = NLP_MODELS / "email_vectorizer.pkl"


# =============================================================================
# LOAD DATASET
# =============================================================================

print("=" * 70)
print("Loading Email Dataset...")
print("=" * 70)

df = pd.read_csv(DATASET_PATH)

print(df.head())
print(df.shape)


# =============================================================================
# STANDARDIZE COLUMN NAMES
# =============================================================================

df = df.rename(
    columns={
        "Email Text": "text",
        "Email Type": "label",
    }
)


# =============================================================================
# PREPROCESS TEXT
# =============================================================================

print("\nCleaning text...")

preprocessor = TextPreprocessor()

df["text"] = preprocessor.preprocess_series(df["text"])


# =============================================================================
# TF-IDF
# =============================================================================

print("Extracting TF-IDF Features...")

tfidf = TFIDFEngine()

X = tfidf.fit_transform(df["text"])

y = df["label"]


# =============================================================================
# TRAIN TEST SPLIT
# =============================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y,
)


# =============================================================================
# TRAIN
# =============================================================================

trainer = BaseTrainer()

results = trainer.train(
    X_train,
    y_train,
    X_test,
    y_test,
)


# =============================================================================
# RESULTS
# =============================================================================

print("\n")
print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

for model_name, metrics in results.items():

    print(f"\n{model_name}")

    for metric, value in metrics.items():
        print(f"{metric:<12}: {value:.4f}")


# =============================================================================
# SAVE MODEL
# =============================================================================

trainer.save_best_model(MODEL_PATH)

tfidf.save(VECTORIZER_PATH)

print("\nTraining Complete.")
