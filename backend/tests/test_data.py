"""
RainCast AI - Unit Tests for Data Integrity & Meteorological Validation
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
import pandas as pd
import numpy as np
from config import PROCESSED_DATA_PATH, ANNUAL_RAINFALL_PATH
from src.data_cleaning import MONTH_COLS, INDIA_BOUNDS


class TestDataIntegrity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(PROCESSED_DATA_PATH)

    def test_dataset_exists_and_size(self):
        self.assertTrue(PROCESSED_DATA_PATH.exists(), "Processed dataset file does not exist.")
        self.assertEqual(len(self.df), 4476, f"Expected exactly 4,476 authentic records, got {len(self.df)}")
        self.assertEqual(int(self.df["year"].max()), 2025, f"Historical observations must end at 2025, found max {self.df['year'].max()}")
        self.assertEqual(int(self.df["year"].min()), 1901, f"Historical observations must start at 1901, found min {self.df['year'].min()}")
        self.assertNotIn(2026, self.df["year"].values, "2026 must be strictly excluded from historical observations.")

    def test_required_columns_present(self):
        required_cols = [
            "location", "SUBDIVISION", "state", "district", "latitude", "longitude",
            "year", "annual_rainfall", "monsoon_rainfall", "lpa_normal",
            "anomaly_mm", "anomaly_pct", "imd_category", "data_source"
        ] + MONTH_COLS
        for col in required_cols:
            self.assertIn(col, self.df.columns, f"Missing required column: {col}")

    def test_geographic_boundaries(self):
        min_lat = self.df["latitude"].min()
        max_lat = self.df["latitude"].max()
        min_lon = self.df["longitude"].min()
        max_lon = self.df["longitude"].max()

        self.assertGreaterEqual(min_lat, INDIA_BOUNDS["lat_min"], "Latitude below Indian bounds")
        self.assertLessEqual(max_lat, INDIA_BOUNDS["lat_max"], "Latitude above Indian bounds")
        self.assertGreaterEqual(min_lon, INDIA_BOUNDS["lon_min"], "Longitude below Indian bounds")
        self.assertLessEqual(max_lon, INDIA_BOUNDS["lon_max"], "Longitude above Indian bounds")

    def test_monthly_sum_equals_annual(self):
        calculated_annual = self.df[MONTH_COLS].sum(axis=1).round(1)
        actual_annual = self.df["annual_rainfall"].round(1)
        discrepancies = np.abs(calculated_annual - actual_annual)
        max_diff = discrepancies.max()
        self.assertLessEqual(max_diff, 0.5, f"Annual rainfall does not match monthly sum, max diff={max_diff}")

    def test_no_missing_values_in_core_fields(self):
        critical_cols = ["state", "district", "year", "annual_rainfall", "lpa_normal", "anomaly_pct"]
        for col in critical_cols:
            null_count = self.df[col].isna().sum()
            self.assertEqual(null_count, 0, f"Found {null_count} nulls in {col}")


if __name__ == "__main__":
    unittest.main()

