"""
Analytics Service computing live operational metrics, distributions, trends, and cross-tabulations.
"""

from collections import defaultdict
from backend.app.core.database import get_db_connection
from backend.app.models.schemas import (
    DashboardResponse,
    DistributionItem,
    MonthlyFeedbackItem,
    SentimentTrendItem,
    SentimentAnalyticsResponse,
    IssueAnalyticsResponse,
    CategoryStatItem
)


def get_dashboard_data() -> DashboardResponse:
    """
    Computes all executive dashboard KPIs, distributions, and trends from SQLite.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Total Count
    cursor.execute("SELECT COUNT(*) FROM feedback")
    total = cursor.fetchone()[0]

    if total == 0:
        conn.close()
        return DashboardResponse(
            total_feedback=0,
            positive_feedback=0,
            negative_feedback=0,
            neutral_feedback=0,
            positive_percentage=0.0,
            negative_percentage=0.0,
            neutral_percentage=0.0,
            most_common_issue="None",
            most_common_issue_count=0,
            sentiment_distribution=[],
            issue_distribution=[],
            monthly_feedback=[],
            sentiment_trend=[],
            sentiment_issue_matrix=[]
        )

    # 2. Sentiment Counts
    cursor.execute("SELECT sentiment, COUNT(*) as cnt FROM feedback GROUP BY sentiment")
    sent_dict = {row["sentiment"]: row["cnt"] for row in cursor.fetchall()}
    pos_cnt = sent_dict.get("Positive", 0)
    neg_cnt = sent_dict.get("Negative", 0)
    neu_cnt = sent_dict.get("Neutral", 0)

    sentiment_dist = [
        DistributionItem(name=s, count=sent_dict.get(s, 0), percentage=round((sent_dict.get(s, 0) / total) * 100, 2))
        for s in ["Positive", "Negative", "Neutral"]
    ]

    # 3. Issue Category Counts
    cursor.execute("SELECT issue_category, COUNT(*) as cnt FROM feedback GROUP BY issue_category ORDER BY cnt DESC")
    issue_rows = cursor.fetchall()
    top_issue = issue_rows[0]["issue_category"] if issue_rows else "N/A"
    top_issue_cnt = issue_rows[0]["cnt"] if issue_rows else 0

    issue_dist = [
        DistributionItem(
            name=row["issue_category"],
            count=row["cnt"],
            percentage=round((row["cnt"] / total) * 100, 2)
        )
        for row in issue_rows
    ]

    # 4. Monthly Feedback & Sentiment Trends
    cursor.execute("""
        SELECT SUBSTR(feedback_date, 1, 7) as month, sentiment, COUNT(*) as cnt
        FROM feedback
        GROUP BY month, sentiment
        ORDER BY month ASC
    """)
    month_data = defaultdict(lambda: {"total": 0, "Positive": 0, "Negative": 0, "Neutral": 0})
    for row in cursor.fetchall():
        m = row["month"]
        s = row["sentiment"]
        c = row["cnt"]
        month_data[m][s] = c
        month_data[m]["total"] += c

    monthly_feedback = []
    sentiment_trend = []
    for m in sorted(month_data.keys()):
        monthly_feedback.append(MonthlyFeedbackItem(
            month=m,
            total=month_data[m]["total"],
            positive=month_data[m]["Positive"],
            negative=month_data[m]["Negative"],
            neutral=month_data[m]["Neutral"]
        ))
        sentiment_trend.append(SentimentTrendItem(
            month=m,
            positive=month_data[m]["Positive"],
            negative=month_data[m]["Negative"],
            neutral=month_data[m]["Neutral"]
        ))

    # 5. Sentiment vs Issue Category Cross-tabulation
    cursor.execute("""
        SELECT issue_category, sentiment, COUNT(*) as cnt
        FROM feedback
        GROUP BY issue_category, sentiment
    """)
    matrix_dict = defaultdict(lambda: {"category": "", "Positive": 0, "Negative": 0, "Neutral": 0, "total": 0})
    for row in cursor.fetchall():
        cat = row["issue_category"]
        s = row["sentiment"]
        c = row["cnt"]
        matrix_dict[cat]["category"] = cat
        matrix_dict[cat][s] = c
        matrix_dict[cat]["total"] += c

    matrix_list = []
    for cat, data in matrix_dict.items():
        t = data["total"]
        matrix_list.append({
            "category": cat,
            "total": t,
            "positive": data["Positive"],
            "negative": data["Negative"],
            "neutral": data["Neutral"],
            "positive_pct": round((data["Positive"] / t) * 100, 1) if t > 0 else 0,
            "negative_pct": round((data["Negative"] / t) * 100, 1) if t > 0 else 0,
            "neutral_pct": round((data["Neutral"] / t) * 100, 1) if t > 0 else 0,
        })

    conn.close()

    return DashboardResponse(
        total_feedback=total,
        positive_feedback=pos_cnt,
        negative_feedback=neg_cnt,
        neutral_feedback=neu_cnt,
        positive_percentage=round((pos_cnt / total) * 100, 2),
        negative_percentage=round((neg_cnt / total) * 100, 2),
        neutral_percentage=round((neu_cnt / total) * 100, 2),
        most_common_issue=top_issue,
        most_common_issue_count=top_issue_cnt,
        sentiment_distribution=sentiment_dist,
        issue_distribution=issue_dist,
        monthly_feedback=monthly_feedback,
        sentiment_trend=sentiment_trend,
        sentiment_issue_matrix=matrix_list
    )


def get_sentiment_analytics() -> SentimentAnalyticsResponse:
    """
    Computes dedicated sentiment metrics, trends, and category associations.
    """
    dash = get_dashboard_data()
    total = dash.total_feedback

    # Identify extrema from matrix
    highest_neg = max(dash.sentiment_issue_matrix, key=lambda x: x["negative_pct"], default={})
    highest_pos = max(dash.sentiment_issue_matrix, key=lambda x: x["positive_pct"], default={})

    return SentimentAnalyticsResponse(
        positive_percentage=dash.positive_percentage,
        negative_percentage=dash.negative_percentage,
        neutral_percentage=dash.neutral_percentage,
        total_feedback=total,
        sentiment_distribution=dash.sentiment_distribution,
        monthly_sentiment_trend=dash.monthly_feedback,
        sentiment_by_issue=dash.sentiment_issue_matrix,
        highest_negative_category=highest_neg,
        highest_positive_category=highest_pos
    )


def get_issue_analytics() -> IssueAnalyticsResponse:
    """
    Computes dedicated issue category statistics, frequencies, and historical trends.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    dash = get_dashboard_data()
    total = dash.total_feedback

    # Monthly issue category trend
    cursor.execute("""
        SELECT SUBSTR(feedback_date, 1, 7) as month, issue_category, COUNT(*) as cnt
        FROM feedback
        GROUP BY month, issue_category
        ORDER BY month ASC
    """)
    issue_monthly = defaultdict(lambda: {})
    for row in cursor.fetchall():
        issue_monthly[row["month"]][row["issue_category"]] = row["cnt"]
    conn.close()

    trend_list = []
    for m in sorted(issue_monthly.keys()):
        entry = {"month": m}
        entry.update(issue_monthly[m])
        trend_list.append(entry)

    # Category detailed stats
    cat_stats = []
    for item in dash.sentiment_issue_matrix:
        cat_stats.append(CategoryStatItem(
            category=item["category"],
            total_tickets=item["total"],
            percentage=round((item["total"] / total) * 100, 2) if total > 0 else 0,
            negative_count=item["negative"],
            negative_rate=item["negative_pct"],
            positive_count=item["positive"],
            positive_rate=item["positive_pct"],
            neutral_count=item["neutral"]
        ))

    highest_neg = max(dash.sentiment_issue_matrix, key=lambda x: x["negative"], default={})

    return IssueAnalyticsResponse(
        issue_distribution=dash.issue_distribution,
        issue_percentages=dash.issue_distribution,
        issue_trend=trend_list,
        sentiment_by_issue=dash.sentiment_issue_matrix,
        category_statistics=cat_stats,
        most_reported_issue=dash.most_common_issue,
        highest_negative_issue=highest_neg.get("category", "N/A")
    )
