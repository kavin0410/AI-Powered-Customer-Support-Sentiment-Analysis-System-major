"""
Customer Issue Classification Modeling Pipeline.

Builds, trains, benchmarks, and serializes ML models for classifying customer issues:
1. Product Issue
2. Delivery Issue
3. Payment Issue
4. Technical Issue
5. Service Issue
6. General Feedback

Evaluates 4 architectures:
- Logistic Regression + TF-IDF
- Multinomial Naive Bayes + TF-IDF
- Linear SVM (Calibrated) + TF-IDF
- Random Forest + TF-IDF
"""

import os
import json
from typing import Dict, Any, Tuple
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier

from src.feature_engineering import build_text_pipeline
from src.evaluation import evaluate_classifier, plot_confusion_matrix, create_comparison_table
from src.preprocessing import VALID_CATEGORIES


ISSUE_CLASSES = sorted(list(VALID_CATEGORIES))


def get_candidate_models(random_state: int = 42) -> Dict[str, Any]:
    """Define candidate classification models for issue categorization."""
    return {
        "Logistic Regression": LogisticRegression(
            C=1.0,
            max_iter=1000,
            class_weight="balanced",
            random_state=random_state
        ),
        "Multinomial Naive Bayes": MultinomialNB(
            alpha=0.5
        ),
        "Linear SVM": CalibratedClassifierCV(
            estimator=LinearSVC(C=1.0, random_state=random_state, dual="auto", class_weight="balanced"),
            method="sigmoid",
            cv=3
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=150,
            max_depth=30,
            min_samples_split=4,
            random_state=random_state,
            class_weight="balanced",
            n_jobs=-1
        )
    }


def train_and_evaluate_issue_models(
    csv_path: str,
    output_dir: str,
    figures_dir: str,
    test_size: float = 0.20,
    random_state: int = 42
) -> Tuple[pd.DataFrame, str, Any]:
    """
    Executes end-to-end issue classification training and benchmarking.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    df = pd.read_csv(csv_path)
    X = df["feedback_text"].values
    y = df["issue_category"].values

    print(f"Loaded {len(df)} records for Issue Classification.")
    print("Class distribution:\n", df["issue_category"].value_counts())

    # Stratified train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state
    )

    print(f"Training split: {len(X_train)} samples | Testing split: {len(X_test)} samples")

    candidates = get_candidate_models(random_state=random_state)
    results = []
    trained_pipelines = {}

    for name, estimator in candidates.items():
        print(f"\n---> Training Issue Model: {name}...")
        pipeline = build_text_pipeline(estimator)
        pipeline.fit(X_train, y_train)
        
        y_pred = pipeline.predict(X_test)
        metrics = evaluate_classifier(name, y_test, y_pred, labels=ISSUE_CLASSES)
        results.append(metrics)
        trained_pipelines[name] = pipeline

        print(f"Results for {name}:")
        print(f"  Accuracy:         {metrics['accuracy']:.4f}")
        print(f"  Macro Precision:  {metrics['precision_macro']:.4f}")
        print(f"  Macro Recall:     {metrics['recall_macro']:.4f}")
        print(f"  Macro F1:         {metrics['f1_macro']:.4f}")
        print(f"  Weighted F1:      {metrics['f1_weighted']:.4f}")

        # Plot confusion matrix
        safe_name = name.lower().replace(" ", "_")
        cm_path = os.path.join(figures_dir, f"issue_cm_{safe_name}.png")
        plot_confusion_matrix(
            metrics["confusion_matrix"],
            labels=ISSUE_CLASSES,
            title=f"Issue Category Confusion Matrix: {name}",
            output_path=cm_path
        )

    comparison_df = create_comparison_table(results)
    comparison_csv_path = os.path.join(output_dir, "issue_model_comparison.csv")
    comparison_df.to_csv(comparison_csv_path, index=False)
    print("\n=== ISSUE MODEL BENCHMARK TABLE ===")
    print(comparison_df.to_string(index=False))

    # Selection criterion: Highest Macro F1
    best_model_name = comparison_df.iloc[0]["Model"]
    best_pipeline = trained_pipelines[best_model_name]
    best_metrics = next(r for r in results if r["model_name"] == best_model_name)

    print(f"\n[BEST MODEL SELECTED]: '{best_model_name}' (Macro F1 = {best_metrics['f1_macro']:.4f})")

    # Serialize best pipeline
    model_save_path = os.path.join(output_dir, "issue_pipeline.pkl")
    joblib.dump(best_pipeline, model_save_path)
    print(f"Saved best issue classification pipeline to: {model_save_path}")

    # Save detailed metadata
    metadata = {
        "task": "Issue Category Classification",
        "best_model": best_model_name,
        "classes": ISSUE_CLASSES,
        "metrics": {
            "accuracy": best_metrics["accuracy"],
            "precision_macro": best_metrics["precision_macro"],
            "recall_macro": best_metrics["recall_macro"],
            "f1_macro": best_metrics["f1_macro"],
            "f1_weighted": best_metrics["f1_weighted"],
        },
        "classification_report": best_metrics["classification_report_dict"]
    }
    with open(os.path.join(output_dir, "issue_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return comparison_df, best_model_name, best_pipeline


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_p = os.path.join(base_dir, "data", "processed", "cleaned_feedback.csv")
    models_p = os.path.join(base_dir, "models")
    fig_p = os.path.join(base_dir, "reports", "figures")
    train_and_evaluate_issue_models(data_p, models_p, fig_p)
