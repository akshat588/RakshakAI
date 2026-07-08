"""
===============================================================================
RakshakAI - TF-IDF Feature Engineering
===============================================================================

Reusable TF-IDF vectorizer for all NLP modules.

Supported Modules:
- Email
- SMS
- WhatsApp
- Fake Job
- Social Engineering
- URL
"""

from pathlib import Path
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDFEngine:
    """
    Reusable TF-IDF feature extractor.
    """

    def __init__(
        self,
        max_features: int = 10000,
        ngram_range: tuple = (1, 2),
        min_df: int = 2,
        max_df: float = 0.95,
    ):

        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            max_df=max_df,
            stop_words="english",
        )

    def fit_transform(self, texts):
        """
        Fit TF-IDF and transform training data.
        """
        return self.vectorizer.fit_transform(texts)

    def transform(self, texts):
        """
        Transform new data.
        """
        return self.vectorizer.transform(texts)

    def save(self, path):
        """
        Save TF-IDF vectorizer.
        """
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.vectorizer, path)

    def load(self, path):
        """
        Load TF-IDF vectorizer.
        """
        self.vectorizer = joblib.load(path)
