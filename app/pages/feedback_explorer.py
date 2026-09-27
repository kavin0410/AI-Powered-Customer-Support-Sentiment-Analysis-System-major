"""
Feedback Explorer Page: Searchable, filterable feedback repository with CSV download and record inspector.
"""

import pandas as pd
import streamlit as st
from app.utils.data_loader import filter_data
from app.components.tables import render_feedback_table
from app.components.cards import render_card


def render(df: pd.DataFrame, is_dark: bool = False):
    """Renders the interactive feedback explorer."""
    st.markdown("## 📋 Customer Feedback Explorer")
    st.markdown("Query, search, inspect individual records, and export filtered customer feedback datasets.")

    # Search & Filter Controls
    with st.expander("🔍 Search & Filter Repository", expanded=True):
        f_col1, f_col2, f_col3 = st.columns([1.5, 1, 1])

        with f_col1:
            search_query = st.text_input(
                "Keyword Search (Text or ID)",
                placeholder="e.g. 'refund', 'broken', 'FB-00102'",
                key="exp_search"
            )

        with f_col2:
            all_sentiments = sorted(df["sentiment"].unique().tolist())
            selected_sent = st.multiselect(
                "Filter Sentiment",
                options=all_sentiments,
                default=[],
                placeholder="All Sentiments",
                key="exp_sentiment"
            )

        with f_col3:
            all_categories = sorted(df["issue_category"].unique().tolist())
            selected_cat = st.multiselect(
                "Filter Issue Category",
                options=all_categories,
                default=[],
                placeholder="All Categories",
                key="exp_category"
            )

        # Date Range
        min_date = df["date_only"].min()
        max_date = df["date_only"].max()
        date_range = st.date_input(
            "Filter Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="exp_dates"
        )

    # Filter dataframe
    filtered_df = filter_data(
        df,
        date_range=date_range if isinstance(date_range, tuple) and len(date_range) == 2 else None,
        selected_sentiments=selected_sent,
        selected_categories=selected_cat,
        search_query=search_query
    )

    # Display Table & Download Button
    render_feedback_table(filtered_df)

    st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

    # Record Inspector
    st.markdown("### 🔍 Single Record Detail Inspector")
    if len(filtered_df) > 0:
        sample_ids = filtered_df["feedback_id"].tolist()[:100]
        selected_id = st.selectbox(
            "Select Feedback ID to inspect detailed record:",
            options=sample_ids,
            key="exp_detail_id"
        )
        
        record = filtered_df[filtered_df["feedback_id"] == selected_id].iloc[0]

        sent = record["sentiment"]
        accent = "#22c55e" if sent == "Positive" else ("#ef4444" if sent == "Negative" else "#0ea5e9")

        detail_html = f"""
        <div style="font-size: 1.05rem; line-height: 1.6; margin-bottom: 0.8rem;">
            <em>"{record['feedback_text']}"</em>
        </div>
        <div style="display: flex; gap: 2rem; flex-wrap: wrap; font-size: 0.9rem;">
            <div><strong>Feedback ID:</strong> {record['feedback_id']}</div>
            <div><strong>Logged Date:</strong> {record['date'].strftime('%B %d, %Y')}</div>
            <div><strong>Sentiment:</strong> <span style="color: {accent}; font-weight: 700;">{record['sentiment']}</span></div>
            <div><strong>Issue Category:</strong> <span style="font-weight: 700;">{record['issue_category']}</span></div>
            <div><strong>Word Count:</strong> {record['word_count']} words</div>
        </div>
        """
        render_card(
            title=f"Record Inspector: {record['feedback_id']}",
            content=detail_html,
            border_color=accent,
            is_dark=is_dark
        )
    else:
        st.info("No records to inspect.")
