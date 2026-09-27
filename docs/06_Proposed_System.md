# 06. Proposed System Specification

The **AI-Powered Customer Support & Sentiment Analysis System** replaces manual and fragmented keyword workflows with a modern, high-throughput, full-stack intelligence architecture.

## Key Innovations of the Proposed System

### 1. Dual-Task Machine Learning Engine
Rather than treating sentiment and category as disconnected tasks, the platform runs unified inference across two specialized, calibrated pipelines:
- **Task A (Sentiment):** Evaluates overall emotional polarity (`Positive`, `Negative`, `Neutral`).
- **Task B (Issue Classification):** Classifies the grievance into one of 6 discrete operational domains (`Product Issue`, `Delivery Issue`, `Payment Issue`, `Technical Issue`, `Service Issue`, `General Feedback`).
- **Calibrated Posterior Distribution:** Yields genuine class probabilities enabling confidence-threshold routing.

### 2. Transparent Attention Level Triage
To assist customer support leaders, a deterministic rule-based business triage layer converts dual ML predictions into operational priorities:
- `Negative` with confidence $\ge 0.60 \implies$ **High Attention** (Immediate escalation)
- `Negative` with confidence $< 0.60 \implies$ **Medium Attention** (Priority queue review)
- `Neutral` $\implies$ **Medium Attention** (Standard informational queue)
- `Positive` $\implies$ **Low Attention** (Appreciation logs / automated response)

### 3. Asynchronous REST API Architecture (FastAPI)
The backend provides low-latency endpoint serving, strict Pydantic v2 data validation, CORS protection, and built-in interactive OpenAPI documentation (`/docs`, `/redoc`).

### 4. Normalized SQLite Repository with Dynamic Seeding
The backend integrates a SQLite relational database auto-seeded with 3,078 verified records, indexing frequently queried fields (`sentiment`, `issue_category`, `feedback_date`) to guarantee sub-millisecond query performance for complex dashboard filters.

### 5. Interactive SaaS Analytics Dashboard (React 18 + Vite + Tailwind CSS)
A single-page application (SPA) featuring:
- Executive KPI ribbon
- Recharts visualizations (Donut, Categorical Bar, Area Volume, Multi-Line Trends, Stacked Bars)
- Live interactive text prediction sandbox with preset scenarios
- Server-side paginated repository with live text search and multi-parameter filtering
- Single-record detail inspection modal
- Automated business insights distinguishing factual observations from strategic actions
- Persistent dark/light theme switching
