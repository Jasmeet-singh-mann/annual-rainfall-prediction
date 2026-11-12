"""
RainCast AI - Interactive Plotly Charting Engine
Builds dark-navy styled meteorological charts with responsive layouts.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

FRONTEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = FRONTEND_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
for p in [str(PROJECT_ROOT), str(BACKEND_DIR), str(FRONTEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from config import THEME


def get_base_layout(title: str = "", height: int = 400) -> go.Layout:
    """Returns a unified dark theme layout for all Plotly figures."""
    return go.Layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(family="Manrope, Inter, sans-serif", size=15, color=THEME["text_primary"]),
            x=0.01,
            y=0.96
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=45, r=25, t=50, b=40),
        height=height,
        font=dict(family="Inter, sans-serif", color=THEME["text_secondary"], size=11),
        xaxis=dict(
            showgrid=True,
            gridcolor=THEME["border"],
            zeroline=False,
            color=THEME["text_secondary"]
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=THEME["border"],
            zeroline=False,
            color=THEME["text_secondary"]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10, color=THEME["text_secondary"])
        )
    )


def plot_historical_trend(df: pd.DataFrame, normal_lpa: float, title: str = "Annual Rainfall Trend (1901 – 2024)") -> go.Figure:
    """Line chart showing historical rainfall, 5-yr moving average, and LPA baseline."""
    df_sorted = df.sort_values(by="year").copy()
    df_sorted["ma5"] = df_sorted["annual_rainfall"].rolling(5, min_periods=2).mean()

    fig = go.Figure(layout=get_base_layout(title, height=420))

    # Actual Annual Rainfall
    fig.add_trace(go.Scatter(
        x=df_sorted["year"],
        y=df_sorted["annual_rainfall"],
        mode="lines+markers",
        name="Annual Rainfall",
        line=dict(color="#4F9DDA", width=1.5),
        marker=dict(size=4, color="#4F9DDA"),
        hovertemplate="Year %{x}<br>Rainfall: <b>%{y:,.1f} mm</b><extra></extra>"
    ))

    # 5-Year Moving Average
    fig.add_trace(go.Scatter(
        x=df_sorted["year"],
        y=df_sorted["ma5"],
        mode="lines",
        name="5-Yr Moving Average",
        line=dict(color="#16B8D4", width=2.5),
        hovertemplate="5-Yr Avg: <b>%{y:,.1f} mm</b><extra></extra>"
    ))

    # Normal LPA Reference Line
    fig.add_trace(go.Scatter(
        x=[df_sorted["year"].min(), df_sorted["year"].max()],
        y=[normal_lpa, normal_lpa],
        mode="lines",
        name=f"Normal (LPA: {normal_lpa:.1f} mm)",
        line=dict(color="#27C58A", width=2, dash="dash"),
        hoverinfo="skip"
    ))

    fig.update_xaxes(title="Observation Year")
    fig.update_yaxes(title="Annual Precipitation (mm)")
    return fig


def plot_monthly_distribution(monthly_series: pd.Series, location_name: str = "") -> go.Figure:
    """Bar chart of monthly precipitation with Southwest Monsoon months highlighted."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    vals = [float(monthly_series.get(f"{m.lower()}_rainfall", 0.0)) for m in months]
    total = max(sum(vals), 1.0)
    pcts = [(v / total) * 100.0 for v in vals]

    # Southwest Monsoon months (Jun, Jul, Aug, Sep) colored in Cyan
    colors_list = ["#16B8D4" if i in [5, 6, 7, 8] else "#23496D" for i in range(12)]

    fig = go.Figure(layout=get_base_layout(f"Monthly Rainfall Climatology — {location_name}", height=380))
    fig.add_trace(go.Bar(
        x=months,
        y=vals,
        marker=dict(color=colors_list, line=dict(color="#1A3A5A", width=1)),
        text=[f"{p:.1f}%" if p > 3 else "" for p in pcts],
        textposition="outside",
        textfont=dict(size=10, color=THEME["text_primary"]),
        hovertemplate="%{x}: <b>%{y:,.1f} mm</b> (%{text})<extra></extra>"
    ))

    fig.update_xaxes(title="Month (Highlighted = SW Monsoon)")
    fig.update_yaxes(title="Rainfall (mm)")
    return fig


def plot_rainfall_anomalies(df: pd.DataFrame, title: str = "Annual Rainfall Anomalies (% Departure from Normal)") -> go.Figure:
    """Waterfall/Bar chart of percentage departure from normal LPA."""
    df_sorted = df.sort_values(by="year").copy()
    colors_bars = ["#27C58A" if a >= 0 else "#E66A72" for a in df_sorted["anomaly_pct"]]

    fig = go.Figure(layout=get_base_layout(title, height=360))
    fig.add_trace(go.Bar(
        x=df_sorted["year"],
        y=df_sorted["anomaly_pct"],
        marker=dict(color=colors_bars),
        hovertemplate="Year %{x}: <b>%{y:+.1f}%</b><extra></extra>"
    ))

    # Add reference band for IMD Normal range (-19% to +19%)
    fig.add_hrect(
        y0=-19.0, y1=19.0,
        fillcolor="rgba(39, 197, 138, 0.08)",
        line_width=1, line_dash="dot", line_color="rgba(39, 197, 138, 0.3)",
        annotation_text="IMD Normal Band (±19%)", annotation_position="top left",
        annotation_font=dict(size=9, color="#27C58A")
    )

    fig.update_xaxes(title="Year")
    fig.update_yaxes(title="Anomaly (%)")
    return fig


