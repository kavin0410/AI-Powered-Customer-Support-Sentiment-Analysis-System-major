"""
Data table rendering and CSV export components for Streamlit.
"""

from datetime import datetime
import pandas as pd
import streamlit as st


def render_feedback_table(df: pd.DataFrame, page_size: int = 15):
    """
    Renders an interactive DataFrame display with selection, record count, and CSV export.
    """
    if len(df) == 0:
        st.info("No customer feedback records match the current filter or search criteria.")
        return

    # Display count
    st.markdown(f"**Displaying {len(df):,} feedback records**")

    # Display columns nicely
    display_df = df[["feedback_id", "date", "sentiment", "issue_category", "feedback_text"]].copy()
    display_df.columns = ["Feedback ID", "Date", "Sentiment", "Issue Category", "Customer Feedback"]

    # Styled dataframe
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=450
    )

    # Download Button
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name=f"customer_feedback_filtered_{timestamp}.csv",
        mime="text/csv",
        help="Download currently filtered feedback records as CSV"
    )
