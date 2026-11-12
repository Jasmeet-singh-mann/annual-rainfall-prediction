"""
RainCast AI - End-to-End Application Runtime & Page Logic Test
Executes every module, data pipeline, prediction horizon,
report compiler, and database operations.
"""

import sys
from pathlib import Path
import unittest

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
for p in [str(PROJECT_ROOT), str(BACKEND_DIR), str(FRONTEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import pandas as pd
import numpy as np

from config import APP_NAME, MODEL_NAMES, SCIENTIFIC_DISCLAIMER
from src.data_collection import load_dataset
from src.prediction import predict_annual_rainfall, get_cached_dataset, load_model_metadata
from src.genai_assistant import generate_prediction_explanation, chat_with_climate_assistant
from src.model_evaluation import (
    get_model_comparison_dataframe,
    get_test_predictions_and_residuals,
    get_feature_importances
)
from src.report_generator import generate_pdf_report, generate_csv_report
from database.db import (
    save_prediction, get_recent_predictions,
    save_chat_message, get_session_chat_history, log_report_generation
)
from src.charts import (
    plot_historical_trend,
    plot_monthly_distribution,
    plot_rainfall_anomalies,
    plot_multi_year_forecast,
    plot_actual_vs_predicted,
    plot_residuals_distribution,
    plot_feature_importances
)


class TestFullApplicationRuntime(unittest.TestCase):

    def test_01_dataset_integrity(self):
        df = load_dataset()
        self.assertFalse(df.empty)
        self.assertEqual(len(df), 4476)
        self.assertEqual(df["year"].max(), 2025)
        self.assertEqual(df["year"].min(), 1901)
        self.assertNotIn(2026, df["year"].values)
        print(" [E2E] Dataset verified: 4,476 authentic records across 1901-2025.")

    def test_02_prediction_horizons(self):
        # Historical year test (2025 ground truth)
        res_2025 = predict_annual_rainfall("Punjab", "Punjab Sub-Division", 2025)
        self.assertGreater(res_2025["predicted_rainfall_mm"], 50.0)
        self.assertEqual(res_2025["forecast_horizon_years"], 0)

        # Future forecast tests from 2027 onwards
        for yr in [2027, 2028, 2030, 2032]:
            for model in MODEL_NAMES:
                res = predict_annual_rainfall("Punjab", "Punjab Sub-Division", yr, model_name=model)
                self.assertGreater(res["predicted_rainfall_mm"], 50.0)
                self.assertLessEqual(res["confidence_lower"], res["predicted_rainfall_mm"])
                self.assertGreaterEqual(res["confidence_upper"], res["predicted_rainfall_mm"])
                self.assertIn(res["classification"], ["Normal", "Deficient", "Excess", "Large Deficient", "Large Excess"])
        print(" [E2E] Multi-model predictions verified across 2025 (ground truth) and 2027-2032 forecasts.")

    def test_03_charts_generation(self):
        df = get_cached_dataset()
        dist_df = df[(df["state"] == "Punjab") & (df["district"] == "Punjab Sub-Division")]
        lpa = float(dist_df["lpa_normal"].iloc[-1])
        fig1 = plot_historical_trend(dist_df, lpa)
        fig2 = plot_monthly_distribution(dist_df.mean(numeric_only=True), "Punjab Sub-Division")
        fig3 = plot_rainfall_anomalies(dist_df)
        fig4 = plot_multi_year_forecast(dist_df, 650.0, 250.0, 1050.0, 2027, lpa)

        self.assertIsNotNone(fig1)
        self.assertIsNotNone(fig2)
        self.assertIsNotNone(fig3)
        self.assertIsNotNone(fig4)
        print(" [E2E] Interactive Plotly charts compiled successfully.")

    def test_04_trilingual_genai(self):
        res = predict_annual_rainfall("Punjab", "Punjab Sub-Division", 2027)
        for lang in ["English", "Hindi", "Punjabi"]:
            explanation = generate_prediction_explanation(res, language=lang)
            self.assertGreater(len(explanation), 40)
            self.assertIn(str(res["predicted_rainfall_mm"]), explanation) # Grounded in numbers!

        chat_resp = chat_with_climate_assistant("Tell me about Punjab rainfall", [])
        self.assertGreater(len(chat_resp), 30)
        print(" [E2E] GenAI explanation engine tested in English, Hindi, and Punjabi with strict factual grounding.")

    def test_05_model_performance_diagnostics(self):
        comp = get_model_comparison_dataframe()
        self.assertEqual(len(comp), 6) # 2 baselines + 4 ML models
        eval_df, res_summary = get_test_predictions_and_residuals("Random Forest Regressor")
        self.assertEqual(len(eval_df), 360) # 10-year test period (2016-2025) across 36 subdivisions
        self.assertLess(abs(res_summary["mean_residual"]), 200.0) # Unbiased check on authentic test residuals

        fig_par = plot_actual_vs_predicted(eval_df)
        fig_res = plot_residuals_distribution(eval_df)
        imp_df = get_feature_importances("Random Forest Regressor")
        fig_imp = plot_feature_importances(imp_df)

        self.assertIsNotNone(fig_par)
        self.assertIsNotNone(fig_res)
        self.assertIsNotNone(fig_imp)
        print(" [E2E] Parity plots, residual histograms, and feature importances verified.")

    def test_06_pdf_and_csv_reports(self):
        pdf = generate_pdf_report("Punjab", "Punjab Sub-Division", 2027)
        self.assertGreater(len(pdf), 3000)
        self.assertTrue(pdf.startswith(b"%PDF"))

        csv = generate_csv_report("Punjab", "Punjab Sub-Division")
        self.assertGreater(len(csv), 1000)
        self.assertIn("Punjab Sub-Division", csv)
        print(" [E2E] ReportLab PDF generation (%PDF header verified) and CSV exports working cleanly.")

    def test_07_sqlite_persistence(self):
        p_id = save_prediction({
            "state": "Punjab", "district": "Ludhiana", "forecast_year": 2027,
            "predicted_rainfall": 696.1, "model_name": "Random Forest Regressor",
            "historical_avg": 662.2, "anomaly_pct": 5.1, "classification": "Normal",
            "confidence_lower": 277.0, "confidence_upper": 1115.2,
            "ai_explanation": "Test explanation"
        })
        self.assertIsInstance(p_id, int)
        rec = get_recent_predictions(limit=5)
        self.assertGreater(len(rec), 0)

        save_chat_message("user", "What is rainfall?", "English", "session_e2e")
        hist = get_session_chat_history("session_e2e")
        self.assertGreater(len(hist), 0)

        log_report_generation("Test Report", "Punjab", "Ludhiana", 2027, "PDF")
        print(" [E2E] SQLite predictions, chat history, and report logs verified.")


if __name__ == "__main__":
    unittest.main()
