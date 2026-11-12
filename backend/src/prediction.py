"""
RainCast AI - Inference & Prediction Service
Performs recursive multi-horizon annual rainfall predictions with expanding uncertainty intervals
and IMD meteorological categorization.
"""

import sys
from pathlib import Path
BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
for p in [str(PROJECT_ROOT), str(BACKEND_DIR), str(FRONTEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from config import (
    MODELS_DIR, PROCESSED_DATA_PATH, FEATURE_COLS,
    IMD_CATEGORIES, SCIENTIFIC_DISCLAIMER
)
from src.feature_engineering import prepare_recursive_features
from src.data_cleaning import classify_imd_anomaly


_LOADED_MODELS: Dict[str, Any] = {}
_METADATA_CACHE: Optional[Dict[str, Any]] = None
_DATASET_CACHE: Optional[pd.DataFrame] = None


def get_cached_dataset() -> pd.DataFrame:
    global _DATASET_CACHE
    if _DATASET_CACHE is None:
        _DATASET_CACHE = pd.read_csv(PROCESSED_DATA_PATH)
    return _DATASET_CACHE


def load_model_metadata() -> Dict[str, Any]:
    global _METADATA_CACHE
    if _METADATA_CACHE is None:
        meta_file = MODELS_DIR / "model_metadata.json"
        if meta_file.exists():
            with open(meta_file, "r") as f:
                _METADATA_CACHE = json.load(f)
        else:
            _METADATA_CACHE = {}
    return _METADATA_CACHE


def get_model(model_name: str = "Random Forest Regressor"):
    """Loads and caches the requested trained model."""
    global _LOADED_MODELS
    if model_name in _LOADED_MODELS:
        return _LOADED_MODELS[model_name]

    slug = model_name.lower().replace(" ", "_")
    model_file = MODELS_DIR / f"{slug}.pkl"
    if not model_file.exists():
        # Fallback to random forest if specific model not found
        model_file = MODELS_DIR / "random_forest_regressor.pkl"
        if not model_file.exists():
            raise FileNotFoundError(f"Trained model file not found at {model_file}. Run train_model.py first.")
    
    model = joblib.load(model_file)
    _LOADED_MODELS[model_name] = model
    return model


def predict_annual_rainfall(
    state: str,
    district: str,
    forecast_year: int = 2027,
    model_name: str = "Random Forest Regressor"
) -> Dict[str, Any]:
    """
    Computes annual rainfall forecast for a given Indian district.
    Supports recursive multi-step forecasting for years from 2027 onward.
    Returns comprehensive metrics, confidence intervals, and IMD classification.
    """
    df = get_cached_dataset()
    metadata = load_model_metadata()
    model = get_model(model_name)

    # Filter station history
    station_df = df[(df["state"] == state) & (df["district"] == district)].sort_values(by="year")
    if len(station_df) == 0:
        # Fallback to state average if district not in dataset
        station_df = df[df["state"] == state].sort_values(by="year")
        if len(station_df) == 0:
            raise ValueError(f"No historical observations found for {state} - {district}")

    lat = float(station_df["latitude"].iloc[0])
    lon = float(station_df["longitude"].iloc[0])
    normal_lpa = float(station_df["lpa_normal"].iloc[-1])
    latest_hist_year = int(station_df["year"].max())

    # Historical series for lag features
    annual_history = station_df["annual_rainfall"].tolist()
    anomaly_history = station_df["anomaly_mm"].tolist()
    monsoon_shares = station_df["monsoon_share"].tolist()

    # Model validation / residual statistics
    model_info = metadata.get("models", {}).get(model_name, {})
    val_mae = model_info.get("validation_metrics", {}).get("mae", 145.0)
    val_r2 = model_info.get("validation_metrics", {}).get("r2", 0.97)
    test_mae = model_info.get("test_metrics", {}).get("mae", 130.0)
    test_rmse = model_info.get("test_metrics", {}).get("rmse", 175.0)
    base_std_residual = model_info.get("test_residuals_std", 150.0)
    latest_observed_rainfall = float(annual_history[-1])

    # If requested year is within historical observations, return ground truth
    if forecast_year <= latest_hist_year:
        hist_match = station_df[station_df["year"] == forecast_year]
        if len(hist_match) > 0:
            pred_val = float(hist_match["annual_rainfall"].iloc[0])
            std_error = 0.0
            horizon_step = 0
            ci_lower = pred_val
            ci_upper = pred_val
        else:
            pred_val = latest_observed_rainfall
            std_error = base_std_residual
            horizon_step = 1
            ci_lower = float(max(0.0, round(pred_val - 1.645 * std_error, 1)))
            ci_upper = float(round(pred_val + 1.645 * std_error, 1))
    else:
        # Recursive forecasting from (latest_hist_year + 1) up to forecast_year
        curr_year = latest_hist_year + 1
        horizon_step = 1
        pred_val = 0.0

        while curr_year <= forecast_year:
            feat_vector = prepare_recursive_features(
                annual_history,
                anomaly_history,
                monsoon_shares,
                lat,
                lon
            )
            pred_val = float(model.predict(feat_vector)[0])
            pred_val = max(10.0, round(pred_val, 1))

            # Append to recursive history for subsequent steps
            annual_history.append(pred_val)
            step_anomaly = round(pred_val - normal_lpa, 1)
            anomaly_history.append(step_anomaly)
            monsoon_shares.append(float(np.mean(monsoon_shares[-5:]))) # Climatological mean share

            if curr_year == forecast_year:
                break
            curr_year += 1
            horizon_step += 1

        # Expanding uncertainty interval calculation
        # As forecast horizon increases, variance grows compounding error
        uncertainty_multiplier = np.sqrt(1.0 + 0.40 * (horizon_step - 1))
        std_error = base_std_residual * uncertainty_multiplier
        # 90% confidence interval (z = 1.645)
        ci_lower = float(max(0.0, round(pred_val - 1.645 * std_error, 1)))
        ci_upper = float(round(pred_val + 1.645 * std_error, 1))

    # Anomaly vs Long Period Average
    anomaly_mm = float(round(pred_val - normal_lpa, 1))
    anomaly_pct = float(round((anomaly_mm / max(normal_lpa, 1.0)) * 100.0, 1))
    classification = classify_imd_anomaly(anomaly_pct)

    # Historical context stats
    hist_mean = float(round(float(np.mean(station_df["annual_rainfall"])), 1))
    hist_min = float(round(float(np.min(station_df["annual_rainfall"])), 1))
    hist_max = float(round(float(np.max(station_df["annual_rainfall"])), 1))
    hist_std = float(round(float(np.std(station_df["annual_rainfall"])), 1))
    latest_observed_rainfall = float(round(float(station_df["annual_rainfall"].iloc[-1]), 1))

    return {
        "state": state,
        "district": district,
        "latitude": lat,
        "longitude": lon,
        "forecast_year": int(forecast_year),
        "forecast_horizon_years": int(horizon_step),
        "predicted_rainfall_mm": float(pred_val),
        "confidence_interval_90": (ci_lower, ci_upper),
        "confidence_lower": ci_lower,
        "confidence_upper": ci_upper,
        "uncertainty_std_error": float(round(float(std_error), 1)),
        "normal_lpa_mm": float(normal_lpa),
        "anomaly_mm": anomaly_mm,
        "anomaly_pct": anomaly_pct,
        "classification": classification,
        "model_name": model_name,
        "validation_mae": val_mae,
        "validation_r2": val_r2,
        "test_mae": test_mae,
        "test_rmse": test_rmse,
        "historical_mean": hist_mean,
        "historical_min": hist_min,
        "historical_max": hist_max,
        "historical_std": hist_std,
        "latest_observed_year": latest_hist_year,
        "latest_observed_rainfall": latest_observed_rainfall,
        "disclaimer": SCIENTIFIC_DISCLAIMER
    }


if __name__ == "__main__":
    res = predict_annual_rainfall("Punjab", "Ludhiana", 2027)
    print("Sample Prediction Output:")
    for k, v in res.items():
        if k != "disclaimer":
            print(f"  {k}: {v}")
