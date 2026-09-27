"""
AI-Powered Customer Support & Sentiment Analysis System
Main Web Application Entrypoint (Phase 2).
"""

import os
import sys
import streamlit as st

# Configure project path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Page configuration
st.set_page_config(
    page_title="AI Customer Support & Sentiment Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

from app.utils.data_loader import load_data
from app.utils.model_loader import load_all_models
from app.pages import (
    dashboard,
    prediction,
    feedback_explorer,
    sentiment_analysis,
    issue_analysis,
    business_insights,
    about
)


def apply_theme_css(is_dark: bool):
    """Injects custom CSS to support consistent Light and Dark themes."""
    if is_dark:
        bg_main = "#0f172a"
        text_main = "#f8fafc"
        sidebar_bg = "#1e293b"
        card_bg = "#1e293b"
        border_subtle = "#334155"
    else:
        bg_main = "#f8fafc"
        text_main = "#0f172a"
        sidebar_bg = "#ffffff"
        card_bg = "#ffffff"
        border_subtle = "#e2e8f0"

    css = f"""
    <style>
        /* Base typography and layout */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        .stApp {{
            background-color: {bg_main};
            color: {text_main};
        }}

        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg};
            border-right: 1px solid {border_subtle};
        }}

        /* Buttons styling */
        .stButton>button {{
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
        }}
        .stButton>button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}

        /* Expander headers */
        .streamlit-expanderHeader {{
            font-weight: 600;
            border-radius: 8px;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def main():
    # Theme state management
    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "🌞 Light Theme"

    # Sidebar Header
    st.sidebar.markdown(
        """
        <div style="padding: 0.5rem 0 1rem 0; text-align: center;">
            <div style="font-size: 2.2rem; margin-bottom: 0.2rem;">🤖</div>
            <h2 style="font-size: 1.25rem; font-weight: 700; margin: 0; line-height: 1.3;">Support AI System</h2>
            <div style="font-size: 0.78rem; color: #64748b; font-weight: 500;">Sentiment & Issue Analytics</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Theme Switcher in Sidebar
    theme_choice = st.sidebar.radio(
        "Display Theme",
        options=["🌞 Light Theme", "🌙 Dark Theme"],
        index=0 if st.session_state["theme_mode"] == "🌞 Light Theme" else 1,
        horizontal=True
    )
    st.session_state["theme_mode"] = theme_choice
    is_dark = (theme_choice == "🌙 Dark Theme")
    apply_theme_css(is_dark)

    st.sidebar.markdown("<hr style='margin: 0.8rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

    # Navigation menu
    nav_options = [
        "🏠 Dashboard",
        "🔮 Predict Feedback",
        "📋 Feedback Explorer",
        "😊 Sentiment Analysis",
        "🏷️ Issue Analysis",
        "💡 Business Insights",
        "ℹ️ About"
    ]

    selected_page = st.sidebar.radio(
        "Navigation",
        options=nav_options,
        index=0,
        key="main_navigation"
    )

    st.sidebar.markdown("<hr style='margin: 1.2rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
    
    # System Status Indicator in Sidebar
    st.sidebar.markdown(
        """
        <div style="font-size: 0.78rem; color: #64748b;">
            <div><strong>Backend Status:</strong> <span style="color: #22c55e;">● Active</span></div>
            <div><strong>Trained Models:</strong> Logistic Regression (Calibrated)</div>
            <div><strong>Dataset:</strong> 3,078 records verified</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load data for pages that require dataset
    data_required_pages = [
        "🏠 Dashboard",
        "📋 Feedback Explorer",
        "😊 Sentiment Analysis",
        "🏷️ Issue Analysis",
        "💡 Business Insights"
    ]

    df = None
    if selected_page in data_required_pages:
        try:
            df = load_data()
        except Exception as e:
            st.error(
                f"🚨 **Dataset Loading Error**: {str(e)}\n\n"
                "Please verify that `data/processed/cleaned_feedback.csv` exists or run `python src/preprocessing.py`."
            )
            return

    # Verify models can be loaded for prediction
    if selected_page == "🔮 Predict Feedback":
        try:
            load_all_models()
        except Exception as e:
            st.error(
                f"🚨 **Model Loading Error**: {str(e)}\n\n"
                "Please verify that trained models exist in `models/` or run the training pipeline."
            )
            return

    # Page Routing
    if selected_page == "🏠 Dashboard":
        dashboard.render(df, is_dark=is_dark)
    elif selected_page == "🔮 Predict Feedback":
        prediction.render(is_dark=is_dark)
    elif selected_page == "📋 Feedback Explorer":
        feedback_explorer.render(df, is_dark=is_dark)
    elif selected_page == "😊 Sentiment Analysis":
        sentiment_analysis.render(df, is_dark=is_dark)
    elif selected_page == "🏷️ Issue Analysis":
        issue_analysis.render(df, is_dark=is_dark)
    elif selected_page == "💡 Business Insights":
        business_insights.render(df, is_dark=is_dark)
    elif selected_page == "ℹ️ About":
        about.render(is_dark=is_dark)


if __name__ == "__main__":
    main()
