"""
===============================================================================
RakshakAI - Text Preprocessor
===============================================================================

Common preprocessing pipeline for all NLP-based detection modules.

Supported Modules:
- Email Phishing
- URL
- SMS
- WhatsApp
- Fake Job
- Social Engineering
"""

import re
import string
from typing import List

import pandas as pd


class TextPreprocessor:
    """
    Common text preprocessing class.
    """

    def __init__(
        self,
        lowercase: bool = True,
        remove_punctuation: bool = True,
        remove_numbers: bool = False,
        strip_whitespace: bool = True,
    ):
        self.lowercase = lowercase
        self.remove_punctuation = remove_punctuation
        self.remove_numbers = remove_numbers
        self.strip_whitespace = strip_whitespace

    def clean_text(self, text: str) -> str:
        """
        Clean a single text string.

        Args:
            text: Input text.

        Returns:
            Cleaned text.
        """

        if pd.isna(text):
            return ""

        text = str(text)

        # Lowercase
        if self.lowercase:
            text = text.lower()

        # Remove URLs
        text = re.sub(r"http\S+|www\S+", " ", text)

        # Remove email addresses
        text = re.sub(r"\S+@\S+", " ", text)

        # Remove HTML tags
        text = re.sub(r"<.*?>", " ", text)

        # Remove punctuation
        if self.remove_punctuation:
            text = text.translate(str.maketrans("", "", string.punctuation))

        # Remove numbers
        if self.remove_numbers:
            text = re.sub(r"\d+", " ", text)

        # Remove multiple spaces
        text = re.sub(r"\s+", " ", text)

        if self.strip_whitespace:
            text = text.strip()

        return text

    def preprocess_series(self, series: pd.Series) -> pd.Series:
        """
        Preprocess an entire pandas Series.

        Args:
            series: Pandas Series.

        Returns:
            Cleaned Series.
        """

        return series.apply(self.clean_text)

    def preprocess_dataframe(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
    ) -> pd.DataFrame:
        """
        Preprocess a dataframe.

        Args:
            dataframe: Input dataframe.
            text_column: Name of text column.

        Returns:
            Clean dataframe.
        """

        dataframe = dataframe.copy()

        dataframe[text_column] = self.preprocess_series(dataframe[text_column])

        return dataframe
