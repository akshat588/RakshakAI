"""
===============================================================================
RakshakAI - Base Trainer
===============================================================================

Generic training engine for NLP models.

Supports:
- Logistic Regression
- Linear SVM
- Multinomial Naive Bayes
- Random Forest

Automatically selects the best model based on F1-score.
"""

from pathlib import Path
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


class BaseTrainer:

    def __init__(self):

        self.models = {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Linear SVM": LinearSVC(),
            "Naive Bayes": MultinomialNB(),
        }

        self.best_model = None
        self.best_name = None
        self.best_score = 0.0

    def train(self, X_train, y_train, X_test, y_test):

        results = {}

        for name, model in self.models.items():

            print(f"\nTraining {name}...")

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            accuracy = accuracy_score(y_test, predictions)

            precision = precision_score(
                y_test,
                predictions,
                average="weighted",
            )

            recall = recall_score(
                y_test,
                predictions,
                average="weighted",
            )

            f1 = f1_score(
                y_test,
                predictions,
                average="weighted",
            )

            results[name] = {
                "Accuracy": accuracy,
                "Precision": precision,
                "Recall": recall,
                "F1": f1,
            }

            if f1 > self.best_score:

                self.best_score = f1
                self.best_model = model
                self.best_name = name

        return results

    def save_best_model(self, model_path):

        if self.best_model is None:
            raise ValueError("No trained model available.")

        Path(model_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        joblib.dump(
            self.best_model,
            model_path,
        )

        print(f"\nBest Model : {self.best_name}")
        print(f"Saved To   : {model_path}")
