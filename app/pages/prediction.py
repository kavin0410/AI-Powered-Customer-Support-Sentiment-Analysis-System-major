"""
Prediction Page: Live single-text prediction engine with calibrated probabilities.
"""

import streamlit as st
from app.utils.model_loader import predict_input
from app.utils.validation import validate_feedback_text, determine_attention_level
from app.components.cards import render_prediction_card
from app.components.charts import plot_probabilities_bar


PRESET_EXAMPLES = [
    "--- Select an example scenario or type custom text below ---",
    "The package arrived broken, completely smashed during transit. Horrible courier service.",
    "I was charged twice on my credit card for the same order! Please refund my money immediately.",
    "Your live agent Sarah was so helpful and solved my issue within minutes. Truly wonderful support!",
    "The mobile app keeps crashing whenever I try to navigate to the checkout page.",
    "The product quality is excellent and I am very happy with my purchase.",
    "My order arrived three days late and the package was damaged.",
    "Money was deducted from my account but the payment failed.",
    "The customer service representative was very helpful.",
    "I received the wrong product.",
    "The delivery was completed on time.",
    "I would like to know more about your product."
]


def render(is_dark: bool = False):
    """Renders the real-time prediction and explanation interface."""
    st.markdown("## 🔮 Real-Time Customer Feedback Predictor")
    st.markdown("Analyze incoming customer reviews, tickets, or messages using the trained ML pipeline.")

    # Quick example dropdown
    selected_example = st.selectbox(
        "💡 Quick-Load Test Scenario (Optional)",
        options=PRESET_EXAMPLES,
        index=0,
        key="preset_selector"
    )

    default_text = ""
    if selected_example != PRESET_EXAMPLES[0]:
        default_text = selected_example

    # Text Area
    user_input = st.text_area(
        "Customer Feedback Text",
        value=default_text,
        height=140,
        placeholder="Enter customer feedback here... (e.g., 'My order arrived two days late and the package was damaged.')",
        help="Type or paste customer comments to run sentiment and issue category inference."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        predict_btn = st.button("🚀 PREDICT FEEDBACK", type="primary", use_container_width=True)
    with col2:
        if st.button("Clear Input"):
            st.rerun()

    if predict_btn:
        # 1. Input Validation
        is_valid, err_msg = validate_feedback_text(user_input)
        if not is_valid:
            st.error(f"⚠️ {err_msg}")
            return

        # 2. Run Inference
        try:
            with st.spinner("Analyzing text with machine learning models..."):
                result = predict_input(user_input)
        except Exception as e:
            st.error(f"Prediction Error: {str(e)}")
            return

        # 3. Compute Attention Level
        attention = determine_attention_level(
            sentiment=result["sentiment"],
            sentiment_conf=result["sentiment_confidence"],
            issue_category=result["issue_category"]
        )

        # 4. Display Result Card
        render_prediction_card(
            feedback=user_input.strip(),
            sentiment=result["sentiment"],
            sentiment_conf=result["sentiment_confidence"],
            issue=result["issue_category"],
            issue_conf=result["issue_confidence"],
            attention_info=attention,
            is_dark=is_dark
        )

        st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

        # 5. Probability Breakdown Visualizations
        st.markdown("### 📊 Model Calibrated Class Probabilities")
        st.markdown(
            "Confidence values represent authentic posterior class probabilities computed from the model's decision function."
        )

        prob_col1, prob_col2 = st.columns(2)
        with prob_col1:
            fig_sent = plot_probabilities_bar(
                result["sentiment_probabilities"],
                title="Sentiment Class Probabilities",
                is_dark=is_dark
            )
            st.plotly_chart(fig_sent, use_container_width=True)

        with prob_col2:
            fig_issue = plot_probabilities_bar(
                result["issue_probabilities"],
                title="Issue Category Class Probabilities",
                is_dark=is_dark
            )
            st.plotly_chart(fig_issue, use_container_width=True)
