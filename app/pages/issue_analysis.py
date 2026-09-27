"""
Issue Analysis Page: Deep-dive into customer support issue taxonomies, ticket frequency, and trends.
"""

import pandas as pd
import streamlit as st
import plotly.express as px
from app.components.charts import (
    plot_issue_category_bar,
    plot_issue_trend,
    plot_category_sentiment_stacked,
    plot_sentiment_issue_heatmap,
    CATEGORY_COLORS
)
from app.components.cards import render_card


def render(df: pd.DataFrame, is_dark: bool = False):
    """Renders the comprehensive issue category analytics view."""
    st.markdown("## 🏷️ Customer Support Issue Analysis")
    st.markdown("Quantify, monitor, and diagnose the distribution of customer issues across all six operational domains.")

    total = len(df)
    issue_counts = df["issue_category"].value_counts()
    
    most_reported = issue_counts.index[0]
    most_reported_count = issue_counts.iloc[0]
    most_reported_pct = (most_reported_count / total) * 100

    # Highest Negative Issue Calculation
    neg_by_cat = df[df["sentiment"] == "Negative"]["issue_category"].value_counts()
    highest_neg_issue = neg_by_cat.index[0]
    highest_neg_count = neg_by_cat.iloc[0]
    total_in_highest_neg = (df["issue_category"] == highest_neg_issue).sum()
    highest_neg_pct = (highest_neg_count / total_in_highest_neg) * 100

    # Top KPI Strip
    kpi_cols = st.columns(3)
    with kpi_cols[0]:
        st.metric("Total Issue Records", f"{total:,}")
    with kpi_cols[1]:
        st.metric("Most Reported Issue", most_reported, f"{most_reported_count:,} ({most_reported_pct:.1f}%)")
    with kpi_cols[2]:
        st.metric("Highest Negative Volume", highest_neg_issue, f"{highest_neg_count:,} negative tickets")

    st.markdown("<hr style='margin: 1.25rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

    # Dynamic Insight Callouts
    ins_col1, ins_col2 = st.columns(2)
    with ins_col1:
        render_card(
            title="📌 Most Prevalent Customer Problem",
            content=f"<strong>{most_reported}</strong> represents <strong>{most_reported_pct:.1f}%</strong> ({most_reported_count:,} records) of all submitted feedback, making it the primary driver of support ticket volume.",
            border_color="#3b82f6",
            is_dark=is_dark
        )
    with ins_col2:
        render_card(
            title="⚠️ Critical Dissatisfaction Hotspot",
            content=f"<strong>{highest_neg_issue}</strong> accounts for the largest absolute volume of negative complaints (<strong>{highest_neg_count:,}</strong> tickets, representing <strong>{highest_neg_pct:.1f}%</strong> of its category volume).",
            border_color="#ef4444",
            is_dark=is_dark
        )

    # Charts Row 1: Frequency & Proportions
    r1_col1, r1_col2 = st.columns(2)
    with r1_col1:
        st.plotly_chart(plot_issue_category_bar(df, is_dark=is_dark), use_container_width=True)
    with r1_col2:
        # Issue Percentage Donut
        pct_df = issue_counts.reset_index()
        pct_df.columns = ["issue_category", "count"]
        fig_donut = px.pie(
            pct_df,
            names="issue_category",
            values="count",
            hole=0.55,
            color="issue_category",
            color_discrete_map=CATEGORY_COLORS
        )
        fig_donut.update_traces(textposition="inside", textinfo="percent+label")
        fig_donut.update_layout(
            template="plotly_dark" if is_dark else "plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title="<b>Issue Category Share (%)</b>"
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # Charts Row 2: Temporal Issue Trajectory & Category Sentiment Mix
    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        st.plotly_chart(plot_issue_trend(df, is_dark=is_dark), use_container_width=True)
    with r2_col2:
        st.plotly_chart(plot_category_sentiment_stacked(df, is_dark=is_dark), use_container_width=True)

    # Charts Row 3: Heatmap
    st.plotly_chart(plot_sentiment_issue_heatmap(df, is_dark=is_dark), use_container_width=True)
