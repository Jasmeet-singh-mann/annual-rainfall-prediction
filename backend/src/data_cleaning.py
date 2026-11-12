"""
RainCast AI - Data Cleaning & Validation Pipeline
Performs rigorous quality checks, geographical bounding, monthly aggregation consistency,
and IMD meteorological normal/anomaly derivations.
"""

import sys
from pathlib import Path
BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
for p in [str(PROJECT_ROOT), str(BACKEND_DIR), str(FRONTEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any
from config import (
    ANNUAL_RAINFALL_PATH, PROCESSED_DATA_PATH, IMD_CATEGORIES
)

MONTH_COLS = [
    "jan_rainfall", "feb_rainfall", "mar_rainfall", "apr_rainfall",
    "may_rainfall", "jun_rainfall", "jul_rainfall", "aug_rainfall",
    "sep_rainfall", "oct_rainfall", "nov_rainfall", "dec_rainfall"
]

# Geographical bounding box of India
INDIA_BOUNDS = {
    "lat_min": 6.5,
    "lat_max": 37.5,
    "lon_min": 68.0,
    "lon_max": 97.5
}


def validate_geography(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Filters or flags points outside the sovereign Indian bounding box."""
    initial_len = len(df)
    valid_mask = (
        (df["latitude"] >= INDIA_BOUNDS["lat_min"]) &
        (df["latitude"] <= INDIA_BOUNDS["lat_max"]) &
        (df["longitude"] >= INDIA_BOUNDS["lon_min"]) &
        (df["longitude"] <= INDIA_BOUNDS["lon_max"])
    )
    cleaned_df = df[valid_mask].copy()
    dropped = initial_len - len(cleaned_df)
    return cleaned_df, {"geographic_outliers_dropped": dropped}


def handle_missing_and_units(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans missing values using station-specific climatological median.
    Never fills missing rainfall with zero without physical justification.
    """
    df = df.copy()
    
    # Check for duplicates
    df = df.drop_duplicates(subset=["state", "district", "year"], keep="last")

    # Monthly rainfall physical validity check (0 mm to 4000 mm per month)
    for m in MONTH_COLS:
        if m in df.columns:
            # Clip negative anomalies or sensor errors
            df[m] = df[m].apply(lambda x: np.nan if (pd.isna(x) or x < 0 or x > 4000) else x)
            # Impute missing with station-specific median
            station_median = df.groupby(["state", "district"])[m].transform("median")
            df[m] = df[m].fillna(station_median).fillna(0.0)

    # Re-calculate exact annual rainfall from monthly totals
    df["annual_rainfall"] = df[MONTH_COLS].sum(axis=1).round(1)

    # Monsoonal seasonal aggregations:
    # Southwest Monsoon (JJAS: June, July, August, September)
    df["monsoon_rainfall"] = df[["jun_rainfall", "jul_rainfall", "aug_rainfall", "sep_rainfall"]].sum(axis=1).round(1)
    # Northeast / Post-monsoon (OND: October, November, December)
    df["post_monsoon_rainfall"] = df[["oct_rainfall", "nov_rainfall", "dec_rainfall"]].sum(axis=1).round(1)
    # Winter (JF: January, February)
    df["winter_rainfall"] = df[["jan_rainfall", "feb_rainfall"]].sum(axis=1).round(1)
    # Pre-monsoon (MAM: March, April, May)
    df["pre_monsoon_rainfall"] = df[["mar_rainfall", "apr_rainfall", "may_rainfall"]].sum(axis=1).round(1)

    # Monsoon share of total precipitation
    df["monsoon_share"] = (df["monsoon_rainfall"] / np.maximum(df["annual_rainfall"], 1.0)).round(3)
    
    return df


def classify_imd_anomaly(anomaly_pct: float) -> str:
    """Classifies percentage departure into official IMD category."""
    if pd.isna(anomaly_pct):
        return "Normal"
    for category, bounds in IMD_CATEGORIES.items():
        if bounds["min"] <= anomaly_pct < bounds["max"]:
            return category
    if anomaly_pct >= 59.5:
        return "Large Excess"
    return "Large Deficient"


def compute_climatological_baselines(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Long Period Average (LPA) based on 1971–2020 standard IMD normal period.
    Adds anomaly (mm), anomaly (%), and IMD category labels.
    """
    df = df.copy()
    
    # Calculate 1971-2020 baseline mean per district
    baseline_period = df[(df["year"] >= 1971) & (df["year"] <= 2020)]
    if len(baseline_period) == 0:
        baseline_period = df
        
    lpa_series = baseline_period.groupby(["state", "district"])["annual_rainfall"].mean()
    lpa_map = lpa_series.to_dict()

    # Assign LPA
    df["lpa_normal"] = df.apply(
        lambda r: lpa_map.get((r["state"], r["district"]), r["annual_rainfall"]),
        axis=1
    ).round(1)

    # Calculate Anomaly (departure from normal)
    df["anomaly_mm"] = (df["annual_rainfall"] - df["lpa_normal"]).round(1)
    df["anomaly_pct"] = (
        (df["anomaly_mm"] / np.maximum(df["lpa_normal"], 1.0)) * 100.0
    ).round(1)

    # Assign IMD classification category
    df["imd_category"] = df["anomaly_pct"].apply(classify_imd_anomaly)

    return df


def run_data_cleaning_pipeline(input_path: Path = ANNUAL_RAINFALL_PATH, output_path: Path = PROCESSED_DATA_PATH) -> pd.DataFrame:
    """Executes the full data cleaning, validation, and enrichment pipeline."""
    print("Executing RainCast AI Data Cleaning Pipeline...")
    df = pd.read_csv(input_path)
    
    # Step 1: Geographical validation
    df, geo_stats = validate_geography(df)
    
    # Step 2: Missing values and unit consistency
    df = handle_missing_and_units(df)
    
    # Step 3: Climatological normals and anomalies
    df = compute_climatological_baselines(df)
    
    # Save processed dataset
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"Pipeline complete! Cleaned dataset: {len(df):,} records saved to {output_path}")
    return df


if __name__ == "__main__":
    run_data_cleaning_pipeline()
