"""
AI-Powered Customer Support & Sentiment Analysis ML Package.
"""

from src.preprocessing import TextPreprocessor, clean_dataset, clean_text
from src.feature_engineering import build_tfidf_vectorizer, build_text_pipeline
from src.evaluation import evaluate_classifier, plot_confusion_matrix, create_comparison_table

__all__ = [
    "TextPreprocessor",
    "clean_dataset",
    "clean_text",
    "build_tfidf_vectorizer",
    "build_text_pipeline",
    "evaluate_classifier",
    "plot_confusion_matrix",
    "create_comparison_table"
]
