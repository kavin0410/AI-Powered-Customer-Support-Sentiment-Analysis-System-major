# 14. Application Modules & User Interface

The React frontend single-page application is partitioned into 7 specialized functional views:

## 1. Executive Dashboard (`/dashboard`)
- **Primary Metric Ribbon:** Displays total volume (3,078), positive, negative, and neutral counts, plus the most frequent issue category.
- **Visualizations (Recharts):**
  1. *Sentiment Distribution:* Donut chart depicting overall customer polarity.
  2. *Issue Category Breakdown:* Horizontal bar chart comparing category frequencies.
  3. *Monthly Ingestion Volume:* Smooth area chart tracking feedback trends across 2025.
  4. *Sentiment Trajectory:* Multi-line chart monitoring sentiment evolution over time.
  5. *Category Composition:* Cross-tabulated stacked bar chart showing sentiment share within each department.

## 2. Real-Time Prediction Sandbox (`/prediction`)
- Interactive text input area with character count limit and clear triggers.
- Four quick-load scenario presets (Praise, Delivery Delay, Billing Failure, Technical Crash).
- Unified dual-task inference display showing:
  - Sentiment classification badge with percentage confidence.
  - Issue category badge with percentage confidence.
  - Operational Attention Level badge (`High Attention`, `Medium Attention`, `Low Attention`).
  - Dynamic classification explanation and triage action plan.
  - Interactive Recharts horizontal probability bars illustrating posterior class distributions.

## 3. Customer Feedback Explorer (`/feedback`)
- Dynamic server-side paginated table with selectable page sizes (10, 20, 50).
- Live search query input with debounce.
- Multi-criteria filter dropdowns for Sentiment and Issue Category.
- Single-record inspection modal showing full customer feedback, identifiers, and timestamps.
- Client-side CSV export trigger.

## 4. Sentiment Analytics Deep-Dive (`/sentiment`)
- Executive polarity breakdown cards.
- Automated identification of category sentiment extrema (e.g. highest positive and highest negative department).
- Temporal sentiment volume charts.

## 5. Issue Category Analytics (`/issues`)
- Proportional volume analysis across all six required domains.
- Category statistics table indicating total complaints, negative grievance rate, and relative share.

## 6. Dynamic Business Insights (`/insights`)
- Automated executive intelligence cards generated dynamically from database statistics.
- Strict structural separation between **Factual Data Observation** and **Recommended Strategic Action**.

## 7. System Architecture & About (`/about`)
- Academic capstone documentation detailing problem statement, objectives, and tech stack.
- Interactive system architecture workflow diagram.
- Machine learning specifications and project team placeholder.
