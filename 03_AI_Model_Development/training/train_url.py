"""
===============================================================================
RakshakAI - URL Detection Model Trainer
===============================================================================
"""

import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split

from config.config import RANDOM_STATE, TEST_SIZE
from config.paths import URL_DATASET, NLP_MODELS

from preprocessing.text_preprocessor import TextPreprocessor
from feature_engineering.tfidf import TFIDFEngine
from training.base_trainer import BaseTrainer

# =============================================================================
# PATHS
# =============================================================================

DATASET_PATH = URL_DATASET / "urls.csv"

MODEL_PATH = NLP_MODELS / "url_detector.pkl"

VECTORIZER_PATH = NLP_MODELS / "url_vectorizer.pkl"

# =============================================================================
# LOAD DATASET
# =============================================================================

print("=" * 70)
print("Loading URL Dataset...")
print("=" * 70)

df = pd.read_csv(DATASET_PATH)

print(df.head())
print(df.shape)

# =============================================================================
# PREPROCESS
# =============================================================================

preprocessor = TextPreprocessor(
    lowercase=True, remove_punctuation=False, remove_numbers=False
)

df["url"] = preprocessor.preprocess_series(df["url"])

# =============================================================================
# TF-IDF
# =============================================================================

print("\nExtracting Features...")

tfidf = TFIDFEngine(
    max_features=15000,
    ngram_range=(3, 5),
    min_df=2,
    max_df=0.95,
)

X = tfidf.fit_transform(df["url"])

y = df["status"]

# =============================================================================
# SPLIT
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
# SAVE
# =============================================================================

trainer.save_best_model(MODEL_PATH)

tfidf.save(VECTORIZER_PATH)

print("\nURL Model Training Complete.")
