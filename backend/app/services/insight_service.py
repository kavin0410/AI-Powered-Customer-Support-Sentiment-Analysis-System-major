"""
Insight Service dynamically generating factual operational observations and strategic business actions.
"""

from typing import List
from backend.app.models.schemas import InsightItem
from backend.app.services.analytics_service import get_dashboard_data


def generate_business_insights() -> List[InsightItem]:
    """
    Synthesizes current dataset statistics to generate real, non-fabricated operational observations.
    Each item separates the factual data observation from actionable recommendations.
    """
    dash = get_dashboard_data()
    total = dash.total_feedback

    if total == 0:
        return []

    insights = []

    # 1. Most Common Issue
    top_issue = dash.most_common_issue
    top_count = dash.most_common_issue_count
    top_pct = round((top_count / total) * 100, 1)

    insights.append(InsightItem(
        type="observation",
        title=f"Primary Ticket Volume Driver: {top_issue}",
        description=f"{top_issue} represents {top_pct}% ({top_count:,} out of {total:,} feedback items) of all logged support inquiries.",
        metric=f"{top_pct}% Share",
        action=f"Deploy specialized {top_issue.lower()} triage workflows and enrich self-service documentation to reduce ticket load."
    ))

    # 2. Critical Dissatisfaction Hotspot
    if dash.sentiment_issue_matrix:
        highest_neg_cat = max(dash.sentiment_issue_matrix, key=lambda x: x["negative_pct"])
        neg_pct_val = highest_neg_cat["negative_pct"]
        cat_name = highest_neg_cat["category"]

        insights.append(InsightItem(
            type="observation",
            title=f"Critical Dissatisfaction Concentration: {cat_name}",
            description=f"{cat_name} exhibits the highest customer dissatisfaction rate at {neg_pct_val}% negative sentiment.",
            metric=f"{neg_pct_val}% Negative",
            action=f"Establish automated manager escalations and expedited compensation workflows for verified {cat_name.lower()} tickets."
        ))

    # 3. Overall Customer Sentiment Baseline
    neg_total_pct = dash.negative_percentage
    pos_total_pct = dash.positive_percentage

    insights.append(InsightItem(
        type="observation",
        title="Customer Sentiment Baseline & Churn Indicator",
        description=f"Negative feedback accounts for {neg_total_pct}% of total customer interactions, while positive reviews account for {pos_total_pct}%.",
        metric=f"{neg_total_pct}% Dissatisfaction",
        action="Integrate sentiment confidence directly into queue prioritization to triage high-risk churn customers before standard tickets."
    ))

    # 4. Seasonal Feedback Surge
    if dash.monthly_feedback:
        peak_month_item = max(dash.monthly_feedback, key=lambda x: x.total)
        peak_m = peak_month_item.month
        peak_vol = peak_month_item.total
        peak_share = round((peak_vol / total) * 100, 1)

        insights.append(InsightItem(
            type="observation",
            title=f"Peak Volume Surge in {peak_m}",
            description=f"Support demand peaked during {peak_m} with {peak_vol:,} feedback records ({peak_share}% of annual traffic).",
            metric=f"{peak_vol:,} Records",
            action=f"Schedule surge support capacity and staff flexible shifts during {peak_m} to avoid response SLA breaches."
        ))

    return insights
