"""
Dashboard Page: Primary executive analytics view for customer support & sentiment trends.
"""

import pandas as pd
import streamlit as st
from app.components.metrics import render_dashboard_kpis
from app.components.charts import (
    plot_sentiment_donut,
    plot_issue_category_bar,
    plot_monthly_trend,
    plot_sentiment_trend,
    plot_issue_trend,
    plot_sentiment_issue_heatmap
)
from app.utils.data_loader import filter_data


def render(df: pd.DataFrame, is_dark: bool = False):
    """Renders the executive analytics dashboard."""
    st.markdown("## 🏠 Executive Support & Sentiment Dashboard")
    st.markdown("Real-time operational intelligence on customer sentiment and support issue patterns.")

    # Top Filter Ribbon
    with st.expander("🔍 Filter Dashboard Data", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            all_sentiments = sorted(df["sentiment"].unique().tolist())
            selected_sentiments = st.multiselect(
                "Filter by Sentiment",
                options=all_sentiments,
                default=all_sentiments,
                key="dash_sentiments"
            )

        with col2:
            all_categories = sorted(df["issue_category"].unique().tolist())
            selected_categories = st.multiselect(
                "Filter by Issue Category",
                options=all_categories,
                default=all_categories,
                key="dash_categories"
            )

        with col3:
            min_date = df["date_only"].min()
            max_date = df["date_only"].max()
            date_range = st.date_input(
                "Filter by Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key="dash_dates"
            )

    # Apply filters
    filtered_df = filter_data(
        df,
        date_range=date_range if isinstance(date_range, tuple) and len(date_range) == 2 else None,
        selected_sentiments=selected_sentiments,
        selected_categories=selected_categories
    )

    st.markdown(
        f"<div style='font-size: 0.95rem; font-weight: 600; margin: 0.5rem 0 1rem 0; color: {'#94a3b8' if is_dark else '#64748b'};'>"
        f"Showing {len(filtered_df):,} of {len(df):,} feedback records"
        f"</div>",
        unsafe_allow_html=True
    )

    if len(filtered_df) == 0:
        st.warning("No feedback records match the selected filter criteria. Please broaden your selection.")
        return

    # 1. KPI Cards
    render_dashboard_kpis(filtered_df, is_dark=is_dark)

    st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

    # 2. Main Distribution Row
    row1_col1, row1_col2 = st.columns([1, 1.2])
    with row1_col1:
        st.plotly_chart(plot_sentiment_donut(filtered_df, is_dark=is_dark), use_container_width=True)
    with row1_col2:
        st.plotly_chart(plot_issue_category_bar(filtered_df, is_dark=is_dark), use_container_width=True)

    # 3. Temporal Volume & Trend Row
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.plotly_chart(plot_monthly_trend(filtered_df, is_dark=is_dark), use_container_width=True)
    with row2_col2:
        st.plotly_chart(plot_sentiment_trend(filtered_df, is_dark=is_dark), use_container_width=True)

    # 4. Issue Trajectory & Cross-Tab Heatmap Row
    row3_col1, row3_col2 = st.columns([1.1, 0.9])
    with row3_col1:
        st.plotly_chart(plot_issue_trend(filtered_df, is_dark=is_dark), use_container_width=True)
    with row3_col2:
        st.plotly_chart(plot_sentiment_issue_heatmap(filtered_df, is_dark=is_dark), use_container_width=True)
