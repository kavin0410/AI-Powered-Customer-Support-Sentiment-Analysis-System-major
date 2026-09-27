"""
Unit tests for Streamlit application utilities and components (Phase 2).
"""

import pytest
import pandas as pd
from app.utils.data_loader import load_data, filter_data
from app.utils.model_loader import load_all_models, predict_input
from app.utils.validation import validate_feedback_text, determine_attention_level
from app.components.charts import (
    plot_sentiment_donut,
    plot_issue_category_bar,
    plot_monthly_trend,
    plot_sentiment_trend,
    plot_issue_trend,
    plot_sentiment_issue_heatmap,
    plot_probabilities_bar
)


class TestDataLoader:
    def test_load_data_schema(self):
        df = load_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "feedback_id" in df.columns
        assert "feedback_text" in df.columns
        assert "sentiment" in df.columns
        assert "issue_category" in df.columns
        assert "date" in df.columns
        assert "year_month" in df.columns
        assert "date_only" in df.columns

    def test_filter_data_sentiment(self):
        df = load_data()
        filtered = filter_data(df, selected_sentiments=["Positive"])
        assert len(filtered) > 0
        assert set(filtered["sentiment"].unique()) == {"Positive"}

    def test_filter_data_category(self):
        df = load_data()
        filtered = filter_data(df, selected_categories=["Payment Issue"])
        assert len(filtered) > 0
        assert set(filtered["issue_category"].unique()) == {"Payment Issue"}

    def test_filter_data_search(self):
        df = load_data()
        filtered = filter_data(df, search_query="refund")
        assert len(filtered) > 0
        for text in filtered["feedback_text"]:
            assert "refund" in text.lower()


class TestModelLoader:
    def test_load_all_models(self):
        sent_model, issue_model = load_all_models()
        assert sent_model is not None
        assert issue_model is not None

    def test_predict_input(self):
        text = "I received a duplicate charge on my credit card."
        res = predict_input(text)
        assert "sentiment" in res
        assert "sentiment_confidence" in res
        assert "issue_category" in res
        assert "issue_confidence" in res
        assert 0.0 <= res["sentiment_confidence"] <= 1.0
        assert 0.0 <= res["issue_confidence"] <= 1.0
        assert isinstance(res["sentiment_probabilities"], dict)
        assert isinstance(res["issue_probabilities"], dict)


class TestValidation:
    def test_validate_feedback_text_valid(self):
        valid, msg = validate_feedback_text("The product arrived in perfect shape.")
        assert valid is True
        assert msg == ""

    def test_validate_feedback_text_empty(self):
        valid, msg = validate_feedback_text("")
        assert valid is False
        assert "Please enter customer feedback" in msg

        valid_ws, msg_ws = validate_feedback_text("   \n\t  ")
        assert valid_ws is False

    def test_validate_feedback_text_too_short(self):
        valid, msg = validate_feedback_text("hi")
        assert valid is False
        assert "too brief" in msg

    def test_determine_attention_level_high(self):
        res = determine_attention_level("Negative", 0.85, "Payment Issue")
        assert res["level"] == "High"
        assert "High Attention" in res["badge"]

    def test_determine_attention_level_medium(self):
        res = determine_attention_level("Negative", 0.55, "Delivery Issue")
        assert res["level"] == "Medium"

    def test_determine_attention_level_low(self):
        res = determine_attention_level("Positive", 0.95, "Service Issue")
        assert res["level"] == "Low"


class TestCharts:
    def test_chart_generation(self):
        df = load_data()
        
        fig1 = plot_sentiment_donut(df, is_dark=False)
        fig2 = plot_issue_category_bar(df, is_dark=True)
        fig3 = plot_monthly_trend(df, is_dark=False)
        fig4 = plot_sentiment_trend(df, is_dark=True)
        fig5 = plot_issue_trend(df, is_dark=False)
        fig6 = plot_sentiment_issue_heatmap(df, is_dark=True)
        fig7 = plot_probabilities_bar({"Positive": 0.8, "Negative": 0.1, "Neutral": 0.1}, "Test", is_dark=False)

        assert fig1 is not None
        assert fig2 is not None
        assert fig3 is not None
        assert fig4 is not None
        assert fig5 is not None
        assert fig6 is not None
        assert fig7 is not None
