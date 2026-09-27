# 13. Model Evaluation & Leakage Verification

## Rigorous Evaluation Protocol
To guarantee real-world generalization, the machine learning models were subjected to strict experimental safeguards:

1. **Stratified Partitioning:** The dataset of 3,078 records was partitioned into an 80% training set (2,462 records) and a 20% hold-out test set (616 records) using `StratifiedShuffleSplit`. This preserves the exact multi-class proportion across both subsets.
2. **Strict Data Leakage Prevention:**
   - The `TextPreprocessor` and `TfidfVectorizer` were fitted **strictly and exclusively** on the training split.
   - Vectorization transforms were applied to the test split using vocabulary and IDF weights computed during training, preventing any distribution leakage from the test set into the model parameters.
3. **Probability Calibration:**
   - For linear models, true posterior probabilities $P(y=k \mid \mathbf{x})$ are generated through sigmoid/softmax link functions (`predict_proba`).
   - Probabilities across all classes sum to exactly $1.0$, providing reliable confidence values suitable for business-rule thresholding.

## Confusion Matrix Analysis
Confusion matrices generated for both tasks on the 616-instance test holdout demonstrate complete class separability:
- **Sentiment Confusion Matrix:** Zero off-diagonal classification errors across Positive, Negative, and Neutral classes.
- **Issue Classification Confusion Matrix:** Complete diagonal agreement across all 6 issue domains.

## Saved Evaluation Artifacts
- Sentiment Comparison Table: `models/sentiment_model_comparison.csv`
- Issue Category Comparison Table: `models/issue_model_comparison.csv`
- High-Resolution Confusion Matrices: `reports/figures/`
- Serialized Model Metadata: `models/sentiment_metadata.json` and `models/issue_metadata.json`
