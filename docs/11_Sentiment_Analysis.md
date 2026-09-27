# 11. Sentiment Analysis Model

## Problem Definition
Sentiment analysis classifies incoming customer expressions into three mutually exclusive emotional states:
- **Positive:** Customer expresses satisfaction, gratitude, praise, or delight.
- **Negative:** Customer communicates frustration, dissatisfaction, grievance, bug reports, or service failure.
- **Neutral:** Customer requests product specifications, inquires about policies, or leaves objective statements without emotional polarity.

## Feature Extraction: TF-IDF Vectorization
The preprocessed text is transformed into numerical vectors using Scikit-Learn's `TfidfVectorizer`:
- **N-gram Range:** `(1, 2)` (capturing both individual words and two-word collocations such as `"very good"`, `"terrible service"`).
- **Sublinear Term Frequency:** Applied (`sublinear_tf=True`) to logarithmically scale term frequency counts, preventing high-frequency terms from skewing vector magnitudes.
- **Max Features:** Tuned to the most informative 5,000 vocabulary tokens.

## Evaluated Classifiers
Four distinct machine learning architectures were trained and benchmarked using an 80/20 stratified split (2,462 training instances, 616 test instances):

1. **Multinomial Naive Bayes (MNB):** Classic probabilistic baseline based on Bayes' theorem with laplace smoothing.
2. **Logistic Regression (L2 Regularized):** Maximum-entropy linear classifier optimizing log-loss with Platt-scaled probability estimation.
3. **Linear Support Vector Classifier (LinearSVC):** Maximum-margin hyper-plane classifier calibrated using `CalibratedClassifierCV` to provide well-behaved probability confidences.
4. **Random Forest Classifier:** Non-linear ensemble model with 100 decision tree estimators.

## Benchmark Results (Test Set, N=616)
| Model Architecture | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Selected |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression + TF-IDF** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **Selected (Best)** |
| Multinomial Naive Bayes + TF-IDF | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | - |
| Linear SVC (Calibrated) + TF-IDF | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | - |
| Random Forest + TF-IDF | 0.9399 | 0.9570 | 0.9332 | 0.9422 | 0.9397 | - |

Logistic Regression was chosen for production deployment due to its high generalization, minimal inference latency (< 5ms), and calibrated probabilistic confidence distribution.
