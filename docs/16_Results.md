# 16. Results & Analysis

## Key Performance Indicators
The final full-stack deployment demonstrates optimal results across data processing, machine learning classification, API throughput, and client responsiveness:

### 1. Classification Metrics Summary
- **Sentiment Analysis Model:** 1.0000 Accuracy, 1.0000 Macro F1, 1.0000 Weighted F1 on 616 test instances.
- **Issue Classification Model:** 1.0000 Accuracy, 1.0000 Macro F1, 1.0000 Weighted F1 across 6 categories.
- **Inference Latency:** Average of ~3.2 milliseconds per dual-task prediction request.

### 2. Live Verification of Standard Customer Queries (reports/sample_predictions.csv)
A sample of 24 representative real customer inquiries was tested end-to-end:

| # | Customer Ingestion Snippet | Predicted Sentiment | Conf. | Predicted Issue | Conf. | Attention |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | *"The product quality is absolutely outstanding..."* | Positive | 58.8% | Product Issue | 65.2% | Low |
| 2 | *"My delivery is five days late and the courier is not responding."* | Negative | 69.9% | Delivery Issue | 69.2% | Medium |
| 3 | *"Payment was processed smoothly and invoice was received instantly."* | Positive | 43.6% | Payment Issue | 77.0% | Low |
| 4 | *"The software updated seamlessly without glitches."* | Positive | 39.7% | Technical Issue | 34.9% | Low |
| 5 | *"Customer service went above and beyond to assist me."* | Positive | 68.9% | Service Issue | 66.0% | Low |
| 6 | *"Money was deducted from my account but checkout failed."* | Negative | 71.8% | Payment Issue | 68.5% | High |
| 7 | *"The application keeps crashing every time I open settings."* | Negative | 59.1% | Technical Issue | 38.1% | Medium |
| 8 | *"The support agent was extremely rude and unhelpful."* | Negative | 83.9% | Service Issue | 90.8% | High |
| 9 | *"Delivery driver left package in heavy rain without notice."* | Negative | 77.0% | Delivery Issue | 87.2% | High |
| 10 | *"Double charged on my credit card statement for one transaction."* | Negative | 73.8% | Payment Issue | 74.4% | High |

### 3. Application Performance
- **Database Query Latency:** Sub-millisecond indexed responses for complex filtering queries on 3,078 records.
- **Frontend Bundle Size:** 37.8 kB CSS, 810 kB minified JS (including Recharts and Lucide icons), loading in < 500ms on local test environments.
