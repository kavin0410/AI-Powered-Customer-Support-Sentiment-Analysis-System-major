"""
Script to create clean, well-documented Jupyter Notebooks for Phase 1 tasks:
1. 01_data_collection.ipynb
2. 02_data_preprocessing.ipynb
3. 03_sentiment_analysis.ipynb
4. 04_issue_classification.ipynb
5. 05_model_comparison.ipynb
"""

import json
import os


def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }


def md_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }


def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split("\n")]
    }


def generate_all_notebooks(notebooks_dir: str):
    os.makedirs(notebooks_dir, exist_ok=True)

    # 1. 01_data_collection.ipynb
    nb1_cells = [
        md_cell(
            "# 01. Data Collection & Raw Dataset Inspection\n"
            "**Project**: AI-Powered Customer Support & Sentiment Analysis System\n\n"
            "This notebook covers:\n"
            "- Overview of data schema and target classes\n"
            "- Reproducible dataset generation pipeline for customer support feedback\n"
            "- Injection of realistic data anomalies (duplicates, missing text, irregular casing)\n"
            "- Raw dataset validation and initial inspection"
        ),
        code_cell(
            "import os\n"
            "import sys\n"
            "sys.path.insert(0, '..')\n\n"
            "import pandas as pd\n"
            "from src.data_generator import generate_raw_dataset, CATEGORIES, SENTIMENTS\n\n"
            "print('Categories:', CATEGORIES)\n"
            "print('Sentiments:', SENTIMENTS)"
        ),
        md_cell("### 1. Generate or Load Raw Feedback Dataset"),
        code_cell(
            "raw_csv_path = '../data/raw/raw_feedback.csv'\n"
            "if not os.path.exists(raw_csv_path):\n"
            "    df_raw = generate_raw_dataset(n_samples=3200, random_seed=42)\n"
            "    os.makedirs('../data/raw', exist_ok=True)\n"
            "    df_raw.to_csv(raw_csv_path, index=False)\n"
            "else:\n"
            "    df_raw = pd.read_csv(raw_csv_path)\n\n"
            "print(f'Raw dataset shape: {df_raw.shape}')\n"
            "df_raw.head()"
        ),
        md_cell("### 2. Inspect Missing Values and Duplicates in Raw Data"),
        code_cell(
            "print('Missing Values in Raw Data:')\n"
            "print(df_raw.isnull().sum())\n\n"
            "duplicate_count = df_raw.duplicated(subset=['feedback_text', 'sentiment', 'issue_category']).sum()\n"
            "print(f'\\nNumber of duplicate records: {duplicate_count}')"
        ),
        md_cell("### 3. Raw Class Distributions"),
        code_cell(
            "print('Raw Sentiment Distribution:')\n"
            "print(df_raw['sentiment'].str.strip().str.capitalize().value_counts())\n\n"
            "print('\\nRaw Issue Category Distribution:')\n"
            "print(df_raw['issue_category'].str.strip().str.title().value_counts())"
        )
    ]
    with open(os.path.join(notebooks_dir, "01_data_collection.ipynb"), "w", encoding="utf-8") as f:
        json.dump(make_notebook(nb1_cells), f, indent=2)

    # 2. 02_data_preprocessing.ipynb
    nb2_cells = [
        md_cell(
            "# 02. Data Cleaning & Text Preprocessing\n"
            "**Project**: AI-Powered Customer Support & Sentiment Analysis System\n\n"
            "This notebook details:\n"
            "- Deduplication and null/whitespace record purging\n"
            "- Schema and categorical label standardization\n"
            "- Negation-preserving text tokenization, custom stopwords, and WordNet lemmatization\n"
            "- Generating `data/processed/cleaned_feedback.csv`"
        ),
        code_cell(
            "import os\n"
            "import sys\n"
            "sys.path.insert(0, '..')\n\n"
            "import pandas as pd\n"
            "from src.preprocessing import clean_dataset, TextPreprocessor, clean_text, NEGATION_WORDS\n\n"
            "print(f'Number of preserved negation tokens: {len(NEGATION_WORDS)}')\n"
            "print('Sample negation tokens:', sorted(list(NEGATION_WORDS))[:10])"
        ),
        md_cell("### 1. Run Data Cleaning Pipeline"),
        code_cell(
            "raw_path = '../data/raw/raw_feedback.csv'\n"
            "processed_path = '../data/processed/cleaned_feedback.csv'\n\n"
            "df_clean = clean_dataset(raw_path, processed_path)\n"
            "print(f'Cleaned dataset shape: {df_clean.shape}')\n"
            "df_clean.head()"
        ),
        md_cell("### 2. Verify Preprocessor Transformations & Negation Preservation"),
        code_cell(
            "preprocessor = TextPreprocessor()\n\n"
            "samples = [\n"
            "    'I did NOT receive the package, it was NEVER delivered! https://tracking.com',\n"
            "    'The app crashes constantly... worst software ever! Contact me at support@mail.com',\n"
            "    'Great customer service, polite agents and quick refund resolution.'\n"
            "]\n\n"
            "for s in samples:\n"
            "    print('ORIGINAL:', s)\n"
            "    print('CLEANED: ', preprocessor.preprocess(s))\n"
            "    print('-' * 60)"
        ),
        md_cell("### 3. Preprocessed Dataset Distribution Checks"),
        code_cell(
            "print('Sentiments in Cleaned Dataset:')\n"
            "print(df_clean['sentiment'].value_counts())\n\n"
            "print('\\nIssue Categories in Cleaned Dataset:')\n"
            "print(df_clean['issue_category'].value_counts())"
        )
    ]
    with open(os.path.join(notebooks_dir, "02_data_preprocessing.ipynb"), "w", encoding="utf-8") as f:
        json.dump(make_notebook(nb2_cells), f, indent=2)

    # 3. 03_sentiment_analysis.ipynb
    nb3_cells = [
        md_cell(
            "# 03. Sentiment Analysis Model Development\n"
            "**Project**: AI-Powered Customer Support & Sentiment Analysis System\n\n"
            "This notebook covers:\n"
            "- Stratified train/test split (80/20)\n"
            "- Feature extraction with TF-IDF unigrams & bigrams\n"
            "- Training 4 candidate classifiers: Logistic Regression, Multinomial Naive Bayes, Linear SVM (Calibrated), Random Forest\n"
            "- Full metric evaluation (Accuracy, Precision, Recall, Macro F1, Weighted F1)\n"
            "- Confusion matrices and serialization of the best pipeline"
        ),
        code_cell(
            "import os\n"
            "import sys\n"
            "sys.path.insert(0, '..')\n\n"
            "import pandas as pd\n"
            "from src.sentiment import train_and_evaluate_sentiment_models"
        ),
        md_cell("### 1. Train and Benchmark Sentiment Models"),
        code_cell(
            "data_path = '../data/processed/cleaned_feedback.csv'\n"
            "models_dir = '../models'\n"
            "figures_dir = '../reports/figures'\n\n"
            "comparison_df, best_name, best_pipeline = train_and_evaluate_sentiment_models(\n"
            "    csv_path=data_path,\n"
            "    output_dir=models_dir,\n"
            "    figures_dir=figures_dir\n"
            ")\n"
            "comparison_df"
        ),
        md_cell("### 2. Best Model Architecture Details"),
        code_cell(
            "print(f'Selected Best Sentiment Model: {best_name}')\n"
            "print('Pipeline steps:', best_pipeline.named_steps)"
        )
    ]
    with open(os.path.join(notebooks_dir, "03_sentiment_analysis.ipynb"), "w", encoding="utf-8") as f:
        json.dump(make_notebook(nb3_cells), f, indent=2)

    # 4. 04_issue_classification.ipynb
    nb4_cells = [
        md_cell(
            "# 04. Customer Issue Category Classification\n"
            "**Project**: AI-Powered Customer Support & Sentiment Analysis System\n\n"
            "This notebook covers:\n"
            "- Multi-class classification across 6 categories:\n"
            "  1. Product Issue\n"
            "  2. Delivery Issue\n"
            "  3. Payment Issue\n"
            "  4. Technical Issue\n"
            "  5. Service Issue\n"
            "  6. General Feedback\n"
            "- Stratified benchmarking of 4 ML models\n"
            "- Confusion matrix visualizations and classification reports\n"
            "- Best issue classifier serialization"
        ),
        code_cell(
            "import os\n"
            "import sys\n"
            "sys.path.insert(0, '..')\n\n"
            "import pandas as pd\n"
            "from src.issue_classifier import train_and_evaluate_issue_models"
        ),
        md_cell("### 1. Train and Benchmark Issue Category Classifiers"),
        code_cell(
            "data_path = '../data/processed/cleaned_feedback.csv'\n"
            "models_dir = '../models'\n"
            "figures_dir = '../reports/figures'\n\n"
            "comparison_df, best_name, best_pipeline = train_and_evaluate_issue_models(\n"
            "    csv_path=data_path,\n"
            "    output_dir=models_dir,\n"
            "    figures_dir=figures_dir\n"
            ")\n"
            "comparison_df"
        ),
        md_cell("### 2. Best Model Architecture Details"),
        code_cell(
            "print(f'Selected Best Issue Category Model: {best_name}')\n"
            "print('Pipeline steps:', best_pipeline.named_steps)"
        )
    ]
    with open(os.path.join(notebooks_dir, "04_issue_classification.ipynb"), "w", encoding="utf-8") as f:
        json.dump(make_notebook(nb4_cells), f, indent=2)

    # 5. 05_model_comparison.ipynb
    nb5_cells = [
        md_cell(
            "# 05. Model Comparison, Inference Engine & Validation\n"
            "**Project**: AI-Powered Customer Support & Sentiment Analysis System\n\n"
            "This notebook provides:\n"
            "- Side-by-side benchmarking of all evaluated models for Sentiment & Issue Classification\n"
            "- Model selection justification based on Macro F1, calibration, and inference stability\n"
            "- Verification of `src.predictor.predict_feedback` across real-world customer test cases\n"
            "- Confidence score validation and probability distribution inspection"
        ),
        code_cell(
            "import os\n"
            "import sys\n"
            "sys.path.insert(0, '..')\n\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n"
            "from src.predictor import predict_feedback\n\n"
            "sent_cmp = pd.read_csv('../models/sentiment_model_comparison.csv')\n"
            "issue_cmp = pd.read_csv('../models/issue_model_comparison.csv')"
        ),
        md_cell("### 1. Sentiment Model Comparison Table"),
        code_cell("sent_cmp"),
        md_cell("### 2. Issue Classification Model Comparison Table"),
        code_cell("issue_cmp"),
        md_cell("### 3. End-to-End Real-Time Inference Testing"),
        code_cell(
            "sample_queries = [\n"
            "    'The delivery driver was two days late and crushed the package box.',\n"
            "    'I received a duplicate charge on my credit card statement for order #40291.',\n"
            "    'Sarah from customer support resolved my issue within five minutes! Best service ever.',\n"
            "    'The mobile app throws error 500 every time I open the checkout screen.',\n"
            "    'Please consider adding eco-friendly packaging options in your future store updates.'\n"
            "]\n\n"
            "results = []\n"
            "for text in sample_queries:\n"
            "    pred = predict_feedback(text)\n"
            "    results.append({\n"
            "        'Feedback': text,\n"
            "        'Sentiment': pred['sentiment'],\n"
            "        'Sentiment Confidence': f\"{pred['sentiment_confidence']:.2%}\",\n"
            "        'Issue Category': pred['issue_category'],\n"
            "        'Issue Confidence': f\"{pred['issue_confidence']:.2%}\"\n"
            "    })\n\n"
            "pd.DataFrame(results)"
        )
    ]
    with open(os.path.join(notebooks_dir, "05_model_comparison.ipynb"), "w", encoding="utf-8") as f:
        json.dump(make_notebook(nb5_cells), f, indent=2)

    print("All 5 Jupyter notebooks generated successfully.")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    nb_dir = os.path.join(base_dir, "notebooks")
    generate_all_notebooks(nb_dir)
