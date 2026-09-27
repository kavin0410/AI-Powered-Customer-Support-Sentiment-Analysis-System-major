"""
Sentiment Analysis Page: In-depth sentiment metrics, trends, and category correlations.
"""

import pandas as pd
import streamlit as st
from app.components.charts import (
    plot_sentiment_donut,
    plot_sentiment_trend,
    plot_monthly_trend,
    plot_category_sentiment_stacked,
    plot_sentiment_issue_heatmap
)
from app.components.cards import render_card


def render(df: pd.DataFrame, is_dark: bool = False):
    """Renders the detailed sentiment analytics view."""
    st.markdown("## 😊 Customer Sentiment Analysis")
    st.markdown("Detailed breakdown of sentiment trends, proportions, and cross-category dynamics.")

    total = len(df)
    pos_count = (df["sentiment"] == "Positive").sum()
    neg_count = (df["sentiment"] == "Negative").sum()
    neu_count = (df["sentiment"] == "Neutral").sum()

    pos_pct = (pos_count / total) * 100 if total > 0 else 0
    neg_pct = (neg_count / total) * 100 if total > 0 else 0
    neu_pct = (neu_count / total) * 100 if total > 0 else 0

    # Dynamic Calculation of Category Sentiment Extrema
    cat_cross = pd.crosstab(df["issue_category"], df["sentiment"], normalize="index") * 100
    for s in ["Negative", "Positive", "Neutral"]:
        if s not in cat_cross.columns:
            cat_cross[s] = 0.0

    highest_neg_cat = cat_cross["Negative"].idxmax()
    highest_neg_pct = cat_cross["Negative"].max()

    highest_pos_cat = cat_cross["Positive"].idxmax()
    highest_pos_pct = cat_cross["Positive"].max()

    # Top KPI Strip
    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.metric("Total Analyzed Feedback", f"{total:,}")
    with kpi_cols[1]:
        st.metric("Positive Sentiment", f"{pos_pct:.1f}%", f"{pos_count:,} reviews")
    with kpi_cols[2]:
        st.metric("Negative Sentiment", f"{neg_pct:.1f}%", f"{neg_count:,} reviews")
    with kpi_cols[3]:
        st.metric("Neutral Sentiment", f"{neu_pct:.1f}%", f"{neu_count:,} reviews")

    st.markdown("<hr style='margin: 1.25rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

    # Dynamic Insights Callout Cards
    insight_cols = st.columns(2)
    with insight_cols[0]:
        render_card(
            title="⚠️ Highest Negative Feedback Concentration",
            content=f"<strong>{highest_neg_cat}</strong> exhibits the highest dissatisfaction rate at <strong>{highest_neg_pct:.1f}%</strong> negative sentiment. Prioritize operational triage for this segment.",
            border_color="#ef4444",
            is_dark=is_dark
        )
    with insight_cols[1]:
        render_card(
            title="🌟 Highest Positive Feedback Concentration",
            content=f"<strong>{highest_pos_cat}</strong> holds the highest satisfaction rate with <strong>{highest_pos_pct:.1f}%</strong> positive sentiment, highlighting strong operational performance.",
            border_color="#22c55e",
            is_dark=is_dark
        )

    # Charts Row 1: Distribution & Trajectory
    r1_col1, r1_col2 = st.columns(2)
    with r1_col1:
        st.plotly_chart(plot_sentiment_donut(df, is_dark=is_dark), use_container_width=True)
    with r1_col2:
        st.plotly_chart(plot_sentiment_trend(df, is_dark=is_dark), use_container_width=True)

    # Charts Row 2: Monthly Volume & Category Stacked Mix
    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        st.plotly_chart(plot_monthly_trend(df, is_dark=is_dark), use_container_width=True)
    with r2_col2:
        st.plotly_chart(plot_category_sentiment_stacked(df, is_dark=is_dark), use_container_width=True)

    # Charts Row 3: Full Cross-tab Heatmap
    st.plotly_chart(plot_sentiment_issue_heatmap(df, is_dark=is_dark), use_container_width=True)
