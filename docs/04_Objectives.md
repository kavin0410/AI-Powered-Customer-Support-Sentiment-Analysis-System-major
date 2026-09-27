# 04. Objectives

The primary objectives of this engineering major project are structured as follows:

### 1. Data Engineering Objectives
- Curate and validate a comprehensive, realistic customer feedback dataset comprising diverse sentiments and operational categories.
- Develop an NLP preprocessing pipeline that preserves semantic sentiment markers, handles informal contractions, cleans noise (URLs, emails, special punctuation), and standardizes word stems via WordNet lemmatization.
- Guarantee strict data leakage prevention by separating train/test partitions before vectorizer fitting.

### 2. Machine Learning Objectives
- Train and benchmark multiple supervised classifiers (Logistic Regression, Multinomial Naive Bayes, Linear Support Vector Classifier, Random Forest) on TF-IDF unigram and bigram representations.
- Select optimal architectures based on accuracy, Macro F1, and calibrated probability outputs.
- Serialize trained end-to-end pipelines into production joblib artifacts for rapid zero-retraining inference.

### 3. Backend & API Objectives
- Construct an asynchronous REST API utilizing FastAPI and Python 3.11+.
- Implement strict Pydantic v2 schemas for all requests and responses.
- Implement transparent, deterministic business triage logic for Attention Level ranking (`High`, `Medium`, `Low`).
- Provide automated OpenAPI interactive documentation (`/docs` and `/redoc`).
- Maintain normalized SQLite storage with automatic migration, auto-seeding, and query optimization indexes.

### 4. Frontend & User Experience Objectives
- Build a responsive SaaS dashboard using React 18, Vite, and Tailwind CSS.
- Eliminate all hardcoded data: ensure every chart, metric card, and table is powered dynamically by backend API responses.
- Implement server-side paginated customer feedback exploration with multi-criteria filtering and text search.
- Integrate interactive Recharts components for real-time visualization of sentiment and issue distributions.
- Implement dark and light mode styling with `localStorage` persistence.

### 5. Quality & Production Hardening Objectives
- Achieve high test coverage with automated pytest suites covering backend APIs, ML inference, and preprocessing.
- Provide containerized deployment scripts via Docker and Docker Compose.
- Author exhaustive technical and architectural documentation.
