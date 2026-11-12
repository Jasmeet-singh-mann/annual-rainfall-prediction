"""
RainCast AI - Automated Report Generation Engine
Produces executive PDF and CSV analytical climate reports with ML predictions,
uncertainty metrics, and AI interpretation.
"""

import sys
from pathlib import Path
BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
for p in [str(PROJECT_ROOT), str(BACKEND_DIR), str(FRONTEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import io
import datetime
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.units import inch

from config import APP_NAME, APP_TAGLINE, SCIENTIFIC_DISCLAIMER
from src.prediction import predict_annual_rainfall, get_cached_dataset
from src.genai_assistant import generate_prediction_explanation


def generate_pdf_report(state: str, district: str, forecast_year: int = 2027,
                        model_name: str = "Random Forest Regressor",
                        report_type: str = "Comprehensive Executive Report",
                        api_key: str = None) -> bytes:
    """
    Builds a professional executive climate report in PDF format using ReportLab.
    Returns bytes suitable for Streamlit download button.
    """
    pred_data = predict_annual_rainfall(state, district, forecast_year, model_name=model_name)
    ai_interpretation = generate_prediction_explanation(pred_data, language="English", api_key=api_key)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#071525'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#16B8D4')
    )
    section_heading = ParagraphStyle(
        'SectionH',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0D2035'),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#2A3A4A')
    )
    disclaimer_style = ParagraphStyle(
        'Discl',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#6B7280')
    )

    elements = []

    # Header / Branding
    elements.append(Paragraph(f"{APP_NAME} — Annual Rainfall & Climate Analytics Report", title_style))
    elements.append(Paragraph(f"{APP_TAGLINE} | Report Type: {report_type}", subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#16B8D4'), spaceAfter=12))

    # Meta Info Table
    gen_time = datetime.datetime.now().strftime("%d %B %Y, %H:%M UTC")
    meta_data = [
        [
            Paragraph("<b>Geographical Target:</b>", body_style),
            Paragraph(f"{district}, {state} (Lat: {pred_data['latitude']}°N, Lon: {pred_data['longitude']}°E)", body_style),
            Paragraph("<b>Report Date:</b>", body_style),
            Paragraph(gen_time, body_style)
        ],
        [
            Paragraph("<b>Target Forecast Year:</b>", body_style),
            Paragraph(f"<b>{forecast_year}</b>", body_style),
            Paragraph("<b>ML Model Selected:</b>", body_style),
            Paragraph(model_name, body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[120, 150, 110, 140])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0F4F8')),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 14))

    # Executive Forecast Summary Box
    elements.append(Paragraph("1. Executive Rainfall Forecast & Classification", section_heading))
    pred_mm = pred_data["predicted_rainfall_mm"]
    lpa = pred_data["normal_lpa_mm"]
    anom_pct = pred_data["anomaly_pct"]
    cat = pred_data["classification"]
    ci_low = pred_data["confidence_lower"]
    ci_high = pred_data["confidence_upper"]

    forecast_data = [
        [
            Paragraph("<b>Predicted Annual Rainfall:</b>", body_style),
            Paragraph(f"<font color='#0D2035' size='12'><b>{pred_mm:,.1f} mm</b></font>", body_style),
            Paragraph("<b>90% Confidence Interval:</b>", body_style),
            Paragraph(f"{ci_low:,.1f} – {ci_high:,.1f} mm", body_style)
        ],
        [
            Paragraph("<b>Historical Normal (LPA):</b>", body_style),
            Paragraph(f"{lpa:,.1f} mm", body_style),
            Paragraph("<b>Rainfall Anomaly (%):</b>", body_style),
            Paragraph(f"<b>{'+' if anom_pct >= 0 else ''}{anom_pct:.1f}%</b> ({cat})", body_style)
        ]
    ]
    fc_table = Table(forecast_data, colWidths=[140, 130, 120, 130])
    fc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E6F7FA')),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#16B8D4')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(fc_table)
    elements.append(Spacer(1, 14))

    # Historical Benchmark Statistics
    latest_yr_lbl = pred_data.get('latest_observed_year', 2026)
    elements.append(Paragraph(f"2. Historical Meteorological Benchmarks (1901 – {latest_yr_lbl})", section_heading))
    hist_stats = [
        ["Benchmark Metric", "Value (mm)", "Notes / Significance"],
        ["Historical Mean Rainfall", f"{pred_data['historical_mean']:,.1f} mm", "Long-term historical climate average"],
        ["30-Year Normal (LPA)", f"{pred_data['normal_lpa_mm']:,.1f} mm", "Standard reference baseline (1971–2020)"],
        [f"Latest Observed Annual Rainfall ({latest_yr_lbl})", f"{pred_data['latest_observed_rainfall']:,.1f} mm", "Preceding year ground truth"],
        ["Historical Maximum Recorded", f"{pred_data['historical_max']:,.1f} mm", "Peak monsoon precipitation year"],
        ["Historical Minimum Recorded", f"{pred_data['historical_min']:,.1f} mm", "Historical drought minimum"],
        ["Standard Deviation (Volatility)", f"±{pred_data['historical_std']:,.1f} mm", "Historical inter-annual variance"]
    ]
    hist_table = Table(hist_stats, colWidths=[180, 110, 230])
    hist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0D2035')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFFFFF')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(hist_table)
    elements.append(Spacer(1, 14))

    # Model Evaluation & Verification Box
    elements.append(Paragraph("3. Model Architecture & Validation Rigor", section_heading))
    val_mae = pred_data["validation_mae"]
    val_r2 = pred_data["validation_r2"]
    test_mae = pred_data["test_mae"]

    eval_text = (
        f"This projection was formulated by the <b>{model_name}</b>, optimized with time-series lag features, "
        f"rolling multi-year moving averages, and local geographic coordinates. Validation MAE on independent historical periods "
        f"is <b>{val_mae:.1f} mm</b> (R²: <b>{val_r2:.3f}</b>). On the untouched test period (2016–2024), the model achieved "
        f"an out-of-sample MAE of <b>{test_mae:.1f} mm</b>, demonstrating robust generalization over baseline climatology."
    )
    elements.append(Paragraph(eval_text, body_style))
    elements.append(Spacer(1, 12))

    # AI Climate Scientist Interpretation
    elements.append(Paragraph("4. AI-Generated Meteorological & Agro-Climatic Interpretation", section_heading))
    import re
    # Properly convert markdown bold to ReportLab HTML tags
    clean_ai_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', ai_interpretation)
    # Split paragraphs by bullets or newlines
    for line in clean_ai_text.split("\n"):
        line = line.strip()
        if line:
            if line.startswith("• ") or line.startswith("- "):
                line = "&bull; " + line[2:]
            elements.append(Paragraph(line, body_style))
            elements.append(Spacer(1, 3))
    elements.append(Spacer(1, 10))

    # Scientific Limitations and Disclaimers
    elements.append(Paragraph("5. Scientific Limitations & Official IMD Disclaimer", section_heading))
    limitation_text = (
        "<b>Limitations & Uncertainty:</b> Long-range annual rainfall projections are subject to chaotic climatic drivers "
        "including Pacific El Niño-Southern Oscillation (ENSO), Indian Ocean Dipole (IOD) events, and tropical depressions. "
        "Forecast confidence bands widen recursively for multi-year horizons."
    )
    elements.append(Paragraph(limitation_text, body_style))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(SCIENTIFIC_DISCLAIMER, disclaimer_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=8))
    elements.append(Paragraph("Generated autonomously by RainCast AI Platform • Data Source: IMD Pune / Open-Meteo ERA5", disclaimer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def generate_csv_report(state: str, district: str) -> str:
    """Generates a CSV string containing the complete historical time series for the selected district."""
    df = get_cached_dataset()
    dist_df = df[(df["state"] == state) & (df["district"] == district)].copy()
    if len(dist_df) == 0:
        dist_df = df[df["state"] == state].copy()
    return dist_df.to_csv(index=False)
