# 12. Issue Category Classification

## Problem Definition
Customer inquiries rarely stop at polarity; support operations require accurate categorization into operational departments to avoid misrouting and delayed escalations. The system categorizes each ticket into one of six operational classes:

1. **Product Issue:** Physical defects, broken items, missing accessories, incorrect sizing, or material quality discrepancies.
2. **Delivery Issue:** Late shipments, lost parcels, courier tracking inaccuracies, damaged packages, or misdelivery.
3. **Payment Issue:** Billing errors, failed checkout transactions, double charges, unauthorized debits, or refund processing inquiries.
4. **Technical Issue:** Mobile app crashes, website 500 error codes, server timeouts, authentication/login failures, or API glitches.
5. **Service Issue:** Unhelpful agent interactions, excessive hold times, impolite representatives, or unresolved escalations.
6. **General Feedback:** Website UX suggestions, catalog feature requests, general appreciation, or neutral corporate feedback.

## Evaluated Classifiers (Test Set, N=616)
Benchmarked under identical 80/20 stratified conditions with sublinear TF-IDF unigram and bigram feature representations:

| Model Architecture | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Selected |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression + TF-IDF** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **Selected (Best)** |
| Multinomial Naive Bayes + TF-IDF | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | - |
| Linear SVC (Calibrated) + TF-IDF | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | - |
| Random Forest + TF-IDF | 0.9903 | 0.9935 | 0.9891 | 0.9910 | 0.9902 | - |

## Classification Report (Best Model: Logistic Regression)
```
                  precision    recall  f1-score   support

  Delivery Issue       1.00      1.00      1.00       123
General Feedback       1.00      1.00      1.00        64
   Payment Issue       1.00      1.00      1.00        97
   Product Issue       1.00      1.00      1.00       147
   Service Issue       1.00      1.00      1.00        93
 Technical Issue       1.00      1.00      1.00        92

        accuracy                           1.00       616
       macro avg       1.00      1.00      1.00       616
    weighted avg       1.00      1.00      1.00       616
```
The serialized pipeline is stored in `models/issue_pipeline.pkl`.
