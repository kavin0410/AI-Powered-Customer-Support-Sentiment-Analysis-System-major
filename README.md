# AI-Powered Customer Support & Sentiment Analysis System
*Enterprise Full-Stack Machine Learning Web Application (React + FastAPI + SQLite + Calibrated Scikit-Learn)*

A production-grade, full-stack artificial intelligence application designed to ingest and analyze unstructured customer feedback, simultaneously predicting **Customer Sentiment** and categorizing **Support Issue Types** with calibrated probability confidences, interactive Recharts analytics dashboards, SQLite persistence, automated business insights, and dark/light theme support.

---

## 1. Abstract
Customer support operations across modern digital businesses face an overwhelming volume of feedback. The unstructured nature of this communication creates severe triage bottlenecks: high manual latency, misrouted tickets, and delayed identification of critical outages. This major capstone project delivers an end-to-end full-stack intelligence system combining Natural Language Processing (NLP), calibrated supervised machine learning algorithms, high-throughput asynchronous REST APIs (FastAPI), relational persistence (SQLite), and a responsive Single Page Application (React 18 + Vite + Tailwind CSS + Recharts). Incoming feedback is categorized into 3 sentiment classes and 6 operational domains with posterior class probabilities and actionable triage priority rules (`High`, `Medium`, `Low`).

---

## 2. Problem Statement
1. **Manual Triage Delays:** Human review of every support ticket creates hours of response latency during traffic spikes.
2. **Inconsistent Routing:** Subjective human categorizations result in departmental misrouting and repeated ticket transfers.
3. **Lack of Calibrated Confidence:** Legacy keyword-based engines produce binary flags without posterior probability distributions, preventing automated confidence-based escalation.
4. **Information Silos:** Support metrics are rarely cross-tabulated with operational departments in real time.
5. **Rigid Interfaces:** Outdated tooling lacks modern responsive dashboards, accessibility, and theme adaptability.

---

## 3. Objectives
- Curate and preprocess a comprehensive dataset of customer interactions without data leakage.
- Build an NLP pipeline preserving negation semantics (`"not"`, `"never"`) and expanding contractions.
- Train, benchmark, and serialize dual-task supervised classifiers with calibrated probabilities.
- Develop an asynchronous FastAPI backend with strict Pydantic v2 schemas and OpenAPI documentation.
- Implement an indexed SQLite database auto-seeded with 3,078 customer feedback records.
- Construct a responsive React 18 single-page application with dark/light mode and interactive Recharts visualizations.
- Validate the system with exhaustive automated test suites and containerized deployment scripts.

---

## 4. Features
- **Dual-Task AI Inference:** Simultaneous sentiment scoring (Positive, Negative, Neutral) and operational issue categorization (6 classes).
- **Calibrated Probabilities:** True posterior class distribution computed for every prediction.
- **Attention Level Triage:** Deterministic rule-based priority scoring (`High`, `Medium`, `Low`) for agent escalation.
- **Executive KPI Dashboard:** Real-time metrics ribbon and 5 interactive Recharts visualizations.
- **Interactive Predictor:** Real-time feedback submission workbench with scenario presets and probability bars.
- **Feedback Explorer:** Server-side paginated repository with live search, multi-criteria filtering, and detail modal.
- **Automated Business Insights:** Data-driven factual observations structurally separated from recommended actions.
- **Theme Switcher:** High-contrast Dark and Light themes persisted via `localStorage`.

---

## 5. System Architecture
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

## 6. Technology Stack
- **Frontend:** React 18, Vite 8, Tailwind CSS 3, React Router v7, Recharts 3, Axios, Lucide React Icons.
- **Backend:** Python 3.11+, FastAPI, Uvicorn ASGI, Pydantic v2, HTTPX.
- **Database:** SQLite 3 (`backend/customer_support.db`), auto-seeded and indexed.
- **Machine Learning:** Scikit-Learn, TF-IDF Vectorizer, Calibrated LinearSVC, Logistic Regression, Joblib, Pandas, NumPy, NLTK.
- **DevOps:** Docker, Docker Compose, NGINX.

---

## 7. Dataset
- **Volume:** 3,078 validated customer interaction records.
- **Attributes:** `feedback_id`, `feedback_text`, `sentiment`, `issue_category`, `date`.
- **Sentiment Breakdown:** Negative (1,393 / 45.3%), Positive (1,080 / 35.1%), Neutral (605 / 19.6%).
- **Issue Distribution:** Product Issue (734), Delivery Issue (617), Payment Issue (485), Service Issue (463), Technical Issue (460), General Feedback (319).

---

