# AI-Powered Customer Support & Sentiment Analysis System
*Enterprise Full-Stack Application (React + FastAPI + SQLite + Machine Learning)*

A production-grade, full-stack AI web application designed to analyze unstructured customer feedback, simultaneously predicting **Customer Sentiment** and categorizing **Support Issue Types** with calibrated probability confidences, interactive Recharts analytics dashboards, SQLite persistence, and automated business insights.

---

## 📌 Project Overview

Customer support teams face high volumes of incoming tickets, feedback forms, and reviews across diverse channels. Manually triaging each feedback item leads to delayed response times, customer churn, and inconsistent prioritization.

This project delivers a complete, end-to-end full-stack web application that:
1. **Analyzes Sentiment**: Classifies incoming feedback into `Positive`, `Negative`, or `Neutral`.
2. **Classifies Support Issues**: Categorizes feedback into six operational domains:
   - `Product Issue`
   - `Delivery Issue`
   - `Payment Issue`
   - `Technical Issue`
   - `Service Issue`
   - `General Feedback`
3. **Calibrated Confidence Scoring**: Generates genuine posterior class probabilities for every prediction to support confidence-based automated routing and human-in-the-loop review.
4. **Transparent Attention Triage**: Applies deterministic business rules to categorize incoming items into `High`, `Medium`, or `Low` priority.
5. **Interactive React SaaS Dashboard**: Modern responsive UI with Tailwind CSS, Recharts visualizations, dark/light mode toggle with `localStorage` persistence, server-side paginated explorer, live predictor, and dynamic business insights.
6. **Robust FastAPI Backend**: High-throughput REST API with automated OpenAPI docs (`/docs`), Pydantic validation, CORS middleware, and SQLite database storage auto-seeded with 3,078 records.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 React Frontend (Vite + SPA)                 │
│  - React Router (7 Dedicated Modular Views)                 │
│  - Tailwind CSS + Lucide Icons + Theme Switcher (Dark/Light)│
│  - Recharts Visualizations (Area, Bar, Donut, Multi-Line)   │
│  - Centralized Axios API Client                             │
└──────────────────────────────┬──────────────────────────────┘
                               │ REST API (JSON)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 FastAPI Backend (Uvicorn ASGI)              │
