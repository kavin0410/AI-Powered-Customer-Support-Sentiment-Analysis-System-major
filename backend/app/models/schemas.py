"""
Pydantic schemas for request validation and response serialization.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


# Health Check Schema
class HealthResponse(BaseModel):
    status: str = "healthy"
    service: str = "AI Customer Support API"
    sentiment_model: bool = True
    issue_model: bool = True
    database_connected: bool = True
    total_records: int = 0


# Prediction Schemas
class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=3, max_length=3000, description="Customer feedback string to classify")


class PredictionResponse(BaseModel):
    text: str
    sentiment: str
    sentiment_confidence: float
    issue_category: str
    issue_confidence: float
    attention_level: str
    explanation: str
    recommended_action: str
    sentiment_probabilities: Dict[str, float]
    issue_probabilities: Dict[str, float]


# Feedback Schemas
class FeedbackItem(BaseModel):
    id: int
    feedback_id: str
    feedback_text: str
    sentiment: str
    issue_category: str
    feedback_date: str
    created_at: str


class FeedbackListResponse(BaseModel):
    data: List[FeedbackItem]
    page: int
    limit: int
    total: int


# Dashboard Schemas
class DistributionItem(BaseModel):
    name: str
    count: int
    percentage: float


class MonthlyFeedbackItem(BaseModel):
    month: str
    total: int
    positive: int
    negative: int
    neutral: int


class SentimentTrendItem(BaseModel):
    month: str
    positive: int
    negative: int
    neutral: int


class DashboardResponse(BaseModel):
    total_feedback: int
    positive_feedback: int
    negative_feedback: int
    neutral_feedback: int
    positive_percentage: float
    negative_percentage: float
    neutral_percentage: float
    most_common_issue: str
    most_common_issue_count: int
    sentiment_distribution: List[DistributionItem]
    issue_distribution: List[DistributionItem]
    monthly_feedback: List[MonthlyFeedbackItem]
    sentiment_trend: List[SentimentTrendItem]
    sentiment_issue_matrix: List[Dict[str, Any]]


# Analytics Schemas
class SentimentAnalyticsResponse(BaseModel):
    positive_percentage: float
    negative_percentage: float
    neutral_percentage: float
    total_feedback: int
    sentiment_distribution: List[DistributionItem]
    monthly_sentiment_trend: List[MonthlyFeedbackItem]
    sentiment_by_issue: List[Dict[str, Any]]
    highest_negative_category: Dict[str, Any]
    highest_positive_category: Dict[str, Any]


class CategoryStatItem(BaseModel):
    category: str
    total_tickets: int
    percentage: float
    negative_count: int
    negative_rate: float
    positive_count: int
    positive_rate: float
    neutral_count: int


class IssueAnalyticsResponse(BaseModel):
    issue_distribution: List[DistributionItem]
    issue_percentages: List[DistributionItem]
    issue_trend: List[Dict[str, Any]]
    sentiment_by_issue: List[Dict[str, Any]]
    category_statistics: List[CategoryStatItem]
    most_reported_issue: str
    highest_negative_issue: str


# Business Insight Schema
class InsightItem(BaseModel):
    type: str = "observation"
    title: str
    description: str
    metric: str
    action: Optional[str] = None
