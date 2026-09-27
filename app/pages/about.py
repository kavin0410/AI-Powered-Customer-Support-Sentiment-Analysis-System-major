"""
About Page: Architectural documentation, problem statement, technical stack, and engineering workflow.
"""

import streamlit as st
from app.components.cards import render_card


def render(is_dark: bool = False):
    """Renders the comprehensive project documentation and technical overview."""
    st.markdown("## ℹ️ About the Project")
    st.markdown("### AI-Powered Customer Support & Sentiment Analysis System")

    # Workflow Diagram
    st.markdown("#### 🔄 End-to-End System Workflow")
    workflow_html = f"""
    <div style="
        background-color: {'#1e293b' if is_dark else '#f8fafc'};
        padding: 1.25rem;
        border-radius: 10px;
        border: 1px solid {'#334155' if is_dark else '#e2e8f0'};
        margin-bottom: 1.5rem;
        text-align: center;
        font-family: monospace;
        font-size: 0.95rem;
        font-weight: 600;
        color: {'#f8fafc' if is_dark else '#0f172a'};
    ">
        <span style="color: #6366f1;">Raw Feedback Data</span> ➔ 
        <span style="color: #0ea5e9;">Text Preprocessing</span> ➔ 
        <span style="color: #14b8a6;">TF-IDF Feature Extraction</span> ➔ 
        <span style="color: #22c55e;">Calibrated ML Models</span> ➔ 
        <span style="color: #eab308;">Inference Engine</span> ➔ 
        <span style="color: #f97316;">Interactive Analytics</span> ➔ 
        <span style="color: #ec4899;">Business Insights</span>
    </div>
    """
    st.markdown(workflow_html, unsafe_allow_html=True)

    # Project Overview Cards
    col1, col2 = st.columns(2)
    with col1:
        render_card(
            title="🎯 Problem Statement",
            content=(
                "Customer support operations are overwhelmed by heterogeneous feedback streams across "
                "e-commerce, web, and mobile channels. Manual review of feedback delays critical resolutions, "
                "risks customer churn, and conceals systemic operational defects."
            ),
            border_color="#6366f1",
            is_dark=is_dark
        )
        render_card(
            title="🚀 System Objectives",
            content=(
                "<ul>"
                "<li>Classify customer sentiment (Positive, Negative, Neutral) in real time.</li>"
                "<li>Categorize customer issues into 6 operational domains (Product, Delivery, Payment, Technical, Service, General).</li>"
                "<li>Generate calibrated posterior probabilities for reliable confidence scoring.</li>"
                "<li>Provide executive dashboards, search explorers, and automated business insights.</li>"
                "</ul>"
            ),
            border_color="#0ea5e9",
            is_dark=is_dark
        )

    with col2:
        render_card(
            title="🛠️ Technology Stack",
            content=(
                "<ul>"
                "<li><strong>Core ML:</strong> Scikit-learn, NLTK (WordNet, Stopwords), NumPy, SciPy</li>"
                "<li><strong>Data Processing:</strong> Pandas 3.0, Joblib</li>"
                "<li><strong>Visualization:</strong> Plotly Express & Graph Objects</li>"
                "<li><strong>Web Framework:</strong> Streamlit 1.53</li>"
                "<li><strong>Testing Suite:</strong> Pytest</li>"
                "</ul>"
            ),
            border_color="#10b981",
            is_dark=is_dark
        )
        render_card(
            title="🧠 Machine Learning Architectures",
            content=(
                "<ul>"
                "<li><strong>Benchmarked Architectures:</strong> Logistic Regression, Multinomial Naive Bayes, Linear SVM (Calibrated), Random Forest.</li>"
                "<li><strong>Selected Primary Model:</strong> Logistic Regression Pipeline with TF-IDF n-grams (1, 2) and sublinear scaling.</li>"
                "<li><strong>Calibration:</strong> Genuine multinomial posterior probability distributions.</li>"
                "</ul>"
            ),
            border_color="#8b5cf6",
            is_dark=is_dark
        )

    st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

    # Major Modules Breakdown
    st.markdown("#### 📦 Major Application Modules")
    tabs = st.tabs(["1. Preprocessing", "2. Prediction Engine", "3. Analytics & Insights", "4. Team Information"])

    with tabs[0]:
        st.markdown(
            """
            - **URL & Email Filtering:** Removes web noise without welding adjacent words.
            - **Contraction Normalization:** Expands contractions to explicitly preserve semantic negations (`wasn't` -> `was not`).
            - **Negation-Preserving Stopwords:** Retains 28 critical sentiment words (`not`, `never`, `barely`, `without`).
            - **WordNet Lemmatization:** Morphological reduction to base root forms.
            """
        )

    with tabs[1]:
        st.markdown(
            """
            - **Dual-Task Inference:** Simultaneously predicts Sentiment and Issue Category in a single pass.
            - **Calibrated Confidences:** Probability outputs derived from genuine model posterior distributions.
            - **Attention Triage:** Transparent rules routing urgent tickets to immediate specialist attention.
            """
        )

    with tabs[2]:
        st.markdown(
            """
            - **Real-Time Cross-Tabs:** Dynamic computation of sentiment breakdowns across issue categories.
            - **Temporal Trajectory:** Tracking monthly feedback surges and category velocity.
            - **Automated Observation Extraction:** Rigorous separation of statistical data observations and actionable business remedies.
            """
        )

    with tabs[3]:
        st.markdown(
            """
            **Project Engineering & Demonstration:**
            - **Role:** Lead Machine Learning Engineer
            - **Institution / Department:** Major Academic Capstone Project
            - **Project Status:** Phase 1 (ML Foundation) & Phase 2 (Interactive Web Application) Complete
            """
        )
