# 15. Testing & Verification

## Automated Testing Strategy
Testing spans unit, integration, schema validation, and end-to-end verification. A total of **38 automated pytest test cases** are maintained in `tests/backend/` and `tests/ml/`:

### 1. Backend API Test Suite (`tests/backend/`)
- `test_health.py` (2 tests): Verifies `/api/health` status, database connection, and model loading flags.
- `test_prediction.py` (3 tests): Tests dual-task prediction outputs, calibrated probabilities, empty/whitespace validation (400/422), and maximum character overflow limits.
- `test_feedback.py` (4 tests): Tests server-side pagination, sentiment filtering, category filtering, keyword search, and 404 handling on missing IDs.
- `test_dashboard.py` (1 test): Validates that dashboard KPI counts match totals and distributions sum accurately.
- `test_analytics.py` (3 tests): Validates `/api/analytics/sentiment`, `/api/analytics/issues`, and `/api/insights` response structures.

### 2. Machine Learning Test Suite (`tests/ml/`)
- `test_preprocessing.py` (8 tests): Tests lowercase conversion, URL/email removal, punctuation handling, negation token preservation (`"not"`, `"never"`), and contraction expansion.
- `test_models.py` (5 tests): Tests pipeline file existence, Scikit-learn Pipeline typing, class labels alignment, and `predict_proba` matrix shapes.
- `test_predictor.py` (12 tests): Tests empty/null/non-string input error handling, output schema integrity, and parametric tests across standard realistic customer statements.

## Test Execution Summary
```
tests/backend/test_analytics.py::test_get_sentiment_analytics PASSED
tests/backend/test_analytics.py::test_get_issue_analytics PASSED
tests/backend/test_analytics.py::test_get_business_insights PASSED
tests/backend/test_dashboard.py::test_get_dashboard_metrics PASSED
tests/backend/test_feedback.py::test_get_feedback_paginated PASSED
tests/backend/test_feedback.py::test_get_feedback_filtering PASSED
tests/backend/test_feedback.py::test_get_feedback_search PASSED
tests/backend/test_feedback.py::test_get_feedback_by_id_success_and_404 PASSED
tests/backend/test_health.py::test_health_check_status PASSED
tests/backend/test_health.py::test_root_endpoint PASSED
tests/backend/test_prediction.py::test_predict_feedback_valid PASSED
tests/backend/test_prediction.py::test_predict_feedback_empty_validation PASSED
tests/backend/test_prediction.py::test_predict_feedback_excessive_length PASSED
tests/ml/test_models.py (5 tests) PASSED
tests/ml/test_predictor.py (12 tests) PASSED
tests/ml/test_preprocessing.py (8 tests) PASSED

======================= 38 passed in 8.18s =======================
```
All 38 tests execute cleanly with a 100% pass rate.
