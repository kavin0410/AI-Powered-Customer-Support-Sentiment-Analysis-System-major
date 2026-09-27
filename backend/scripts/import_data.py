"""
Standalone reproducible dataset import pipeline for SQLite database.
Reads cleaned Phase 1 dataset, validates columns, handles duplicates,
and populates the SQLite feedback repository.
"""

import os
import sys
import sqlite3
from datetime import datetime
import pandas as pd

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.app.core.config import DB_PATH, DATA_PATH
from backend.app.core.database import get_db_connection, init_db


def import_dataset(csv_path: str = DATA_PATH, db_path: str = DB_PATH) -> int:
    """
    Imports and validates feedback records from CSV into SQLite database.
    """
    print("=" * 60)
    print("AI CUSTOMER SUPPORT SYSTEM - DATASET IMPORT PIPELINE")
    print("=" * 60)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Source dataset not found at: '{csv_path}'")

    print(f"[1/4] Reading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    total_raw_rows = len(df)
    print(f"      Total records loaded from CSV: {total_raw_rows}")

    # Validate required columns
    required_cols = {"feedback_id", "feedback_text", "sentiment", "issue_category"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")

    print("[2/4] Validating schema and sanitizing records...")
    # Drop rows with null text or id
    clean_df = df.dropna(subset=["feedback_id", "feedback_text"]).copy()
    clean_df["feedback_id"] = clean_df["feedback_id"].astype(str).str.strip()
    clean_df["feedback_text"] = clean_df["feedback_text"].astype(str).str.strip()
    clean_df = clean_df[clean_df["feedback_text"].str.len() > 0]

    # De-duplicate by feedback_id
    initial_valid = len(clean_df)
    clean_df = clean_df.drop_duplicates(subset=["feedback_id"], keep="first")
    duplicates_removed = initial_valid - len(clean_df)
    if duplicates_removed > 0:
        print(f"      Removed {duplicates_removed} duplicate records.")

    print("[3/4] Ensuring database schema and indexes exist...")
    init_db()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check existing count before insert
    cursor.execute("SELECT COUNT(*) FROM feedback")
    count_before = cursor.fetchone()[0]

    print("[4/4] Inserting validated records into SQLite...")
    now_iso = datetime.now().isoformat()
    records = []
    for _, row in clean_df.iterrows():
        f_id = row["feedback_id"]
        f_text = row["feedback_text"]
        f_sent = str(row.get("sentiment", "Neutral")).strip()
        f_cat = str(row.get("issue_category", "General Feedback")).strip()
        f_date = str(row.get("date", datetime.now().strftime("%Y-%m-%d"))).strip()

        records.append((f_id, f_text, f_sent, f_cat, f_date, now_iso))

    cursor.executemany("""
        INSERT OR IGNORE INTO feedback (feedback_id, feedback_text, sentiment, issue_category, feedback_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, records)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM feedback")
    count_after = cursor.fetchone()[0]
    newly_inserted = count_after - count_before
    conn.close()

    print("=" * 60)
    print("IMPORT SUMMARY:")
    print(f"  - Database Path:         {db_path}")
    print(f"  - Valid Source Records:  {len(clean_df)}")
    print(f"  - Pre-existing Records:  {count_before}")
    print(f"  - Newly Added Records:   {newly_inserted}")
    print(f"  - Total Active Records:  {count_after}")
    print("=" * 60)
    print("Dataset import completed successfully!")
    return count_after


if __name__ == "__main__":
    try:
        import_dataset()
    except Exception as e:
        print(f"[ERROR] Dataset import failed: {e}", file=sys.stderr)
        sys.exit(1)
