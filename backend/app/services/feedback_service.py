"""
Feedback Service handling SQLite database querying, filtering, search, and pagination.
"""

from typing import Optional
from backend.app.core.database import get_db_connection
from backend.app.models.schemas import FeedbackListResponse, FeedbackItem


def get_feedback_list(
    sentiment: Optional[str] = None,
    issue_category: Optional[str] = None,
    search: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    limit: int = 20
) -> FeedbackListResponse:
    """
    Retrieves a paginated list of customer feedback records matching filter criteria.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    conditions = []
    params = []

    if sentiment and sentiment.strip():
        conditions.append("sentiment = ?")
        params.append(sentiment.strip())

    if issue_category and issue_category.strip():
        conditions.append("issue_category = ?")
        params.append(issue_category.strip())

    if search and search.strip():
        conditions.append("(feedback_text LIKE ? OR feedback_id LIKE ?)")
        search_pattern = f"%{search.strip()}%"
        params.extend([search_pattern, search_pattern])

    if start_date and start_date.strip():
        conditions.append("feedback_date >= ?")
        params.append(start_date.strip())

    if end_date and end_date.strip():
        conditions.append("feedback_date <= ?")
        params.append(end_date.strip())

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    # Count total matching records
    count_query = f"SELECT COUNT(*) FROM feedback {where_clause}"
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]

    # Paginated select
    offset = max(0, (page - 1) * limit)
    data_query = f"""
        SELECT id, feedback_id, feedback_text, sentiment, issue_category, feedback_date, created_at
        FROM feedback
        {where_clause}
        ORDER BY feedback_date DESC, id DESC
        LIMIT ? OFFSET ?
    """
    cursor.execute(data_query, params + [limit, offset])
    rows = cursor.fetchall()
    conn.close()

    items = [
        FeedbackItem(
            id=row["id"],
            feedback_id=row["feedback_id"],
            feedback_text=row["feedback_text"],
            sentiment=row["sentiment"],
            issue_category=row["issue_category"],
            feedback_date=row["feedback_date"],
            created_at=row["created_at"]
        )
        for row in rows
    ]

    return FeedbackListResponse(
        data=items,
        page=page,
        limit=limit,
        total=total
    )


def get_feedback_by_id(feedback_id: str) -> Optional[FeedbackItem]:
    """
    Fetches a single feedback record by feedback_id or numeric id.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, feedback_id, feedback_text, sentiment, issue_category, feedback_date, created_at
        FROM feedback
        WHERE feedback_id = ? OR CAST(id AS TEXT) = ?
    """, (feedback_id, feedback_id))
    
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return FeedbackItem(
        id=row["id"],
        feedback_id=row["feedback_id"],
        feedback_text=row["feedback_text"],
        sentiment=row["sentiment"],
        issue_category=row["issue_category"],
        feedback_date=row["feedback_date"],
        created_at=row["created_at"]
    )
