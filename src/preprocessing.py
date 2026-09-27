"""
Text Preprocessing and Data Cleaning Module.

Provides:
1. `TextPreprocessor`: Reusable text cleaning, tokenization, stopword filtering
   (preserving negation tokens crucial for sentiment), and lemmatization.
2. `clean_dataset`: Pipeline function to ingest raw CSV data, purge duplicates,
   handle missing/empty values, standardize categorical fields, validate dates,
   and persist clean datasets.
"""

import os
import re
import string
from typing import List, Optional, Union
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin

# Ensure required NLTK resources
try:
    STOP_WORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", quiet=True)
    STOP_WORDS = set(stopwords.words("english"))

# Sentiment-critical words that must NOT be removed as stopwords
NEGATION_WORDS = {
    "not", "no", "nor", "neither", "never", "none", "hardly", "scarcely",
    "barely", "cannot", "couldn't", "didn't", "doesn't", "don't", "hadn't",
    "hasn't", "haven't", "isn't", "mightn't", "mustn't", "needn't", "shan't",
    "shouldn't", "wasn't", "weren't", "won't", "wouldn't", "without", "against"
}

# Adjusted stop words set
CUSTOM_STOP_WORDS = STOP_WORDS - NEGATION_WORDS

# Standard categories and sentiments
VALID_SENTIMENTS = {"Positive", "Negative", "Neutral"}
VALID_CATEGORIES = {
    "Product Issue",
    "Delivery Issue",
    "Payment Issue",
    "Technical Issue",
    "Service Issue",
    "General Feedback"
}

# Normalization mapping for dirty casing/spacing
CATEGORY_MAP = {cat.lower(): cat for cat in VALID_CATEGORIES}
SENTIMENT_MAP = {s.lower(): s for s in VALID_SENTIMENTS}


class TextPreprocessor(BaseEstimator, TransformerMixin):
    """
    Reusable text preprocessing class compatible with scikit-learn Pipeline.
    
    Transforms raw strings into cleaned, normalized, lemmatized text tokens.
    """

    def __init__(
        self,
        lowercase: bool = True,
        remove_urls: bool = True,
        remove_punctuation: bool = True,
        remove_numbers: bool = False,
        remove_stopwords: bool = True,
        lemmatize: bool = True
    ):
        self.lowercase = lowercase
        self.remove_urls = remove_urls
        self.remove_punctuation = remove_punctuation
        self.remove_numbers = remove_numbers
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize
        
        self.lemmatizer = WordNetLemmatizer() if lemmatize else None
        self.stopwords = CUSTOM_STOP_WORDS if remove_stopwords else set()

    def fit(self, X, y=None):
        return self

    def transform(self, X) -> List[str]:
        if isinstance(X, pd.Series):
            return [self.preprocess(text) for text in X]
        elif isinstance(X, (list, np.ndarray)):
            return [self.preprocess(text) for text in X]
        elif isinstance(X, str):
            return self.preprocess(X)
        else:
            raise TypeError(f"Unsupported input type for TextPreprocessor: {type(X)}")

    def preprocess(self, text: Optional[Union[str, float]]) -> str:
        """Process a single piece of text."""
        if text is None or pd.isna(text) or not isinstance(text, str):
            return ""

        cleaned = text.strip()
        if not cleaned:
            return ""

        # 1. Lowercase conversion
        if self.lowercase:
            cleaned = cleaned.lower()

        # 2. URL removal
        if self.remove_urls:
            cleaned = re.sub(r"https?://\S+|www\.\S+", " ", cleaned)

        # 3. Email removal
        cleaned = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", " ", cleaned)

        # 4. Expand common contractions to preserve negation meaning
        cleaned = re.sub(r"won\'t", "will not", cleaned)
        cleaned = re.sub(r"can\'t", "can not", cleaned)
        cleaned = re.sub(r"n\'t", " not", cleaned)
        cleaned = re.sub(r"\'re", " are", cleaned)
        cleaned = re.sub(r"\'s", " is", cleaned)
        cleaned = re.sub(r"\'d", " would", cleaned)
        cleaned = re.sub(r"\'ll", " will", cleaned)
        cleaned = re.sub(r"\'t", " not", cleaned)
        cleaned = re.sub(r"\'ve", " have", cleaned)
        cleaned = re.sub(r"\'m", " am", cleaned)

        # 5. Remove numbers if configured
        if self.remove_numbers:
            cleaned = re.sub(r"\d+", " ", cleaned)

        # 6. Punctuation handling
        if self.remove_punctuation:
            # Replace punctuation with whitespace to prevent token welding (e.g., "broken,unusable" -> "broken unusable")
            translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
            cleaned = cleaned.translate(translator)

        # 7. Tokenization via whitespace split
        tokens = cleaned.split()

        # 8. Stopword removal (preserving negations)
        if self.remove_stopwords:
            tokens = [w for w in tokens if w not in self.stopwords]

        # 9. Lemmatization
        if self.lemmatize and self.lemmatizer:
            tokens = [self.lemmatizer.lemmatize(w) for w in tokens]

        # 10. Normalization of whitespace
        return " ".join(tokens).strip()


