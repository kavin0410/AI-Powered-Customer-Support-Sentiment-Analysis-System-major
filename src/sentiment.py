"""
Sentiment Analysis Modeling Pipeline.

Builds, trains, evaluates, and compares 4 ML architectures:
1. Logistic Regression + TF-IDF
2. Multinomial Naive Bayes + TF-IDF
3. Linear SVM (Calibrated) + TF-IDF
4. Random Forest + TF-IDF

Selects and serializes the optimal model pipeline based on balanced Macro/Weighted F1.
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
from src.preprocessing import VALID_SENTIMENTS


SENTIMENT_CLASSES = sorted(list(VALID_SENTIMENTS))  # ['Negative', 'Neutral', 'Positive']


def get_candidate_models(random_state: int = 42) -> Dict[str, Any]:
    """Define candidate classification models."""
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


def train_and_evaluate_sentiment_models(
    csv_path: str,
    output_dir: str,
    figures_dir: str,
    test_size: float = 0.20,
    random_state: int = 42
) -> Tuple[pd.DataFrame, str, Any]:
    """
    Executes end-to-end sentiment model training and benchmarking.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    df = pd.read_csv(csv_path)
    X = df["feedback_text"].values
    y = df["sentiment"].values

    print(f"Loaded {len(df)} records for Sentiment Training.")
    print("Class distribution:\n", df["sentiment"].value_counts())

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
        print(f"\n---> Training Sentiment Model: {name}...")
        pipeline = build_text_pipeline(estimator)
        pipeline.fit(X_train, y_train)
        
        y_pred = pipeline.predict(X_test)
        metrics = evaluate_classifier(name, y_test, y_pred, labels=SENTIMENT_CLASSES)
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
        cm_path = os.path.join(figures_dir, f"sentiment_cm_{safe_name}.png")
        plot_confusion_matrix(
            metrics["confusion_matrix"],
            labels=SENTIMENT_CLASSES,
            title=f"Sentiment Confusion Matrix: {name}",
            output_path=cm_path
        )

    comparison_df = create_comparison_table(results)
    comparison_csv_path = os.path.join(output_dir, "sentiment_model_comparison.csv")
    comparison_df.to_csv(comparison_csv_path, index=False)
    print("\n=== SENTIMENT MODEL BENCHMARK TABLE ===")
    print(comparison_df.to_string(index=False))

    # Selection criterion: Highest Macro F1 (balances all classes without majority bias)
    best_model_name = comparison_df.iloc[0]["Model"]
    best_pipeline = trained_pipelines[best_model_name]
    best_metrics = next(r for r in results if r["model_name"] == best_model_name)

    print(f"\n[BEST MODEL SELECTED]: '{best_model_name}' (Macro F1 = {best_metrics['f1_macro']:.4f})")

    # Serialize best pipeline
    model_save_path = os.path.join(output_dir, "sentiment_pipeline.pkl")
    joblib.dump(best_pipeline, model_save_path)
    print(f"Saved best sentiment pipeline to: {model_save_path}")

    # Save detailed classification report and metrics metadata
    metadata = {
        "task": "Sentiment Analysis",
        "best_model": best_model_name,
        "classes": SENTIMENT_CLASSES,
        "metrics": {
            "accuracy": best_metrics["accuracy"],
            "precision_macro": best_metrics["precision_macro"],
            "recall_macro": best_metrics["recall_macro"],
            "f1_macro": best_metrics["f1_macro"],
            "f1_weighted": best_metrics["f1_weighted"],
        },
        "classification_report": best_metrics["classification_report_dict"]
    }
    with open(os.path.join(output_dir, "sentiment_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return comparison_df, best_model_name, best_pipeline


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_p = os.path.join(base_dir, "data", "processed", "cleaned_feedback.csv")
    models_p = os.path.join(base_dir, "models")
    fig_p = os.path.join(base_dir, "reports", "figures")
    train_and_evaluate_sentiment_models(data_p, models_p, fig_p)
