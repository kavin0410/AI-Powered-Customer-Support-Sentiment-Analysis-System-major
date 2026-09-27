# 07. Methodology

The development methodology follows an iterative, phased engineering framework:

```
[Phase 1: ML Foundation] ───► [Phase 2: Full-Stack Integration] ───► [Phase 3: Production Hardening]
```

## Phase 1: Machine Learning Foundation
1. **Data Generation & Collection:** Synthesizing realistic customer feedback scenarios with balanced distributions across 3 sentiments and 6 operational categories.
2. **Text Normalization:** Implementing custom tokenization, lowercasing, contraction expansion, noise stripping (URLs, emails, punctuation), negation-preserving stopword filtering, and WordNet lemmatization.
3. **Feature Engineering:** Applying sublinear TF-IDF vectorization with unigram and bigram representation (`ngram_range=(1, 2)`).
4. **Model Training & Benchmarking:** Comparing Logistic Regression, Multinomial Naive Bayes, Linear Support Vector Classifier (calibrated via Platt scaling), and Random Forest.
5. **Model Evaluation & Serialization:** Generating classification reports, confusion matrices, and serializing the best performing pipelines with joblib.

## Phase 2: Full-Stack Application Integration
1. **API Development:** Building a FastAPI REST backend structured into routers, services, schemas, and utils.
2. **Database Modeling:** Creating a SQLite schema with indices on `sentiment`, `issue_category`, and `feedback_date`, with an auto-seeding engine loading 3,078 records from `cleaned_feedback.csv`.
3. **Frontend Development:** Building a React 18 single-page application with Vite, Tailwind CSS, React Router v7, Recharts, and Axios.
4. **Dynamic Data Flow:** Connecting all dashboard charts and metric cards directly to backend endpoints, eliminating all mock or hardcoded statistics.

## Phase 3: Production Hardening & Validation
1. **Centralized Error Handling & Logging:** Implementing custom exception handlers to prevent internal traceback and file path leakage, and setting up structured application logging.
2. **Comprehensive Automated Testing:** Writing 38 pytest test cases across `tests/backend/` and `tests/ml/`.
3. **Containerization:** Authoring production Dockerfiles for frontend and backend with NGINX SPA routing and healthcheck probes in `docker-compose.yml`.
4. **Documentation & Reporting:** Creating complete architectural documentation in `docs/` and generating `reports/sample_predictions.csv` for verified live inquiries.
