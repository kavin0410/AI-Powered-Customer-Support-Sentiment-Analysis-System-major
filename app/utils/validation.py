"""
Input validation and business decision rules for the prediction engine.
"""

from typing import Tuple, Dict, Any


MAX_TEXT_LENGTH = 3000


def validate_feedback_text(text: str) -> Tuple[bool, str]:
    """
    Validates user-submitted feedback string.
    Returns (is_valid, error_message).
    """
    if text is None:
        return False, "Please enter customer feedback before running prediction."

    cleaned = text.strip()
    if not cleaned:
        return False, "Please enter customer feedback before running prediction."

    if len(cleaned) < 3:
        return False, "Feedback is too brief. Please enter at least a few words."

    if len(cleaned) > MAX_TEXT_LENGTH:
        return False, f"Feedback exceeds maximum character limit of {MAX_TEXT_LENGTH} characters."

    return True, ""


def determine_attention_level(sentiment: str, sentiment_conf: float, issue_category: str) -> Dict[str, Any]:
    """
    Computes a transparent, reproducible Attention Level & Triage Action based on:
    1. Sentiment severity: Negative feedback poses customer churn risk.
    2. Sentiment confidence: High-confidence negativity requires expedited escalation.
    3. Category urgency: Payment & Delivery failures have high operational stakes.

    Logic rules:
    - Negative & Confidence >= 0.70 -> 'High' (Immediate supervisor/specialist escalation required)
    - Negative & Confidence < 0.70  -> 'Medium' (Standard queue escalation with agent verification)
    - Neutral                      -> 'Medium' (Informational query / policy clarification queue)
    - Positive                     -> 'Low' (Customer satisfaction record / retention nurture)
    """
    if sentiment == "Negative":
        if sentiment_conf >= 0.70:
            level = "High"
            color = "#e74c3c"
            badge = "🔴 High Attention"
            action = f"Escalate immediately to senior {issue_category} specialist. Prioritize customer outreach within 1 hour."
        else:
            level = "Medium"
            color = "#f39c12"
            badge = "🟠 Medium Attention"
            action = f"Route to standard {issue_category} support team for detailed ticket assessment."
    elif sentiment == "Neutral":
        level = "Medium"
        color = "#3498db"
        badge = "🔵 Medium Attention"
        action = f"Route to general knowledge base / information desk for {issue_category} clarification."
    else:  # Positive
        level = "Low"
        color = "#2ecc71"
        badge = "🟢 Low Attention"
        action = "Log positive feedback for customer retention tracking and employee recognition."

    return {
        "level": level,
        "badge": badge,
        "color": color,
        "action": action,
        "explanation": f"{sentiment} sentiment detected with {sentiment_conf:.1%} confidence for {issue_category}."
    }