def clean_text(text: Optional[str]) -> str:
    """Convenience helper function for single string preprocessing."""
    preprocessor = TextPreprocessor()
    return preprocessor.preprocess(text)


def clean_dataset(raw_csv_path: str, output_csv_path: str) -> pd.DataFrame:
    """
    Ingests raw dataset, cleans missing/null/whitespace records, handles duplicates,
    standardizes categorical labels, validates dates, applies text cleaning,
    and saves the cleaned dataset.
    """
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw CSV not found at: {raw_csv_path}")

    df = pd.read_csv(raw_csv_path)
    initial_count = len(df)
    print(f"Loaded raw dataset from {raw_csv_path} with {initial_count} records.")

    # 1. Drop complete duplicates
    df = df.drop_duplicates(subset=["feedback_text", "sentiment", "issue_category"])
    dropped_dupes = initial_count - len(df)

    # 2. Handle missing or whitespace-only feedback_text
    df = df.dropna(subset=["feedback_text"])
    df["feedback_text"] = df["feedback_text"].astype(str).str.strip()
    df = df[df["feedback_text"].str.len() > 0]
    
    # 3. Standardize and validate sentiment
    df["sentiment"] = df["sentiment"].astype(str).str.strip().str.lower().map(SENTIMENT_MAP)
    df = df.dropna(subset=["sentiment"])
    df = df[df["sentiment"].isin(VALID_SENTIMENTS)]

    # 4. Standardize and validate issue_category
    df["issue_category"] = df["issue_category"].astype(str).str.strip().str.lower().map(CATEGORY_MAP)
    df = df.dropna(subset=["issue_category"])
    df = df[df["issue_category"].isin(VALID_CATEGORIES)]

    # 5. Clean / validate dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # 6. Apply Text Preprocessor to add preprocessed text column for fast training
    preprocessor = TextPreprocessor()
    df["cleaned_text"] = [preprocessor.preprocess(t) for t in df["feedback_text"]]
    
    # Filter out any records whose cleaned text ended up empty
    df = df[df["cleaned_text"].str.len() > 0]

    # Re-index feedback_id if needed
    df["feedback_id"] = [f"FB-{i+1:05d}" for i in range(len(df))]
    df = df.reset_index(drop=True)

    # Save processed dataset
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)

    final_count = len(df)
    print(f"Cleaning complete. Dropped duplicates: {dropped_dupes}. Remaining records: {final_count}.")
    print(f"Cleaned dataset saved to: {output_csv_path}")

    return df


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    raw_p = os.path.join(base_dir, "data", "raw", "raw_feedback.csv")
    clean_p = os.path.join(base_dir, "data", "processed", "cleaned_feedback.csv")
    clean_dataset(raw_p, clean_p)