def plot_multi_year_forecast(
    history_df: pd.DataFrame,
    predicted_rainfall_mm: float,
    ci_lower: float,
    ci_upper: float,
    forecast_year: int,
    normal_lpa: float
) -> go.Figure:
    """Forecast chart showing recent history stitched to predicted year with 90% confidence interval."""
    recent_hist = history_df.sort_values(by="year").tail(15).copy()

    fig = go.Figure(layout=get_base_layout(f"Rainfall Projection Horizon to {forecast_year}", height=420))

    # Recent Ground Truth
    fig.add_trace(go.Scatter(
        x=recent_hist["year"],
        y=recent_hist["annual_rainfall"],
        mode="lines+markers",
        name="Observed Rainfall",
        line=dict(color="#4F9DDA", width=2),
        marker=dict(size=5, color="#4F9DDA"),
        hovertemplate="Year %{x}: <b>%{y:,.1f} mm</b> (Observed)<extra></extra>"
    ))

    # Projection point & connection
    last_year = int(recent_hist["year"].iloc[-1])
    last_val = float(recent_hist["annual_rainfall"].iloc[-1])

    proj_years = [last_year, forecast_year]
    proj_vals = [last_val, predicted_rainfall_mm]

    fig.add_trace(go.Scatter(
        x=proj_years,
        y=proj_vals,
        mode="lines",
        name="ML Projection Trajectory",
        line=dict(color="#16B8D4", width=2.5, dash="dash"),
        hoverinfo="skip"
    ))

    # Predicted Point
    fig.add_trace(go.Scatter(
        x=[forecast_year],
        y=[predicted_rainfall_mm],
        mode="markers",
        name=f"Predicted ({forecast_year})",
        marker=dict(size=11, color="#16B8D4", symbol="diamond", line=dict(color="#FFFFFF", width=1.5)),
        hovertemplate=f"Forecast {forecast_year}: <b>{predicted_rainfall_mm:,.1f} mm</b><extra></extra>"
    ))

    # 90% Confidence Interval Error Bar
    fig.add_trace(go.Scatter(
        x=[forecast_year, forecast_year],
        y=[ci_lower, ci_upper],
        mode="lines",
        name="90% Confidence Interval",
        line=dict(color="#16B8D4", width=4),
        hoverinfo="skip"
    ))

    # Normal Line
    fig.add_trace(go.Scatter(
        x=[recent_hist["year"].min(), forecast_year],
        y=[normal_lpa, normal_lpa],
        mode="lines",
        name=f"Normal (LPA: {normal_lpa:.1f} mm)",
        line=dict(color="#27C58A", width=1.5, dash="dot"),
        hoverinfo="skip"
    ))

    fig.update_xaxes(title="Year", dtick=2)
    fig.update_yaxes(title="Annual Rainfall (mm)")
    return fig


def plot_actual_vs_predicted(eval_df: pd.DataFrame) -> go.Figure:
    """Parity scatter plot (Actual vs Predicted) on untouched test period (2016-2024)."""
    fig = go.Figure(layout=get_base_layout("Actual vs Predicted Rainfall (Out-of-Sample Test Period 2016–2024)", height=430))

    # Reference 45-degree line (Perfect Prediction)
    min_val = min(eval_df["actual"].min(), eval_df["predicted"].min()) * 0.9
    max_val = max(eval_df["actual"].max(), eval_df["predicted"].max()) * 1.05

    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode="lines",
        name="Perfect Parity (y = x)",
        line=dict(color="#F4B942", width=1.5, dash="dash"),
        hoverinfo="skip"
    ))

    # Scatter of test samples
    fig.add_trace(go.Scatter(
        x=eval_df["actual"],
        y=eval_df["predicted"],
        mode="markers",
        name="Test Evaluation Samples",
        marker=dict(
            size=6,
            color="#16B8D4",
            opacity=0.75,
            line=dict(color="#071525", width=0.5)
        ),
        text=eval_df.apply(lambda r: f"{r['district']}, {r['state']} ({r['year']})", axis=1),
        hovertemplate="<b>%{text}</b><br>Actual: %{x:,.1f} mm<br>Predicted: %{y:,.1f} mm<extra></extra>"
    ))

    fig.update_xaxes(title="Observed Actual Rainfall (mm)")
    fig.update_yaxes(title="Predicted Rainfall (mm)")
    return fig


def plot_residuals_distribution(eval_df: pd.DataFrame) -> go.Figure:
    """Histogram of prediction residuals (Actual - Predicted)."""
    fig = go.Figure(layout=get_base_layout("Residual Error Distribution (Actual – Predicted)", height=380))
    fig.add_trace(go.Histogram(
        x=eval_df["residual"],
        nbinsx=35,
        marker=dict(color="#4F9DDA", line=dict(color="#1A3A5A", width=1)),
        hovertemplate="Error Bin: %{x} mm<br>Count: %{y}<extra></extra>"
    ))

    # Vertical line at zero error
    fig.add_vline(x=0, line_width=2, line_dash="dash", line_color="#27C58A")
    fig.update_xaxes(title="Residual Error (mm)")
    fig.update_yaxes(title="Sample Frequency")
    return fig


def plot_feature_importances(imp_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of feature importance ranking."""
    fig = go.Figure(layout=get_base_layout("Machine Learning Feature Importance Rankings", height=380))
    fig.add_trace(go.Bar(
        y=imp_df["Description"],
        x=imp_df["Importance"],
        orientation="h",
        marker=dict(
            color=imp_df["Importance"],
            colorscale=[[0, "#123758"], [0.5, "#4F9DDA"], [1, "#16B8D4"]],
            line=dict(color="#1A3A5A", width=1)
        ),
        hovertemplate="%{y}: <b>%{x:.3f}</b><extra></extra>"
    ))
    fig.update_xaxes(title="Relative Importance Weight")
    fig.update_yaxes(autorange="reversed")
    return fig

