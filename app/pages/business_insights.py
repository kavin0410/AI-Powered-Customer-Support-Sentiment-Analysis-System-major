"""
Business Insights Page: Automated, fact-based operational observations and strategic business actions.
"""

import pandas as pd
import streamlit as st
from app.components.cards import render_card


def render(df: pd.DataFrame, is_dark: bool = False):
    """Renders data-driven business insights derived dynamically from the dataset."""
    st.markdown("## 💡 Data-Driven Business Insights")
    st.markdown(
        "Automated operational diagnostics synthesizing sentiment trends, issue prevalence, "
        "and actionable business interventions."
    )

    total_records = len(df)
    if total_records == 0:
        st.warning("Insufficient data to compute business insights.")
        return

    # Dynamic Calculations
    sent_counts = df["sentiment"].value_counts()
    neg_count = sent_counts.get("Negative", 0)
    neg_pct = (neg_count / total_records) * 100

    issue_counts = df["issue_category"].value_counts()
    top_issue = issue_counts.index[0]
    top_issue_count = issue_counts.iloc[0]
    top_issue_pct = (top_issue_count / total_records) * 100

    # Cross-tab for highest negative category percentage
    crosstab_pct = pd.crosstab(df["issue_category"], df["sentiment"], normalize="index") * 100
    if "Negative" in crosstab_pct.columns:
        highest_neg_cat = crosstab_pct["Negative"].idxmax()
        highest_neg_rate = crosstab_pct["Negative"].max()
    else:
        highest_neg_cat, highest_neg_rate = "N/A", 0.0

    # Peak Volume Month
    monthly_vol = df["year_month"].value_counts()
    peak_month = monthly_vol.index[0]
    peak_month_vol = monthly_vol.iloc[0]
    peak_month_pct = (peak_month_vol / total_records) * 100

    # Short vs Long feedback sentiment
    df["len_bucket"] = pd.cut(df["word_count"], bins=[0, 15, 35, 1000], labels=["Short", "Medium", "Long"])
    len_neg = df[df["sentiment"] == "Negative"]["len_bucket"].value_counts(normalize=True) * 100
    dominant_neg_len = len_neg.index[0] if len(len_neg) > 0 else "Medium"

    # Display Strategic Overview KPI ribbon
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Dissatisfaction", f"{neg_pct:.1f}%", f"{neg_count:,} negative reviews")
    with col2:
        st.metric("Primary Ticket Driver", top_issue, f"{top_issue_pct:.1f}% share")
    with col3:
        st.metric("Most Vulnerable Category", highest_neg_cat, f"{highest_neg_rate:.1f}% negative rate")
    with col4:
        st.metric("Peak Feedback Month", peak_month, f"{peak_month_vol:,} records")

    st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

    # Structured Insights with Strict Separation of Observation vs Action
    insights = [
        {
            "num": 1,
            "title": f"High Ticket Volume in {top_issue}",
            "observation": (
                f"<strong>{top_issue}</strong> accounts for <strong>{top_issue_pct:.1f}%</strong> "
                f"({top_issue_count:,} out of {total_records:,} feedback entries), making it the single largest "
                f"category of customer support inquiries."
            ),
            "action": (
                f"Conduct an end-to-end quality audit on {top_issue.lower()} processes. Establish dedicated rapid-response "
                f"teams and enhance self-service FAQs to deflect high-frequency queries."
            ),
            "accent": "#3b82f6"
        },
        {
            "num": 2,
            "title": f"Critical Dissatisfaction Concentration in {highest_neg_cat}",
            "observation": (
                f"Feedback classified under <strong>{highest_neg_cat}</strong> demonstrates the highest proportion of negative "
                f"sentiment at <strong>{highest_neg_rate:.1f}%</strong>, indicating that customers experiencing this issue "
                f"have a very high churn risk."
            ),
            "action": (
                f"Revise the operational escalation workflow for {highest_neg_cat.lower()}. Establish proactive outreach protocols "
                f"and automated refund/compensation mechanisms for verified service breakdowns."
            ),
            "accent": "#ef4444"
        },
        {
            "num": 3,
            "title": "Overall Sentiment Baseline & Churn Indicator",
            "observation": (
                f"Negative feedback represents <strong>{neg_pct:.1f}%</strong> of all received feedback, while positive feedback "
                f"stands at <strong>{(sent_counts.get('Positive', 0)/total_records)*100:.1f}%</strong> and neutral inquiries account "
                f"for <strong>{(sent_counts.get('Neutral', 0)/total_records)*100:.1f}%</strong>."
            ),
            "action": (
                "Deploy real-time sentiment scoring directly into the support ticketing queue to automatically route high-confidence "
                "negative tickets to Tier-2 support specialists, reducing customer resolution wait times."
            ),
            "accent": "#f59e0b"
        },
        {
            "num": 4,
            "title": f"Temporal Volume Surge in {peak_month}",
            "observation": (
                f"Customer feedback reached an apex in <strong>{peak_month}</strong> with <strong>{peak_month_vol:,}</strong> "
                f"records (<strong>{peak_month_pct:.1f}%</strong> of total annual volume), representing a seasonal influx of support demand."
            ),
            "action": (
                f"Plan ahead for cyclical spikes in support load during {peak_month} by scheduling flexible staffing, pre-training "
                f"seasonal agents, and verifying server capacity to prevent app timeout and delivery delays."
            ),
            "accent": "#8b5cf6"
        }
    ]

    for item in insights:
        card_content = f"""
        <div style="margin-bottom: 0.8rem;">
            <div style="font-size: 0.82rem; font-weight: 700; text-transform: uppercase; color: {'#94a3b8' if is_dark else '#64748b'}; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
                📊 DATA OBSERVATION
            </div>
            <div style="font-size: 0.95rem; line-height: 1.5; margin-bottom: 0.8rem;">
                {item['observation']}
            </div>
            
            <div style="font-size: 0.82rem; font-weight: 700; text-transform: uppercase; color: {item['accent']}; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
                🎯 RECOMMENDED BUSINESS ACTION
            </div>
            <div style="font-size: 0.95rem; line-height: 1.5;">
                {item['action']}
            </div>
        </div>
        """
        render_card(
            title=f"Insight #{item['num']}: {item['title']}",
            content=card_content,
            border_color=item["accent"],
            is_dark=is_dark
        )