## 8. Data Preprocessing
- **Case Normalization:** Standardizing tokens to lowercase.
- **Noise Sanitization:** Stripping URLs, email addresses, and non-alphanumeric punctuation.
- **Contraction Expansion:** Expanding informal contractions (`"can't"` $\rightarrow$ `"cannot"`, `"wasn't"` $\rightarrow$ `"was not"`).
- **Negation Preservation:** Whitelisting critical negation words (`"not"`, `"never"`, `"no"`, `"without"`) to prevent polarity inversion.
- **Lemmatization:** Converting nouns and verbs to canonical roots using NLTK `WordNetLemmatizer`.

---

## 9. Sentiment Analysis
- **Classes:** Positive, Negative, Neutral.
- **Vectorization:** Sublinear TF-IDF with unigram and bigram representation (`ngram_range=(1, 2)`).
- **Selected Model:** Logistic Regression with L2 regularization and calibrated Platt scaling.
- **Test Performance (N=616):** Accuracy: 1.0000, Macro F1: 1.0000, Weighted F1: 1.0000.

---

## 10. Issue Classification
- **Classes (6 domains):** Product Issue, Delivery Issue, Payment Issue, Technical Issue, Service Issue, General Feedback.
- **Selected Model:** Logistic Regression with sublinear TF-IDF vectorization.
- **Test Performance (N=616):** Accuracy: 1.0000, Macro F1: 1.0000, Weighted F1: 1.0000.

---

## 11. Model Comparison

### Sentiment Analysis Benchmark (Test Set, N=616)
| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Selected |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression + TF-IDF** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **Yes (Best)** |
| Multinomial Naive Bayes + TF-IDF | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | - |
| Linear SVM (Calibrated) + TF-IDF | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | - |
| Random Forest + TF-IDF | 0.9399 | 0.9570 | 0.9332 | 0.9422 | 0.9397 | - |

### Customer Issue Classification Benchmark (Test Set, N=616)
| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Selected |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression + TF-IDF** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **Yes (Best)** |
| Multinomial Naive Bayes + TF-IDF | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | - |
| Linear SVM (Calibrated) + TF-IDF | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | - |
| Random Forest + TF-IDF | 0.9903 | 0.9935 | 0.9891 | 0.9910 | 0.9902 | - |

---

## 12. Model Evaluation
- Zero data leakage: vectorizers fitted strictly on training data.
- True posterior class probabilities validated with `.predict_proba()`.
- Classification reports and confusion matrices stored in `models/` and `reports/figures/`.

---

## 13. Backend
- Built on FastAPI with Uvicorn ASGI runner.
- Modular architecture: `api/`, `core/`, `models/`, `services/`, `utils/`.
- Centralized exception handlers preventing stack trace and file path exposure.
- Structured logging with INFO, WARNING, and ERROR levels.
- Pre-loads ML pipelines once on startup into thread-safe singleton memory cache.

---

## 14. Frontend
- Built on React 18 and Vite with SPA client routing via React Router v7.
- Responsive SaaS layout with collapsible sidebar for mobile and tablet devices.
- Reusable UI component library with semantic color badges and accessibility indicators.
- Dark and Light mode styling with persistent `localStorage` synchronization.

---

## 15. Database
- SQLite 3 (`backend/customer_support.db`).
- Table: `feedback` (`id`, `feedback_id`, `feedback_text`, `sentiment`, `issue_category`, `feedback_date`, `created_at`).
- Indexes: `idx_feedback_sentiment`, `idx_feedback_category`, `idx_feedback_date`.
- Seeding: Automated on startup from `data/processed/cleaned_feedback.csv` (3,078 records) or via `backend/scripts/import_data.py`.

---

## 16. API Endpoints
All endpoints are available with OpenAPI documentation at `http://localhost:8000/docs`:

| Method | Endpoint | Query / Body | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | None | API health status & model availability |
| `POST` | `/api/predict` | `{"text": "..."}` | Dual-task prediction with calibrated confidence & attention level |
| `GET` | `/api/dashboard` | None | Executive KPIs, distributions, and monthly trends |
| `GET` | `/api/feedback` | `page, limit, sentiment, issue_category, search` | Server-side paginated feedback list |
| `GET` | `/api/feedback/{id}` | `feedback_id` | Single feedback record details (404 on missing ID) |
| `GET` | `/api/analytics/sentiment` | None | Sentiment percentages, trends, and category cross-tabs |
| `GET` | `/api/analytics/issues` | None | Issue distribution, percentages, and category statistics |
| `GET` | `/api/insights` | None | Dynamic factual observations and recommended actions |

---

## 17. Dashboard
- 5 Executive KPI cards: Total Feedback (3,078), Positive, Negative, Neutral, Top Issue.
- 5 Dynamic Recharts Charts: Sentiment Donut, Issue Bar, Monthly Volume Area, Sentiment Trend Lines, Sentiment vs Issue Stacked Bars.
- Dynamic data binding with zero hardcoded values.

---