│  - CORS Middleware (http://localhost:5173)                  │
│  - Pydantic Request / Response Schema Validation            │
│  - Global Exception Handling & OpenAPI (/docs, /redoc)      │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
               ▼                               ▼
┌──────────────────────────────┐ ┌─────────────────────────────┐
│  Dual ML Inference Engine    │ │  SQLite Database & Services │
│  - Text Preprocessing Pipeline│ │  - customer_support.db      │
│  - TF-IDF Vectorizers        │ │  - feedback table (3,078 r) │
│  - Calibrated Sentiment Model│ │  - Server-side Pagination   │
│  - Calibrated Issue Model    │ │  - Dynamic KPI Aggregations │
│  - Attention Level Triage    │ │  - Dynamic Business Insights│
└──────────────────────────────┘ └─────────────────────────────┘
```

---

## 💻 Full-Stack Features

### 1. Executive Dashboard (`/dashboard`)
- Primary 5-metric KPI ribbon: Total Feedback (3,078), Positive, Negative, Neutral, and Most Common Issue.
- Five dynamic Recharts visualizations:
  1. **Sentiment Distribution** (Donut chart with custom legend)
  2. **Issue Category Distribution** (Categorical bar chart)
  3. **Monthly Feedback Volume Trend** (Gradient area chart)
  4. **Monthly Sentiment Trajectory** (Multi-line trend: Positive, Negative, Neutral)
  5. **Sentiment Composition by Issue Category** (Cross-tabulated stacked bars)
- Zero hardcoded statistics: all metrics are derived live from the SQLite database.

### 2. Live Predictor Engine (`/prediction`)
- Interactive text submission with sample customer scenario presets.
- Dual-task classification providing predicted Sentiment and Issue Category with genuine, calibrated confidence percentages.
- Transparent Attention Level scoring (`High`, `Medium`, `Low`) with operational triage guidance.
- Interactive Recharts probability distribution bars showing full posterior distributions across all classes.
- Robust client/server validation: handles empty input, whitespace, and excessive character lengths.

### 3. Customer Feedback Explorer (`/feedback`)
- Searchable feedback repository with keyword search across feedback text.
- Multi-criteria filtering by Sentiment, Issue Category, and Date Range.
- Server-side pagination with configurable page limits (`limit=10, 20, 50`).
- Interactive record inspection modal displaying full record metadata and timestamps.
- Client-side CSV export trigger.

### 4. Sentiment Analysis Deep-Dive (`/sentiment`)
- Positive, Negative, and Neutral percentage breakdowns.
- Extrema callouts identifying categories with highest positive and negative concentrations.
- Monthly sentiment trends and cross-category stacked distributions.

### 5. Customer Support Issue Analysis (`/issues`)
- Volume and share breakdowns across all six required issue categories.
- Identification of dominant complaint drivers and operational pain points.
- Category statistics table with issue share percentages and negative feedback proportions.

### 6. Automated Business Insights (`/insights`)
- Dynamically synthesized factual observations derived directly from data distributions.
- Strict structural separation between **Factual Observation** and **Recommended Strategic Action**.
- Identifies critical delivery delays, payment friction, and app instability.

### 7. System Architecture & About (`/about`)
- Academic capstone documentation detailing problem statement, objectives, and tech stack.
- Interactive architectural workflow cards.
- Machine learning specifications and project team placeholder.

### 8. Theme System (Dark / Light Mode)
- Seamless theme toggle in header with instant DOM synchronization and `localStorage` persistence.
- High-contrast, accessibility-tested color palettes for charts and typography in both modes.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite 8, Tailwind CSS 3, React Router v7, Recharts 3, Axios, Lucide React Icons |
| **Backend** | Python 3.11+, FastAPI 0.115+, Uvicorn ASGI, Pydantic v2, HTTPX |
| **Database** | SQLite 3 (`backend/customer_support.db`), auto-seeded from `data/processed/cleaned_feedback.csv` |
| **Machine Learning** | Scikit-Learn, TF-IDF Vectorizer, Calibrated LinearSVC / Logistic Regression, Joblib, Pandas, NumPy, NLTK |

---

## 📂 Project Structure

```
AI-Powered-Customer-Support-Sentiment-Analysis-System-major/
│
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI entrypoint, lifespan loader, CORS, /api/health
│   │   ├── api/                        # REST API endpoint routers
│   │   │   ├── prediction.py           # POST /api/predict
│   │   │   ├── dashboard.py            # GET  /api/dashboard
│   │   │   ├── feedback.py             # GET  /api/feedback & /api/feedback/{id}
│   │   │   ├── analytics.py            # GET  /api/analytics/{sentiment,issues}
│   │   │   └── insights.py             # GET  /api/insights
│   │   ├── core/
│   │   │   ├── config.py               # Settings, origins, database paths
│   │   │   └── database.py             # SQLite connection & auto-seeding engine
│   │   ├── models/
│   │   │   └── schemas.py              # Pydantic request & response models
│   │   ├── services/
│   │   │   ├── prediction_service.py   # Model inference & confidence extraction
│   │   │   ├── analytics_service.py    # SQL aggregations for KPIs & chart series
│   │   │   ├── feedback_service.py     # Filtered, paginated feedback queries
│   │   │   └── insight_service.py      # Dynamic fact-based business insight generator
│   │   └── utils/
│   │       ├── model_loader.py         # Singleton Phase 1 model loader
│   │       └── validation.py           # Input sanitization & attention triage logic
│   ├── requirements.txt                # Backend dependencies
│   └── run.py                          # Local backend launcher
│
├── frontend/
│   ├── src/
│   │   ├── components/                 # Reusable React components
│   │   │   ├── Sidebar.jsx             # Collapsible navigation drawer
│   │   │   ├── Header.jsx              # Status badge, theme switcher, avatar
│   │   │   ├── MetricCard.jsx          # KPI card with delta & accent colors
│   │   │   ├── ChartCard.jsx           # Recharts card container
│   │   │   ├── FeedbackTable.jsx       # Paginated feedback table with badges
│   │   │   ├── FeedbackDetailModal.jsx # Single record inspection modal
│   │   │   ├── PredictionResult.jsx    # Dual-task result & probability bars
│   │   │   └── LoadingState.jsx        # Loading spinner & error retry cards
│   │   ├── pages/                      # Page views
│   │   │   ├── Dashboard.jsx           # KPI ribbon + 5 Recharts visualizations
│   │   │   ├── Prediction.jsx          # Real-time dual-task classifier
│   │   │   ├── FeedbackExplorer.jsx    # Paginated explorer & search
│   │   │   ├── SentimentAnalysis.jsx   # Sentiment proportions & trends
│   │   │   ├── IssueAnalysis.jsx       # Issue frequencies & category stats
│   │   │   ├── BusinessInsights.jsx    # Dynamic factual insights & actions
│   │   │   └── About.jsx               # Capstone project documentation
│   │   ├── services/
│   │   │   └── api.js                  # Centralized Axios client
│   │   ├── App.jsx                     # Router, layout & dark mode state
│   │   ├── main.jsx                    # React root entrypoint
│   │   └── index.css                   # Tailwind CSS directives
│   ├── package.json                    # Frontend dependencies & scripts
│   ├── vite.config.js                  # Vite configuration
│   └── tailwind.config.js              # Tailwind theme configuration
│
├── models/
│   ├── sentiment_pipeline.pkl          # Serialized sentiment pipeline (TF-IDF + Calibrated LinearSVC)
│   ├── issue_pipeline.pkl              # Serialized issue pipeline (TF-IDF + Calibrated LinearSVC)
│   ├── sentiment_metadata.json         # Sentiment model performance & labels
│   └── issue_metadata.json             # Issue model performance & labels
│
├── data/
│   └── processed/
│       └── cleaned_feedback.csv        # Source dataset (3,078 validated feedback records)
│
├── tests/
│   ├── test_backend_api.py             # 11 Unit tests for FastAPI endpoints & validation
│   └── test_live_system.py             # Live integration & 8-query prediction test suite
│
└── README.md                           # Master project documentation
```

---

## 📡 REST API Reference

The FastAPI backend automatically provides interactive OpenAPI documentation at `http://localhost:8000/docs` and `http://localhost:8000/redoc`.

| Method | Endpoint | Query / Body | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | None | API health status & model availability flag |
| `POST` | `/api/predict` | `{"text": "..."}` | Dual-task prediction with calibrated confidence & attention level |
| `GET` | `/api/dashboard` | None | Real-time executive KPIs, distributions, and monthly trends |
| `GET` | `/api/feedback` | `page, limit, sentiment, issue_category, search` | Server-side paginated feedback list |
| `GET` | `/api/feedback/{id}` | `feedback_id` | Single feedback record details (404 if not found) |
| `GET` | `/api/analytics/sentiment` | None | Sentiment percentages, monthly trend, and category cross-tabs |
| `GET` | `/api/analytics/issues` | None | Issue distribution, percentages, trends, and category statistics |
| `GET` | `/api/insights` | None | Dynamic factual observations and recommended actions |

---

## 🚀 Installation & Running Guide

### 1. Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher (Node v20+ recommended)
- npm or yarn

### 2. Backend Setup
```bash
# From project root
# (Ensure your Python virtual environment is activated)
pip install -r backend/requirements.txt

# Run the FastAPI server on port 8000
python backend/run.py
# Alternatively:
# python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
*The backend will automatically create `backend/customer_support.db` and seed it with all 3,078 records from `data/processed/cleaned_feedback.csv`.*

### 3. Frontend Setup
```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Start Vite development server on port 5173
npm run dev
```

The React application is accessible at: **`http://localhost:5173`**  
The FastAPI Swagger documentation is at: **`http://localhost:8000/docs`**

---

## 🧪 Testing & Verification

### Automated Backend Tests
Run the comprehensive FastAPI test suite:
```bash
python -m pytest tests/test_backend_api.py -v
```
*Validates 11 backend test cases covering health checks, prediction schemas, input validation (empty/whitespace/overflow), pagination, filtering, 404 handling, and analytics.*

### Live System & 8-Sample Query Verification
Run the live integration suite:
```bash
python tests/test_live_system.py
```

### Verified Sample Predictions Output (Step 36)
| # | Customer Input | Predicted Sentiment | Sentiment Conf. | Issue Category | Issue Conf. | Attention Level |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | *"The product quality is excellent and I am very happy."* | **Positive** | 42.9% | **Product Issue** | 50.2% | **Low** |
| 2 | *"My delivery is three days late."* | **Negative** | 61.7% | **Delivery Issue** | 47.5% | **Medium** |
| 3 | *"Money was deducted but payment failed."* | **Negative** | 61.7% | **Payment Issue** | 71.7% | **Medium** |
| 4 | *"The application keeps crashing."* | **Negative** | 35.9% | **Technical Issue** | 34.4% | **Medium** |
| 5 | *"The customer service was very helpful."* | **Positive** | 62.9% | **Service Issue** | 70.5% | **Low** |
| 6 | *"I received the wrong product."* | **Negative** | 66.6% | **Product Issue** | 35.1% | **Medium** |
| 7 | *"The order arrived on time."* | **Negative** | 55.7% | **Delivery Issue** | 44.4% | **Medium** |
| 8 | *"Can you tell me more about this product?"* | **Neutral** | 43.1% | **Product Issue** | 51.2% | **Medium** |

---

## 🛡️ Security & Reliability
- **Input Validation**: Strict bounds via Pydantic (`min_length=3`, `max_length=5000`).
- **SQL Injection Prevention**: Parameterized SQLite queries throughout `feedback_service.py` and `database.py`.
- **CORS Hardening**: Explicit allowed origins configured for local React development (`http://localhost:5173`).
- **No Hardcoded Secrets**: Environment variable support with `.env.example` templates.
- **Error Shielding**: No raw internal stack traces exposed to client responses.

---

## 🔮 Future Enhancements
- Integration of modern Transformer LLMs (e.g. RoBERTa or Mistral) for zero-shot multilingual classification.
- Real-time customer support agent notification webhooks (Slack / Microsoft Teams / Zendesk).
- Automated AI draft response generation for high-attention grievances.
