"""
Interactive Plotly charts for Sentiment & Customer Issue Analytics.
Supports seamless switching between Light and Dark themes.
"""

from typing import Dict
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


SENTIMENT_COLORS = {
    "Positive": "#22c55e",
    "Negative": "#ef4444",
    "Neutral": "#0ea5e9"
}

CATEGORY_COLORS = {
    "Product Issue": "#f97316",
    "Delivery Issue": "#3b82f6",
    "Payment Issue": "#ec4899",
    "Technical Issue": "#8b5cf6",
    "Service Issue": "#14b8a6",
    "General Feedback": "#64748b"
}


def _apply_theme(fig: go.Figure, is_dark: bool, title: str = "") -> go.Figure:
    """Applies consistent typography, background, and margin styling."""
    bg_color = "#1e293b" if is_dark else "#ffffff"
    paper_color = "#0f172a" if is_dark else "#ffffff"
    font_color = "#f8fafc" if is_dark else "#1e293b"
    grid_color = "#334155" if is_dark else "#f1f5f9"

    fig.update_layout(
        template="plotly_dark" if is_dark else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=font_color, family="Inter, system-ui, sans-serif"),
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=15, color=font_color),
            x=0.01,
            y=0.96
        ),
        margin=dict(l=40, r=30, t=50, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        )
    )
    fig.update_xaxes(showgrid=True, gridcolor=grid_color, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=grid_color, zeroline=False)
    return fig


def plot_sentiment_donut(df: pd.DataFrame, is_dark: bool = False) -> go.Figure:
    """Donut chart showing overall sentiment proportions."""
    counts = df["sentiment"].value_counts().reset_index()
    counts.columns = ["sentiment", "count"]
    
    fig = px.pie(
        counts,
        names="sentiment",
        values="count",
        hole=0.55,
        color="sentiment",
        color_discrete_map=SENTIMENT_COLORS
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hoverinfo="label+value+percent",
        marker=dict(line=dict(color="#0f172a" if is_dark else "#ffffff", width=2))
    )
    return _apply_theme(fig, is_dark, "Sentiment Distribution")


def plot_issue_category_bar(df: pd.DataFrame, is_dark: bool = False) -> go.Figure:
    """Horizontal bar chart of issue categories sorted by frequency."""
    counts = df["issue_category"].value_counts().reset_index()
    counts.columns = ["issue_category", "count"]
    counts = counts.sort_values(by="count", ascending=True)

    fig = px.bar(
        counts,
        x="count",
        y="issue_category",
        orientation="h",
        color="issue_category",
        color_discrete_map=CATEGORY_COLORS,
        text="count"
    )
    fig.update_traces(textposition="outside", showlegend=False)
    fig.update_layout(xaxis_title="Feedback Count", yaxis_title="")
    return _apply_theme(fig, is_dark, "Issue Category Distribution")


def plot_monthly_trend(df: pd.DataFrame, is_dark: bool = False) -> go.Figure:
    """Stacked bar chart of monthly feedback volume broken down by sentiment."""
    monthly = df.groupby(["year_month", "sentiment"]).size().reset_index(name="count")
    monthly = monthly.sort_values(by="year_month")

    fig = px.bar(
        monthly,
        x="year_month",
        y="count",
        color="sentiment",
        color_discrete_map=SENTIMENT_COLORS,
        barmode="stack"
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Feedback Volume")
    return _apply_theme(fig, is_dark, "Monthly Feedback Volume & Trend")


def plot_sentiment_trend(df: pd.DataFrame, is_dark: bool = False) -> go.Figure:
    """Line chart tracking sentiment volume changes over time."""
    trend = df.groupby(["year_month", "sentiment"]).size().reset_index(name="count")
    trend = trend.sort_values(by="year_month")

    fig = px.line(
        trend,
        x="year_month",
        y="count",
        color="sentiment",
        color_discrete_map=SENTIMENT_COLORS,
        markers=True
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Feedback Count")
    return _apply_theme(fig, is_dark, "Sentiment Trajectory Over Time")


def plot_issue_trend(df: pd.DataFrame, is_dark: bool = False) -> go.Figure:
    """Multi-line trend chart showing temporal shifts in issue types."""
    trend = df.groupby(["year_month", "issue_category"]).size().reset_index(name="count")
    trend = trend.sort_values(by="year_month")

    fig = px.line(
        trend,
        x="year_month",
        y="count",
        color="issue_category",
        color_discrete_map=CATEGORY_COLORS,
        markers=True
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Ticket Volume")
    return _apply_theme(fig, is_dark, "Issue Category Trends Over Time")


def plot_sentiment_issue_heatmap(df: pd.DataFrame, is_dark: bool = False) -> go.Figure:
    """Heatmap displaying sentiment percentage breakdown for each issue category."""
    ct = pd.crosstab(df["issue_category"], df["sentiment"], normalize="index") * 100
    for col in ["Negative", "Neutral", "Positive"]:
        if col not in ct.columns:
            ct[col] = 0.0
    ct = ct[["Negative", "Neutral", "Positive"]].round(1)

    fig = go.Figure(
        data=go.Heatmap(
            z=ct.values,
            x=ct.columns,
            y=ct.index,
            colorscale="Viridis" if is_dark else "Blues",
            text=ct.values,
            texttemplate="%{text}%",
            hoverinfo="x+y+z"
        )
    )
    fig.update_layout(xaxis_title="Sentiment", yaxis_title="")
    return _apply_theme(fig, is_dark, "Sentiment vs Issue Category Heatmap (%)")


def plot_category_sentiment_stacked(df: pd.DataFrame, is_dark: bool = False) -> go.Figure:
    """Stacked percentage bar chart showing sentiment mix within each category."""
    ct = pd.crosstab(df["issue_category"], df["sentiment"], normalize="index") * 100
    for col in ["Negative", "Neutral", "Positive"]:
        if col not in ct.columns:
            ct[col] = 0.0
    ct = ct[["Negative", "Neutral", "Positive"]].reset_index()
    melted = pd.melt(ct, id_vars=["issue_category"], value_vars=["Negative", "Neutral", "Positive"],
                     var_name="sentiment", value_name="percentage")

    fig = px.bar(
        melted,
        x="percentage",
        y="issue_category",
        color="sentiment",
        color_discrete_map=SENTIMENT_COLORS,
        orientation="h",
        text=melted["percentage"].apply(lambda v: f"{v:.1f}%")
    )
    fig.update_layout(barmode="stack", xaxis_title="Percentage (%)", yaxis_title="")
    return _apply_theme(fig, is_dark, "Sentiment Composition by Issue Category (%)")


def plot_probabilities_bar(prob_dict: Dict[str, float], title: str, is_dark: bool = False) -> go.Figure:
    """Horizontal bar chart showing model calibrated posterior probabilities for classes."""
    data = pd.DataFrame(list(prob_dict.items()), columns=["class", "probability"]).sort_values(
        by="probability", ascending=True
    )
    data["pct_str"] = data["probability"].apply(lambda p: f"{p*100:.1f}%")

    fig = px.bar(
        data,
        x="probability",
        y="class",
        orientation="h",
        text="pct_str"
    )
    fig.update_traces(
        marker_color="#6366f1",
        textposition="outside"
    )
    fig.update_layout(xaxis_range=[0, 1.15], xaxis_title="Model Probability", yaxis_title="")
    return _apply_theme(fig, is_dark, title)
