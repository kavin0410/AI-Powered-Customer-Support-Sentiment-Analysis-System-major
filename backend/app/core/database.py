"""
SQLite database management and dataset seeding.
"""

import os
import sqlite3
from datetime import datetime
import pandas as pd
from backend.app.core.config import DB_PATH, DATA_PATH


def get_db_connection() -> sqlite3.Connection:
    """Returns a SQLite connection configured with Row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes SQLite tables and automatically seeds from cleaned_feedback.csv if empty.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_id TEXT UNIQUE NOT NULL,
            feedback_text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            issue_category TEXT NOT NULL,
            feedback_date TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()

    # Check if table already contains data
    cursor.execute("SELECT COUNT(*) FROM feedback")
    count = cursor.fetchone()[0]

    if count == 0:
        if os.path.exists(DATA_PATH):
            print(f"[DB INIT] Importing baseline feedback records from '{DATA_PATH}'...")
            df = pd.read_csv(DATA_PATH)
            
            records_to_insert = []
            now_iso = datetime.now().isoformat()
            
            for _, row in df.iterrows():
                f_id = str(row.get("feedback_id", "")).strip()
                f_text = str(row.get("feedback_text", "")).strip()
                f_sent = str(row.get("sentiment", "")).strip()
                f_cat = str(row.get("issue_category", "")).strip()
                f_date = str(row.get("date", "")).strip()
                
                if f_id and f_text:
                    records_to_insert.append((
                        f_id,
                        f_text,
                        f_sent,
                        f_cat,
                        f_date,
                        now_iso
                    ))

            cursor.executemany("""
                INSERT OR IGNORE INTO feedback (feedback_id, feedback_text, sentiment, issue_category, feedback_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, records_to_insert)
            conn.commit()
            print(f"[DB INIT] Successfully seeded {len(records_to_insert)} records into SQLite database.")
        else:
            print(f"[DB INIT] Warning: Data path '{DATA_PATH}' does not exist. Initialized empty database.")

    conn.close()
