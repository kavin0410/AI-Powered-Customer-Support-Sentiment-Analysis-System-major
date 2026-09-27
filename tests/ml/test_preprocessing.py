"""
Unit tests for text preprocessing, tokenization, and negation preservation.
"""

import pytest
from src.preprocessing import TextPreprocessor, clean_text, NEGATION_WORDS


class TestTextPreprocessor:
    def setup_method(self):
        self.preprocessor = TextPreprocessor()

    def test_lowercase_conversion(self):
        text = "EXTREMELY DISAPPOINTED with the Service!"
        result = self.preprocessor.preprocess(text)
        assert result == result.lower()
        assert "disappointed" in result

    def test_url_removal(self):
        text = "Visit https://support.example.com/help or http://bit.ly/test for info"
        result = self.preprocessor.preprocess(text)
        assert "http" not in result
        assert "support.example.com" not in result
        assert "info" in result

    def test_email_removal(self):
        text = "Contact me at user.support@company.com immediately."
        result = self.preprocessor.preprocess(text)
        assert "user.support@company.com" not in result
        assert "@" not in result

    def test_punctuation_handling(self):
        text = "Broken, unusable! Terrible... worst purchase ever???"
        result = self.preprocessor.preprocess(text)
        for char in [",", "!", ".", "?"]:
            assert char not in result

    def test_negation_preservation(self):
        text = "The product is not working and I did not receive any help."
        result = self.preprocessor.preprocess(text)
        assert "not" in result.split(), "Negation token 'not' was erroneously stripped!"
        
        text2 = "I never received my package, it was never delivered."
        result2 = self.preprocessor.preprocess(text2)
        assert "never" in result2.split(), "Negation token 'never' was stripped!"

    def test_contraction_expansion(self):
        text = "I wasn't able to login and shouldn't have been charged."
        result = self.preprocessor.preprocess(text)
        assert "not" in result

    def test_empty_and_none_input(self):
        assert self.preprocessor.preprocess("") == ""
        assert self.preprocessor.preprocess("   \t\n  ") == ""
        assert self.preprocessor.preprocess(None) == ""


def test_clean_text_helper():
    res = clean_text("Check http://test.com - Awesome experience!")
    assert "awesome" in res
    assert "http" not in res
