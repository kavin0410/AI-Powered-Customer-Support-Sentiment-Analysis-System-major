"""
Validation and business triage logic for the prediction engine.
"""

from typing import Dict, Any


def determine_attention_level(sentiment: str, sentiment_conf: float, issue_category: str) -> Dict[str, Any]:
    """
    Computes a transparent, reproducible Attention Level based on business rules:
    - Negative & Confidence >= 0.70 -> 'High' (Immediate specialist escalation)
    - Negative & Confidence < 0.70  -> 'Medium' (Standard queue review)
    - Neutral                      -> 'Medium' (Informational query / policy clarification)
    - Positive                     -> 'Low' (Retention tracking / employee praise)

    Note: This is a business triage layer, not an ML classification.
    """
    if sentiment == "Negative":
        if sentiment_conf >= 0.70:
            level = "High"
            action = f"Escalate urgently to senior {issue_category} specialist. Priority response required within 1 hour."
            explanation = f"High-confidence dissatisfaction ({sentiment_conf:.1%}) detected on {issue_category}."
        else:
            level = "Medium"
            action = f"Route to standard {issue_category} support queue with agent verification."
            explanation = f"Moderate-confidence negative sentiment ({sentiment_conf:.1%}) on {issue_category}."
    elif sentiment == "Neutral":
        level = "Medium"
        action = f"Route to standard knowledge base / support agent for {issue_category} clarification."
        explanation = f"Informational or neutral sentiment ({sentiment_conf:.1%}) regarding {issue_category}."
    else:  # Positive
        level = "Low"
        action = "Log positive feedback for customer retention tracking and internal recognition."
        explanation = f"Customer expressed positive feedback ({sentiment_conf:.1%}) for {issue_category}."

    return {
        "level": level,
        "action": action,
        "explanation": explanation
    }
