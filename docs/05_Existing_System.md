# 05. Existing System Analysis

## Overview of Existing Approaches
In many commercial and legacy enterprise environments, customer support ticket management and sentiment monitoring rely on three primary paradigms:

### 1. Manual Human Triage
- **Workflow:** Incoming tickets enter a general inbox. Tier-1 support staff manually read each text snippet, assess urgency, select a category dropdown, and route the ticket to the appropriate department.
- **Shortcomings:** Highly labor-intensive, slow (often taking hours or days during traffic surges), subject to cognitive variance across human agents, and costly to scale.

### 2. Regex and Keyword Matching
- **Workflow:** Rule engines check for predefined substrings (e.g., "refund", "crash", "late", "broke") to flag tickets.
- **Shortcomings:** Incapable of understanding context, sarcasm, or linguistic nuances. Fails completely on negations (e.g., treating "I am not happy with the delivery" as positive if "happy" is matched, or misrouting "I didn't receive a broken product" as a broken product report).

### 3. Monolithic Standalone Scripts & Black-Box APIs
- **Workflow:** Basic Python or R scripts that perform batch offline sentiment scoring, or third-party proprietary APIs (e.g., cloud sentiment APIs).
- **Shortcomings:** High recurring API costs, vendor lock-in, latency bottlenecks, and a lack of integrated domain-specific issue taxonomy. Furthermore, these tools typically lack interactive full-stack management dashboards and persistent databases for historical analytics.

| Feature / Metric | Manual Triage | Keyword Rule Engines | Proposed Full-Stack AI System |
| :--- | :--- | :--- | :--- |
| **Response Latency** | Minutes to Hours | Milliseconds | < 50 Milliseconds |
| **Negation Handling** | High (Human) | Poor / Zero | High (Preserved Tokens) |
| **Issue Categorization** | Inconsistent | Rigid / Fragile | Supervised ML (Calibrated) |
| **Confidence Scoring** | Subjective | None | True Posterior Probability |
| **Operating Cost** | Linear with Volume | Low | Minimal (Self-Hosted) |
| **Analytics Dashboard** | Disconnected | Fragmented | Live Integrated React SPA |
