"""
===============================================================================
RakshakAI - Social Engineering Detection Model Trainer
===============================================================================
"""

import pandas as pd

from sklearn.model_selection import train_test_split

from config.config import RANDOM_STATE, TEST_SIZE
from config.paths import SOCIAL_DATASET, NLP_MODELS

from preprocessing.text_preprocessor import TextPreprocessor
from feature_engineering.tfidf import TFIDFEngine
from training.base_trainer import BaseTrainer

# =============================================================================
# PATHS
# =============================================================================

DATASET_PATH = SOCIAL_DATASET / "Dataset_5971.csv"

MODEL_PATH = NLP_MODELS / "social_engineering_detector.pkl"

VECTORIZER_PATH = NLP_MODELS / "social_engineering_vectorizer.pkl"

# =============================================================================
# LOAD DATASET
# =============================================================================

print("=" * 70)
print("Loading Social Engineering Dataset...")
print("=" * 70)

df = pd.read_csv(DATASET_PATH)

print(df.head())
print(df.shape)

# =============================================================================
# PREPROCESS
# =============================================================================

preprocessor = TextPreprocessor()

df["TEXT"] = preprocessor.preprocess_series(df["TEXT"])

# =============================================================================
# FEATURES
# =============================================================================

print("\nExtracting Features...")

tfidf = TFIDFEngine(
    max_features=10000,
    ngram_range=(1, 2),
)

X = tfidf.fit_transform(df["TEXT"])

y = df["LABEL"]

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

print("\nSocial Engineering Model Training Complete.")
