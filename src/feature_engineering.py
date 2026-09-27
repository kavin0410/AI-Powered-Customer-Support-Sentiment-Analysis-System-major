"""
Feature Engineering Module for Customer Support ML Pipeline.

Provides reusable TF-IDF vectorizer builders and text-to-feature pipelines.
"""

from typing import Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from src.preprocessing import TextPreprocessor


def build_tfidf_vectorizer(
    max_features: int = 5000,
    ngram_range: Tuple[int, int] = (1, 2),
    min_df: int = 2,
    max_df: float = 0.95,
    sublinear_tf: bool = True
) -> TfidfVectorizer:
    """
    Constructs a calibrated TfidfVectorizer configured for customer feedback texts.
    Uses unigrams and bigrams with sublinear TF scaling to damp outlier word frequencies.
    """
    return TfidfVectorizer(
        ngram_range=ngram_range,
        max_features=max_features,
        min_df=min_df,
        max_df=max_df,
        sublinear_tf=sublinear_tf
    )


def build_text_pipeline(classifier, max_features: int = 5000, ngram_range: Tuple[int, int] = (1, 2)) -> Pipeline:
    """
    Constructs a complete end-to-end scikit-learn Pipeline incorporating:
    1. Preprocessor: TextPreprocessor (cleans, lemmatizes, handles contractions)
    2. Vectorizer: TfidfVectorizer (extracts n-gram TF-IDF weights)
    3. Classifier: Specified estimator (Logistic Regression, MNB, LinearSVC, etc.)
    """
    return Pipeline([
        ("preprocessor", TextPreprocessor()),
        ("vectorizer", build_tfidf_vectorizer(max_features=max_features, ngram_range=ngram_range)),
        ("classifier", classifier)
    ])
