"""
Test script to run and record actual model predictions on the 8 required sample queries.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from app.utils.model_loader import predict_input
from app.utils.validation import determine_attention_level

test_inputs = [
    "The product quality is excellent and I am very happy with my purchase.",
    "My order arrived three days late and the package was damaged.",
    "Money was deducted from my account but the payment failed.",
    "The mobile application crashes whenever I try to open it.",
    "The customer service representative was very helpful.",
    "I received the wrong product.",
    "The delivery was completed on time.",
    "I would like to know more about your product."
]

print("=" * 80)
print("ACTUAL MODEL PREDICTIONS ON REQUIRED TEST SUITE SAMPLES")
print("=" * 80)

for idx, text in enumerate(test_inputs, 1):
    res = predict_input(text)
    att = determine_attention_level(res["sentiment"], res["sentiment_confidence"], res["issue_category"])
    print(f"\nSample #{idx}: \"{text}\"")
    print(f" -> Sentiment:          {res['sentiment']} (Confidence: {res['sentiment_confidence']:.1%})")
    print(f" -> Issue Category:     {res['issue_category']} (Confidence: {res['issue_confidence']:.1%})")
    print(f" -> Attention Level:    {att['level']}")
    print(f" -> Recommended Action: {att['action']}")
