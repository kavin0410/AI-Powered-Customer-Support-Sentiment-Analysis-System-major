"""
Reusable Card and Callout UI components.
"""

import streamlit as st


def render_card(title: str, content: str, subtitle: str = "", border_color: str = "#4e73df", is_dark: bool = False):
    """Renders a styled card with optional left accent border."""
    bg_color = "#1e2430" if is_dark else "#ffffff"
    text_color = "#f8f9fa" if is_dark else "#2c3e50"
    sub_color = "#a0aec0" if is_dark else "#6c757d"
    border_subtle = "#2d3748" if is_dark else "#e2e8f0"

    html = f"""
    <div style="
        background-color: {bg_color};
        padding: 1.25rem;
        border-radius: 10px;
        border: 1px solid {border_subtle};
        border-left: 5px solid {border_color};
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    ">
        <h4 style="margin: 0 0 0.4rem 0; color: {text_color}; font-size: 1.1rem; font-weight: 600;">{title}</h4>
        {f'<p style="margin: 0 0 0.5rem 0; color: {sub_color}; font-size: 0.85rem;">{subtitle}</p>' if subtitle else ''}
        <div style="color: {text_color}; font-size: 0.95rem; line-height: 1.5;">{content}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_prediction_card(
    feedback: str,
    sentiment: str,
    sentiment_conf: float,
    issue: str,
    issue_conf: float,
    attention_info: dict,
    is_dark: bool = False
):
    """Renders a structured, high-impact prediction result display card."""
    bg_color = "#1a202c" if is_dark else "#f8fafc"
    card_bg = "#2d3748" if is_dark else "#ffffff"
    text_color = "#f7fafc" if is_dark else "#1a202c"
    sub_color = "#a0aec0" if is_dark else "#64748b"

    sent_color = "#2ecc71" if sentiment == "Positive" else ("#e74c3c" if sentiment == "Negative" else "#3498db")
    
    html = f"""
    <div style="background-color: {card_bg}; padding: 1.5rem; border-radius: 12px; border: 1px solid {'#4a5568' if is_dark else '#e2e8f0'}; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-top: 1rem;">
        <div style="font-size: 0.85rem; color: {sub_color}; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; margin-bottom: 0.5rem;">
            Customer Feedback Submitted
        </div>
        <div style="font-size: 1.05rem; font-style: italic; color: {text_color}; margin-bottom: 1.25rem; padding: 0.75rem 1rem; background-color: {bg_color}; border-radius: 8px; border-left: 4px solid #6366f1;">
            "{feedback}"
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem;">
            <div style="padding: 1rem; background-color: {bg_color}; border-radius: 8px; border-top: 4px solid {sent_color};">
                <div style="font-size: 0.8rem; color: {sub_color}; font-weight: 600;">PREDICTED SENTIMENT</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: {sent_color};">{sentiment}</div>
                <div style="font-size: 0.9rem; color: {text_color};">Model Confidence: <strong>{sentiment_conf:.1%}</strong></div>
            </div>
            
            <div style="padding: 1rem; background-color: {bg_color}; border-radius: 8px; border-top: 4px solid #8b5cf6;">
                <div style="font-size: 0.8rem; color: {sub_color}; font-weight: 600;">ISSUE CATEGORY</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #8b5cf6;">{issue}</div>
                <div style="font-size: 0.9rem; color: {text_color};">Model Confidence: <strong>{issue_conf:.1%}</strong></div>
            </div>
        </div>

        <div style="padding: 1rem; background-color: {bg_color}; border-radius: 8px; border-left: 5px solid {attention_info['color']};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                <span style="font-weight: 700; color: {attention_info['color']}; font-size: 1.05rem;">{attention_info['badge']}</span>
            </div>
            <div style="font-size: 0.9rem; color: {text_color}; margin-bottom: 0.4rem;">
                <strong>Explanation:</strong> {attention_info['explanation']}
            </div>
            <div style="font-size: 0.9rem; color: {text_color};">
                <strong>Recommended Action:</strong> {attention_info['action']}
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