## 18. Prediction Workflow
1. User enters feedback text or selects a scenario preset.
2. Client sends request to `POST /api/predict`.
3. Backend preprocesses text, evaluates both models, and computes attention triage:
   - Negative & Conf $\ge 0.60 \implies$ **High Attention**
   - Negative & Conf $< 0.60 \implies$ **Medium Attention**
   - Neutral $\implies$ **Medium Attention**
   - Positive $\implies$ **Low Attention**
4. UI renders sentiment badge, issue category badge, attention card, explanation, and interactive probability distribution bars.

---

## 19. Business Insights
- Dynamically synthesized factual observations derived from real data.
- Strict separation between **Data Observation** and **Recommended Strategic Action**.
- Identifies critical delivery delays, payment friction, and app instability without fabricated claims.

---

## 20. Installation

### Prerequisites
- Python 3.11+
- Node.js 18+ (Node 20+ recommended)
- npm or yarn

### Step-by-Step Installation
```bash
# Clone the repository
git clone https://github.com/kavin0410/AI-Powered-Customer-Support-Sentiment-Analysis-System-major.git
cd AI-Powered-Customer-Support-Sentiment-Analysis-System-major

# Set up Python virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

---

## 21. Running the Backend
```bash
# From workspace root
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
# Alternatively:
python backend/run.py
```
- API Base URL: `http://localhost:8000`
- Interactive Swagger Documentation: `http://localhost:8000/docs`

---

## 22. Running the Frontend
```bash
# In a separate terminal, navigate to frontend
cd frontend
npm run dev
# or
node ./node_modules/vite/bin/vite.js --host 0.0.0.0 --port 5173
```
- Frontend Web App: `http://localhost:5173`

---

## 23. Testing
Execute the complete test suite (38 automated tests):
```bash
# Run all tests
python -m pytest tests/backend tests/ml -v

# Run live system integration test & sample predictions
python tests/test_live_system.py
```
*All 38 unit and integration tests pass with 100% success rate.*

---

## 24. Project Structure
```
AI-Powered-Customer-Support-Sentiment-Analysis-System-major/
│
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI entrypoint, lifespan loader, CORS, /api/health
│   │   ├── api/                        # REST API endpoint routers
│   │   ├── core/                       # Database manager & configuration
│   │   ├── models/                     # Pydantic schemas
│   │   ├── services/                   # Business logic & inference services
│   │   └── utils/                      # Model loader & attention validation
│   ├── scripts/
│   │   └── import_data.py              # Standalone SQLite dataset import pipeline
│   ├── Dockerfile                      # Production backend container definition
│   └── requirements.txt                # Backend runtime dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/                 # UI components (Header, Sidebar, Cards, Modal, Table)
│   │   ├── pages/                      # 7 Application views
│   │   ├── services/api.js             # Central Axios client
│   │   ├── App.jsx                     # Application router & theme state
│   │   └── index.css                   # Tailwind base directives
│   ├── Dockerfile                      # Multi-stage production frontend container
│   └── package.json                    # Frontend dependencies & scripts
│
├── data/
│   └── processed/cleaned_feedback.csv  # 3,078 validated feedback records
│
├── models/
│   ├── sentiment_pipeline.pkl          # Serialized sentiment pipeline
│   ├── issue_pipeline.pkl              # Serialized issue pipeline
│   ├── sentiment_metadata.json         # Performance metrics & classes
│   └── issue_metadata.json             # Performance metrics & classes
│
├── docs/                               # 20 Academic Capstone Documentation files
│
├── reports/
│   ├── sample_predictions.csv          # 24 verified real customer prediction inferences
│   └── figures/                        # High-resolution confusion matrices & charts
│
├── tests/
│   ├── backend/                        # Backend API test suite (13 tests)
│   ├── ml/                             # Machine learning test suite (25 tests)
│   └── test_live_system.py             # Live HTTP integration runner
│
├── docker-compose.yml                  # Containerized multi-service deployment
├── .env.example                        # Environment variables template
├── .gitignore                          # Git exclusions
└── README.md                           # Master project documentation
```

---

## 25. Limitations
- Current preprocessing and lemmatization pipeline is specialized for English text.
- Operational issue classification is bounded to six predefined enterprise categories.
- Figurative irony or subtle sarcasm may pose challenges for linear TF-IDF models.
- SQLite is optimal for single-node setups; distributed enterprise environments recommend PostgreSQL.

---

## 26. Future Enhancements
- Integration of Transformer LLMs (e.g. RoBERTa or fine-tuned Mistral-7B) for multi-lingual zero-shot classification.
- Real-time agent webhook connectors (Slack, Zendesk, Salesforce Service Cloud).
- Generative AI-assisted response drafting for customer support agents.
- Human-in-the-loop active learning feedback mechanism.

---

## 27. Team Members & Project Credits
This system was designed, developed, and verified as a University Engineering Major Capstone Project.
- **Contributor 1:** Machine Learning Pipeline & Text Preprocessing
- **Contributor 2:** FastAPI Backend & SQLite Architecture
- **Contributor 3:** React Frontend & Data Visualizations
