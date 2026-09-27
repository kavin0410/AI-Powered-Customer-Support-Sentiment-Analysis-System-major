"""
Data loading and filtering utilities for Streamlit dashboard.
"""

import os
from typing import Optional, Tuple, List
import pandas as pd
import streamlit as st


DEFAULT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data", "processed", "cleaned_feedback.csv"
)


@st.cache_data(show_spinner="Loading customer feedback dataset...")
def load_data(csv_path: Optional[str] = None) -> pd.DataFrame:
    """
    Loads and caches the cleaned customer feedback dataset.
    Validates presence of required schema columns and parses timestamps.
    """
    path = csv_path or DEFAULT_DATA_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found at '{path}'. Please ensure 'data/processed/cleaned_feedback.csv' exists."
        )

    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"Error reading dataset from '{path}': {str(e)}")

    required_cols = {"feedback_id", "feedback_text", "sentiment", "issue_category", "date"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    # Standardize types and parse date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    df["date_only"] = df["date"].dt.date
    
    # Calculate text length metrics
    df["char_count"] = df["feedback_text"].astype(str).str.len()
    df["word_count"] = df["feedback_text"].astype(str).str.split().str.len()

    return df


def filter_data(
    df: pd.DataFrame,
    date_range: Optional[Tuple] = None,
    selected_sentiments: Optional[List[str]] = None,
    selected_categories: Optional[List[str]] = None,
    search_query: Optional[str] = None
) -> pd.DataFrame:
    """
    Filters DataFrame based on date range, sentiments, categories, and keyword search.
    """
    filtered = df.copy()

    # Date Range Filter
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        if start_date and end_date:
            filtered = filtered[
                (filtered["date_only"] >= start_date) & 
                (filtered["date_only"] <= end_date)
            ]

    # Sentiment Filter
    if selected_sentiments and len(selected_sentiments) > 0:
        filtered = filtered[filtered["sentiment"].isin(selected_sentiments)]

    # Issue Category Filter
    if selected_categories and len(selected_categories) > 0:
        filtered = filtered[filtered["issue_category"].isin(selected_categories)]

    # Search Query Filter
    if search_query and search_query.strip():
        q = search_query.strip().lower()
        filtered = filtered[
            filtered["feedback_text"].str.lower().str.contains(q, na=False) |
            filtered["feedback_id"].str.lower().str.contains(q, na=False)
        ]

    return filtered
