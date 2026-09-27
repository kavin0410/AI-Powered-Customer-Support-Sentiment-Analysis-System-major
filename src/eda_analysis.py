"""
EDA and Visualization Pipeline for Customer Support Feedback.

Analyzes dataset shapes, distributions, text lengths, temporal trends,
and vocabulary frequency, generating high-resolution figures in reports/figures/.
"""

import os
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def run_eda(csv_path: str, figures_dir: str):
    """Generate comprehensive EDA charts and reports."""
    os.makedirs(figures_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    print("=== DATASET SHAPE & INFO ===")
    print(f"Total Rows: {df.shape[0]}")
    print(f"Total Columns: {df.shape[1]}")
    print(f"Columns: {list(df.columns)}")
    print("\nMissing values:")
    print(df.isnull().sum())

    # Set aesthetic theme
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    plt.rcParams["figure.dpi"] = 300

    # 1. Sentiment Distribution
    plt.figure(figsize=(8, 5))
    order_sent = ["Negative", "Positive", "Neutral"]
    palette_sent = {"Negative": "#e74c3c", "Positive": "#2ecc71", "Neutral": "#3498db"}
    ax = sns.countplot(data=df, x="sentiment", order=order_sent, palette=palette_sent)
    plt.title("Distribution of Customer Feedback Sentiment", fontsize=14, weight="bold", pad=12)
    plt.xlabel("Sentiment Class", fontsize=11)
    plt.ylabel("Number of Feedback Records", fontsize=11)
    for p in ax.patches:
        height = int(p.get_height())
        ax.annotate(f"{height} ({height/len(df):.1%})",
                    (p.get_x() + p.get_width() / 2., height),
                    ha="center", va="bottom", fontsize=10, xytext=(0, 4),
                    textcoords="offset points")
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "sentiment_distribution.png"))
    plt.close()
    print("Generated: sentiment_distribution.png")

    # 2. Issue Category Distribution
    plt.figure(figsize=(10, 5.5))
    cat_counts = df["issue_category"].value_counts()
    ax = sns.barplot(x=cat_counts.values, y=cat_counts.index, palette="viridis")
    plt.title("Distribution of Customer Issue Categories", fontsize=14, weight="bold", pad=12)
    plt.xlabel("Number of Feedback Records", fontsize=11)
    plt.ylabel("Issue Category", fontsize=11)
    for p in ax.patches:
        width = int(p.get_width())
        ax.annotate(f"{width} ({width/len(df):.1%})",
                    (width, p.get_y() + p.get_height() / 2.),
                    ha="left", va="center", fontsize=9.5, xytext=(5, 0),
                    textcoords="offset points")
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "issue_category_distribution.png"))
    plt.close()
    print("Generated: issue_category_distribution.png")

    # 3. Feedback Length Distribution (Word Count & Character Count)
    df["word_count"] = df["feedback_text"].apply(lambda t: len(str(t).split()))
    df["char_count"] = df["feedback_text"].apply(lambda t: len(str(t)))
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(df["word_count"], bins=30, kde=True, ax=axes[0], color="#2980b9")
    axes[0].set_title("Feedback Word Count Distribution", fontsize=13, weight="bold")
    axes[0].set_xlabel("Word Count per Feedback")
    axes[0].set_ylabel("Frequency")
    axes[0].axvline(df["word_count"].mean(), color="red", linestyle="--", label=f"Mean: {df['word_count'].mean():.1f}")
    axes[0].axvline(df["word_count"].median(), color="orange", linestyle=":", label=f"Median: {df['word_count'].median():.1f}")
    axes[0].legend()

    sns.boxplot(data=df, x="sentiment", y="word_count", ax=axes[1], palette=palette_sent, order=order_sent)
    axes[1].set_title("Word Count by Sentiment Class", fontsize=13, weight="bold")
    axes[1].set_xlabel("Sentiment Class")
    axes[1].set_ylabel("Word Count")
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "feedback_length_distribution.png"))
    plt.close()
    print("Generated: feedback_length_distribution.png")

    # 4. Monthly Feedback Volume
    df["date"] = pd.to_datetime(df["date"])
    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    monthly_vol = df.groupby(["year_month", "sentiment"]).size().unstack(fill_value=0)

    plt.figure(figsize=(12, 6))
    monthly_vol.plot(kind="bar", stacked=True, color=[palette_sent.get(c, "#95a5a6") for c in monthly_vol.columns], figsize=(12, 6))
    plt.title("Monthly Customer Feedback Volume by Sentiment", fontsize=14, weight="bold", pad=12)
    plt.xlabel("Month", fontsize=11)
    plt.ylabel("Feedback Count", fontsize=11)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Sentiment", loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "monthly_feedback_volume.png"))
    plt.close()
    print("Generated: monthly_feedback_volume.png")

    # 5. Sentiment by Issue Category Heatmap & Stacked Bar
    plt.figure(figsize=(10, 6))
    cross_tab = pd.crosstab(df["issue_category"], df["sentiment"], normalize="index") * 100
    cross_tab = cross_tab[["Negative", "Neutral", "Positive"]]
    sns.heatmap(cross_tab, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Percentage (%)'})
    plt.title("Sentiment Percentage within Each Issue Category (%)", fontsize=14, weight="bold", pad=12)
    plt.xlabel("Sentiment", fontsize=11)
    plt.ylabel("Issue Category", fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "sentiment_by_issue_category.png"))
    plt.close()
    print("Generated: sentiment_by_issue_category.png")

    # 6. Top Frequent Words Overall
    all_tokens = " ".join(df["cleaned_text"].astype(str)).split()
    word_freq = Counter(all_tokens).most_common(25)
    wf_df = pd.DataFrame(word_freq, columns=["word", "count"])

    plt.figure(figsize=(10, 6.5))
    sns.barplot(data=wf_df, x="count", y="word", palette="mako")
    plt.title("Top 25 Most Frequent Words Across All Feedback (Cleaned)", fontsize=14, weight="bold", pad=12)
    plt.xlabel("Token Frequency", fontsize=11)
    plt.ylabel("Term", fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "top_frequent_words.png"))
    plt.close()
    print("Generated: top_frequent_words.png")

    # 7. Top Words by Sentiment
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
    for i, sent in enumerate(order_sent):
        sent_tokens = " ".join(df[df["sentiment"] == sent]["cleaned_text"].astype(str)).split()
        top_sent_words = Counter(sent_tokens).most_common(15)
        top_df = pd.DataFrame(top_sent_words, columns=["word", "count"])
        sns.barplot(data=top_df, x="count", y="word", ax=axes[i], color=palette_sent[sent])
        axes[i].set_title(f"Top 15 Words: {sent} Sentiment", fontsize=13, weight="bold")
        axes[i].set_xlabel("Count")
        axes[i].set_ylabel("Term")
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "top_words_by_sentiment.png"))
    plt.close()
    print("Generated: top_words_by_sentiment.png")

    print("\nEDA completed. All figures saved to reports/figures/.")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "processed", "cleaned_feedback.csv")
    fig_dir = os.path.join(base_dir, "reports", "figures")
    run_eda(data_path, fig_dir)
