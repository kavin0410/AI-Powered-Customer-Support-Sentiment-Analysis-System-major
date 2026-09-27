"""
Evaluation and Metrics Reporting Module.

Computes comprehensive classification metrics:
- Accuracy, Precision (Macro & Weighted), Recall (Macro & Weighted)
- F1-Score (Macro & Weighted)
- Confusion Matrix & Classification Report
- High-resolution Confusion Matrix visualization saving to disk
"""

import os
from typing import Dict, List, Any
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)


def evaluate_classifier(
    model_name: str,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    labels: List[str]
) -> Dict[str, Any]:
    """
    Computes all standard evaluation metrics for multi-class classification.
    """
    acc = accuracy_score(y_true, y_pred)
    prec_macro = precision_score(y_true, y_pred, average="macro", zero_division=0)
    prec_weighted = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    rec_macro = recall_score(y_true, y_pred, average="macro", zero_division=0)
    rec_weighted = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1_macro = f1_score(y_true, y_pred, average="macro", zero_division=0)
    f1_weighted = f1_score(y_true, y_pred, average="weighted", zero_division=0)
    
    report_dict = classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0)
    report_str = classification_report(y_true, y_pred, labels=labels, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    return {
        "model_name": model_name,
        "accuracy": float(acc),
        "precision_macro": float(prec_macro),
        "precision_weighted": float(prec_weighted),
        "recall_macro": float(rec_macro),
        "recall_weighted": float(rec_weighted),
        "f1_macro": float(f1_macro),
        "f1_weighted": float(f1_weighted),
        "classification_report_str": report_str,
        "classification_report_dict": report_dict,
        "confusion_matrix": cm,
        "labels": labels
    }


def plot_confusion_matrix(
    cm: np.ndarray,
    labels: List[str],
    title: str,
    output_path: str
):
    """Saves a styled, annotated confusion matrix heatmap."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.figure(figsize=(8, 6.5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=labels,
        yticklabels=labels,
        cbar=True
    )
    plt.title(title, fontsize=13, weight="bold", pad=12)
    plt.xlabel("Predicted Label", fontsize=11)
    plt.ylabel("True Label", fontsize=11)
    plt.xticks(rotation=30, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Confusion matrix plot saved: {output_path}")


def create_comparison_table(results_list: List[Dict[str, Any]]) -> pd.DataFrame:
    """Creates a summary comparison DataFrame from multiple evaluation result dicts."""
    rows = []
    for res in results_list:
        rows.append({
            "Model": res["model_name"],
            "Accuracy": round(res["accuracy"], 4),
            "Macro Precision": round(res["precision_macro"], 4),
            "Weighted Precision": round(res["precision_weighted"], 4),
            "Macro Recall": round(res["recall_macro"], 4),
            "Weighted Recall": round(res["recall_weighted"], 4),
            "Macro F1": round(res["f1_macro"], 4),
            "Weighted F1": round(res["f1_weighted"], 4)
        })
    df = pd.DataFrame(rows)
    # Sort by Macro F1 descending
    df = df.sort_values(by="Macro F1", ascending=False).reset_index(drop=True)
    return df
