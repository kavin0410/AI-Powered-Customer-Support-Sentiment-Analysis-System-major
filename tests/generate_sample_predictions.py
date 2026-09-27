"""
Script to test at least 20 real sample customer messages across all sentiments
and all 6 issue categories using the actual serialized Phase 1 models.
Saves the results directly to reports/sample_predictions.csv.
"""

import os
import sys
import pandas as pd

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.services.prediction_service import predict_text


# 24 diverse, realistic customer feedback texts
SAMPLE_TEXTS = [
    # Positive + Various categories
    "The product quality is absolutely outstanding and exceeded all my expectations!",
    "My package was delivered ahead of schedule and packaged with care.",
    "Payment was processed smoothly and the invoice was received instantly.",
    "The software updated seamlessly without any glitches or downtime.",
    "Customer service went above and beyond to assist me with my inquiry.",
    "Overall great shopping experience with your company, keep up the good work!",
    
    # Negative + Various categories
    "The item broke within two days of normal use, very poor quality.",
    "My delivery is five days late and the courier is not responding.",
    "Money was deducted from my account but the checkout failed and order was cancelled.",
    "The application keeps crashing every time I try to open the settings tab.",
    "The support agent was extremely rude and unhelpful on the phone.",
    "Terrible experience overall, I demand a full refund and explanation.",
    
    # Neutral + Various categories
    "Can you provide more information about the specifications of this model?",
    "When will my package be dispatched from the central sorting warehouse?",
    "Does your payment portal accept international debit cards?",
    "Is there an updated version of the mobile app available for download?",
    "I would like to inquire about the terms of your return policy.",
    "Just submitting general feedback regarding the website layout and color scheme.",
    
    # Additional edge/realistic scenarios
    "Received the wrong size and color compared to what I ordered online.",
    "The delivery driver left my package out in the heavy rain without notification.",
    "Double charged on my credit card statement for a single transaction.",
    "Login authentication fails repeatedly with a 500 error code on your portal.",
    "Representative Sarah resolved my issue in under three minutes, brilliant service!",
    "The product looks fine but the instructions manual was completely missing."
]


def generate_predictions():
    print(f"Generating predictions for {len(SAMPLE_TEXTS)} customer feedback messages...")
    results = []

    for idx, text in enumerate(SAMPLE_TEXTS, 1):
        pred = predict_text(text)
        print(f"[{idx:02d}] {pred.sentiment} ({pred.sentiment_confidence:.1%}) | {pred.issue_category} ({pred.issue_confidence:.1%}) | Attention: {pred.attention_level}")
        results.append({
            "text": text,
            "predicted_sentiment": pred.sentiment,
            "sentiment_confidence": round(pred.sentiment_confidence, 4),
            "predicted_issue": pred.issue_category,
            "issue_confidence": round(pred.issue_confidence, 4),
            "attention_level": pred.attention_level
        })

    os.makedirs("reports", exist_ok=True)
    out_csv = os.path.join("reports", "sample_predictions.csv")
    df = pd.DataFrame(results)
    df.to_csv(out_csv, index=False)
    print(f"\nSuccessfully saved {len(df)} sample predictions to '{out_csv}'.")


if __name__ == "__main__":
    generate_predictions()
