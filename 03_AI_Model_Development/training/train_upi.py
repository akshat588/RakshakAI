"""
===============================================================================
RakshakAI - UPI Fraud Detection Model Trainer
===============================================================================
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from config.config import RANDOM_STATE, TEST_SIZE
from config.paths import UPI_DATASET, NLP_MODELS
from training.base_trainer import BaseTrainer

# =============================================================================
# PATHS
# =============================================================================

DATASET_PATH = UPI_DATASET / "upi_fraud.csv"

MODEL_PATH = NLP_MODELS / "upi_detector.pkl"

# =============================================================================
# LOAD
# =============================================================================

print("=" * 70)
print("Loading UPI Dataset...")
print("=" * 70)

df = pd.read_csv(DATASET_PATH)

print(df.head())
print(df.shape)

# =============================================================================
# DROP UNUSED COLUMNS
# =============================================================================

drop_cols = [
    "Transaction_ID",
    "Customer_Name",
    "Customer_ID",
    "UPI_ID",
    "Merchant_UPI_ID",
    "IP_Address",
    "Device_ID",
    "Fraud_Type",
]

df = df.drop(columns=drop_cols)

# =============================================================================
# TARGET
# =============================================================================

y = df["Is_Fraudulent"]

X = df.drop(columns=["Is_Fraudulent"])

# =============================================================================
# CATEGORICAL / NUMERIC
# =============================================================================

categorical_cols = X.select_dtypes(include="object").columns.tolist()

numeric_cols = X.select_dtypes(exclude="object").columns.tolist()

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore")),
                ]
            ),
            categorical_cols,
        ),
        (
            "num",
            Pipeline([("imputer", SimpleImputer(strategy="median"))]),
            numeric_cols,
        ),
    ]
)

X = preprocessor.fit_transform(X)
# =============================================================================
# SAVE PREPROCESSOR
# =============================================================================

PREPROCESSOR_PATH = NLP_MODELS / "upi_preprocessor.pkl"

joblib.dump(preprocessor, PREPROCESSOR_PATH)

print("UPI Preprocessor Saved.")
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

print("\nUPI Model Training Complete.")
