"""
Unit tests for predictor engine, schema validation, and edge case handling.
"""

import pytest
from src.predictor import (
    predict_sentiment,
    predict_issue,
    predict_feedback,
)
from src.preprocessing import VALID_SENTIMENTS, VALID_CATEGORIES


class TestPredictorValidation:
    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            predict_feedback("")

    def test_whitespace_string_raises_value_error(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            predict_feedback("   \t  \n  ")

    def test_none_input_raises_value_error(self):
        with pytest.raises(ValueError, match="cannot be None"):
            predict_feedback(None)

    def test_non_string_raises_type_error(self):
        with pytest.raises(TypeError, match="Expected string input"):
            predict_feedback(12345)


class TestPredictorOutputs:
    def test_predict_sentiment_schema(self):
        text = "This item is broken and completely useless."
        res = predict_sentiment(text)
        assert "sentiment" in res
        assert "confidence" in res
        assert "probabilities" in res
        assert res["sentiment"] in VALID_SENTIMENTS
        assert 0.0 <= res["confidence"] <= 1.0
        assert isinstance(res["probabilities"], dict)

    def test_predict_issue_schema(self):
        text = "My credit card was charged twice for the same subscription."
        res = predict_issue(text)
        assert "issue_category" in res
        assert "confidence" in res
        assert "probabilities" in res
        assert res["issue_category"] in VALID_CATEGORIES
        assert 0.0 <= res["confidence"] <= 1.0
        assert isinstance(res["probabilities"], dict)

    def test_predict_feedback_combined_schema(self):
        text = "The courier delivered the package to the wrong address."
        res = predict_feedback(text)
        
        assert "sentiment" in res
        assert "sentiment_confidence" in res
        assert "issue_category" in res
        assert "issue_confidence" in res
        
        assert res["sentiment"] in VALID_SENTIMENTS
        assert res["issue_category"] in VALID_CATEGORIES
        assert 0.0 <= res["sentiment_confidence"] <= 1.0
        assert 0.0 <= res["issue_confidence"] <= 1.0

    @pytest.mark.parametrize(
        "text,expected_sentiment,expected_issue",
        [
            ("The delivery was delayed by three weeks and courier dropped the box.", "Negative", "Delivery Issue"),
            ("Refund was processed back to my bank account instantly. Great service!", "Positive", "Payment Issue"),
            ("The website returns a 500 error code when logging into my account.", "Negative", "Technical Issue"),
            ("Customer agent took 2 hours to answer and then hung up the phone.", "Negative", "Service Issue"),
            ("Standard product dimensions match the catalog description sheet.", "Neutral", "Product Issue"),
        ]
    )
    def test_realistic_sample_predictions(self, text, expected_sentiment, expected_issue):
        res = predict_feedback(text)
        assert res["sentiment"] == expected_sentiment
        assert res["issue_category"] == expected_issue
