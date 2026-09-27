# 08. System Architecture

The overall system architecture follows a decoupled, three-tier micro-service pattern consisting of the Client Layer (React SPA), Application Gateway Layer (FastAPI), and Data/Inference Layer (SQLite & Serialized ML Pipelines).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             PRESENTATION TIER                               │
│                   React 18 Single-Page Application (Vite)                   │
│                                                                             │
│   ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐   │
│   │   Dashboard   │ │  Predictor    │ │  Feedback     │ │  Sentiment /  │   │
│   │   KPIs & 5    │ │  Dual-Task    │ │  Server-Side  │ │  Issue Deep   │   │
│   │   Recharts    │ │  Inference UI │ │  Paginated    │ │  Analytics    │   │
│   └───────┬───────┘ └───────┬───────┘ └───────┬───────┘ └───────┬───────┘   │
│           │                 │                 │                 │           │
│           └─────────────────┼─────────────────┼─────────────────┘           │
│                             ▼                                               │
│                 Central Axios HTTP Client (services/api.js)                 │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │ JSON over HTTP REST
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            APPLICATION GATEWAY TIER                         │
│                         FastAPI REST API (Uvicorn ASGI)                     │
│                                                                             │
│   ├── Middleware: CORS (http://localhost:5173), Exception Handlers, Logger  │
│   ├── Schema Validation: Pydantic v2 (min/max length, whitespace trimming)  │
│   │                                                                         │
│   ├── REST Routers:                                                         │
│   │   ├── GET  /api/health                                                  │
│   │   ├── POST /api/predict                                                 │
│   │   ├── GET  /api/dashboard                                               │
│   │   ├── GET  /api/feedback & /api/feedback/{id}                           │
│   │   ├── GET  /api/analytics/{sentiment,issues}                            │
│   │   └── GET  /api/insights                                                │
│   │                                                                         │
│   └── Business Services:                                                    │
│       ├── PredictionService   ◄──► Validation & Attention Triage Engine     │
│       ├── FeedbackService     ◄──► Parameterized SQL Queries                │
│       ├── AnalyticsService    ◄──► Dynamic Aggregation Aggregators          │
│       └── InsightService      ◄──► Dynamic Observation & Action Synthesizer │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │ Internal Function Calls & SQL
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PERSISTENCE & MODEL TIER                          │
│                                                                             │
│   ┌───────────────────────────────────┐ ┌───────────────────────────────┐   │
│   │         SQLite Database           │ │      Serialized ML Models     │   │
│   │   - Table: feedback (3,078 recs)  │ │   - models/sentiment_*.pkl    │   │
│   │   - Indexes: sentiment, category, │ │   - models/issue_*.pkl        │   │
│   │     feedback_date                 │ │   - Calibrated Platt Scaling  │   │
│   │   - File: customer_support.db     │ │   - Zero-Retraining Singleton │   │
│   └───────────────────────────────────┘ └───────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Architectural Highlights
1. **Stateless Backend:** FastAPI routes do not store conversational state in server memory, facilitating seamless horizontal container scaling.
2. **Singleton Model Caching:** Serialized ML pipelines load once upon application startup via the FastAPI lifespan context manager and remain cached in memory for sub-millisecond inference.
3. **Optimized SQLite Persistence:** Indexed lookups on frequently filtered fields prevent full table scans when aggregating dashboard charts.
4. **Environment Isolation:** Configuration parameters (`PORT`, `HOST`, `ALLOWED_ORIGINS`, `VITE_API_BASE_URL`) are externalized via environment variables.
