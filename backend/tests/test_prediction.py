"""
RainCast AI - Unit Tests for Machine Learning Predictions & Uncertainty Propagation
"""

import sys
from pathlib import Path
BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
for p in [str(PROJECT_ROOT), str(BACKEND_DIR), str(FRONTEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import unittest
import numpy as np
from config import MODELS_DIR, MODEL_NAMES, IMD_CATEGORIES
from src.prediction import predict_annual_rainfall, load_model_metadata


class TestPredictionEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.metadata = load_model_metadata()

    def test_model_files_exist(self):
        for name in MODEL_NAMES:
            slug = name.lower().replace(" ", "_")
            model_file = MODELS_DIR / f"{slug}.pkl"
            self.assertTrue(model_file.exists(), f"Model file missing: {model_file}")

    def test_single_year_prediction(self):
        res = predict_annual_rainfall("Punjab", "Ludhiana", 2027, model_name="Random Forest Regressor")
        self.assertIn("predicted_rainfall_mm", res)
        self.assertGreater(res["predicted_rainfall_mm"], 50.0)
        self.assertLess(res["predicted_rainfall_mm"], 4000.0)

        # Confidence Interval Check
        ci_lower = res["confidence_lower"]
        ci_upper = res["confidence_upper"]
        pred = res["predicted_rainfall_mm"]
        self.assertLessEqual(ci_lower, pred, "CI Lower bound must be <= predicted value")
        self.assertGreaterEqual(ci_upper, pred, "CI Upper bound must be >= predicted value")

    def test_imd_classification_validity(self):
        res = predict_annual_rainfall("Maharashtra", "Pune", 2027)
        cat = res["classification"]
        self.assertIn(cat, IMD_CATEGORIES.keys(), f"Invalid IMD category: {cat}")

    def test_expanding_uncertainty_with_horizon(self):
        res_step1 = predict_annual_rainfall("Kerala", "Wayanad", 2027)
        res_step3 = predict_annual_rainfall("Kerala", "Wayanad", 2029)

        std_1 = res_step1["uncertainty_std_error"]
        std_3 = res_step3["uncertainty_std_error"]

        self.assertGreater(
            std_3, std_1,
            f"Uncertainty must expand for longer forecast horizons (Step 1: {std_1}, Step 3: {std_3})"
        )


if __name__ == "__main__":
    unittest.main()

