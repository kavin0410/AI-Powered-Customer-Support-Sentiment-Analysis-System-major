"""
KPI Metrics Card components for Streamlit Dashboard.
"""

import pandas as pd
import streamlit as st


def render_dashboard_kpis(df: pd.DataFrame, is_dark: bool = False):
    """
    Renders the primary 5-metric KPI card ribbon:
    Total Feedback | Positive | Negative | Neutral | Most Common Issue
    """
    total = len(df)
    if total == 0:
        st.warning("No records found matching current filter criteria.")
        return

    pos_count = (df["sentiment"] == "Positive").sum()
    neg_count = (df["sentiment"] == "Negative").sum()
    neu_count = (df["sentiment"] == "Neutral").sum()
    
    pos_pct = (pos_count / total) * 100
    neg_pct = (neg_count / total) * 100
    neu_pct = (neu_count / total) * 100

    issue_counts = df["issue_category"].value_counts()
    top_issue = issue_counts.index[0] if len(issue_counts) > 0 else "N/A"
    top_issue_count = issue_counts.iloc[0] if len(issue_counts) > 0 else 0
    top_issue_pct = (top_issue_count / total) * 100 if total > 0 else 0

    card_bg = "#1e293b" if is_dark else "#ffffff"
    text_color = "#f8fafc" if is_dark else "#0f172a"
    sub_color = "#94a3b8" if is_dark else "#64748b"
    border_color = "#334155" if is_dark else "#e2e8f0"

    cols = st.columns(5)

    metrics_data = [
        {"title": "Total Feedback", "val": f"{total:,}", "sub": "100% of analyzed data", "accent": "#6366f1"},
        {"title": "Positive Sentiment", "val": f"{pos_count:,}", "sub": f"{pos_pct:.1f}% of total", "accent": "#22c55e"},
        {"title": "Negative Sentiment", "val": f"{neg_count:,}", "sub": f"{neg_pct:.1f}% of total", "accent": "#ef4444"},
        {"title": "Neutral Sentiment", "val": f"{neu_count:,}", "sub": f"{neu_pct:.1f}% of total", "accent": "#0ea5e9"},
        {"title": "Top Issue Category", "val": top_issue, "sub": f"{top_issue_count:,} ({top_issue_pct:.1f}%)", "accent": "#a855f7"},
    ]

    for col, m in zip(cols, metrics_data):
        with col:
            html = f"""
            <div style="
                background-color: {card_bg};
                border: 1px solid {border_color};
                border-top: 4px solid {m['accent']};
                border-radius: 10px;
                padding: 1rem 0.9rem;
                margin-bottom: 0.8rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            ">
                <div style="font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; color: {sub_color}; margin-bottom: 0.35rem;">
                    {m['title']}
                </div>
                <div style="font-size: 1.45rem; font-weight: 700; color: {text_color}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {m['val']}
                </div>
                <div style="font-size: 0.78rem; color: {sub_color}; margin-top: 0.25rem;">
                    {m['sub']}
                </div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
