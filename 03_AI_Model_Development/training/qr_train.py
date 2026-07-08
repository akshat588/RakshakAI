"""
===============================================================================
RakshakAI
QR Code AI Model Training
===============================================================================
"""

from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# =============================================================================
# Paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = PROJECT_ROOT / "03_AI_Model_Development" / "datasets" / "qr_dataset.csv"

MODEL_DIR = PROJECT_ROOT / "03_AI_Model_Development" / "saved_models" / "nlp"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "qr_detector.pkl"
VECTORIZER_PATH = MODEL_DIR / "qr_vectorizer.pkl"

# =============================================================================
# Load Dataset
# =============================================================================

print("=" * 70)
print("Loading QR Dataset...")
print("=" * 70)

df = pd.read_csv(DATASET_PATH)

print(f"Samples : {len(df)}")
print(df["label"].value_counts())

# =============================================================================
# Features
# =============================================================================

X = df["qr_content"].astype(str)
y = df["label"]

# =============================================================================
# Split
# =============================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print(f"\nTraining : {len(X_train)}")
print(f"Testing  : {len(X_test)}")

# =============================================================================
# TF-IDF
# =============================================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words=None,
    ngram_range=(1, 2),
    max_features=10000,
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# =============================================================================
# Model
# =============================================================================

print("\nTraining Logistic Regression...")

model = LogisticRegression(
    random_state=42,
    max_iter=1000,
)

model.fit(X_train_vec, y_train)

# =============================================================================
# Evaluation
# =============================================================================

pred = model.predict(X_test_vec)

acc = accuracy_score(y_test, pred)
pre = precision_score(y_test, pred)
rec = recall_score(y_test, pred)
f1 = f1_score(y_test, pred)

print("\n" + "=" * 70)
print("Evaluation")
print("=" * 70)

print(f"Accuracy : {acc:.4f}")
print(f"Precision: {pre:.4f}")
print(f"Recall   : {rec:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nConfusion Matrix")
print(confusion_matrix(y_test, pred))

print("\nClassification Report")
print(classification_report(y_test, pred))

# =============================================================================
# Save
# =============================================================================

joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print("\n" + "=" * 70)
print("Model Saved Successfully")
print("=" * 70)

print(f"Model      : {MODEL_PATH}")
print(f"Vectorizer : {VECTORIZER_PATH}")
