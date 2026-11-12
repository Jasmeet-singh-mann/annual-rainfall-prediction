"""
RainCast AI - Model Evaluation & Residual Diagnostics
Analyzes model performance across validation and test sets, computes residual distributions,
and extracts feature importance rankings.
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
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from config import MODELS_DIR, FEATURE_COLS
from src.prediction import load_model_metadata, get_model, get_cached_dataset
from src.feature_engineering import create_features, get_chronological_splits


def get_model_comparison_dataframe() -> pd.DataFrame:
    """Returns a structured comparison table of all trained models and baselines."""
    metadata = load_model_metadata()
    if not metadata:
        return pd.DataFrame()

    records = []

    # Baselines
    baselines = metadata.get("baselines", {})
    clim = baselines.get("climatological_mean", {})
    records.append({
        "Model": "Historical Climatological Mean (Baseline)",
        "Type": "Baseline",
        "Val MAE (mm)": clim.get("validation", {}).get("mae", np.nan),
        "Val RMSE (mm)": clim.get("validation", {}).get("rmse", np.nan),
        "Val R²": clim.get("validation", {}).get("r2", np.nan),
        "Test MAE (mm)": clim.get("test", {}).get("mae", np.nan),
        "Test RMSE (mm)": clim.get("test", {}).get("rmse", np.nan),
        "Test R²": clim.get("test", {}).get("r2", np.nan),
        "Improvement vs Mean (%)": 0.0,
        "Selected": False
    })

    pers = baselines.get("persistence_lag1", {})
    records.append({
        "Model": "Persistence / Lag-1 (Baseline)",
        "Type": "Baseline",
        "Val MAE (mm)": pers.get("validation", {}).get("mae", np.nan),
        "Val RMSE (mm)": pers.get("validation", {}).get("rmse", np.nan),
        "Val R²": pers.get("validation", {}).get("r2", np.nan),
        "Test MAE (mm)": pers.get("test", {}).get("mae", np.nan),
        "Test RMSE (mm)": pers.get("test", {}).get("rmse", np.nan),
        "Test R²": pers.get("test", {}).get("r2", np.nan),
        "Improvement vs Mean (%)": round(((clim.get("validation", {}).get("mae", 1) - pers.get("validation", {}).get("mae", 1)) / clim.get("validation", {}).get("mae", 1)) * 100, 1),
        "Selected": False
    })

    # Machine Learning Models
    models_dict = metadata.get("models", {})
    best_model_name = metadata.get("best_model", "")

    for name, data in models_dict.items():
        v = data.get("validation_metrics", {})
        t = data.get("test_metrics", {})
        records.append({
            "Model": name,
            "Type": "Machine Learning",
            "Val MAE (mm)": v.get("mae", np.nan),
            "Val RMSE (mm)": v.get("rmse", np.nan),
            "Val R²": v.get("r2", np.nan),
            "Test MAE (mm)": t.get("mae", np.nan),
            "Test RMSE (mm)": t.get("rmse", np.nan),
            "Test R²": t.get("r2", np.nan),
            "Improvement vs Mean (%)": data.get("improvement_over_climatology_pct", np.nan),
            "Selected": (name == best_model_name)
        })

    df = pd.DataFrame(records)
    return df


def get_test_predictions_and_residuals(model_name: str = "Random Forest Regressor") -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Evaluates a specific model on the untouched test period (2016-2024),
    returning a DataFrame with columns [actual, predicted, residual, state, district, year].
    """
    df = get_cached_dataset()
    feats = create_features(df)
    _, _, test_df = get_chronological_splits(feats)

    model = get_model(model_name)
    X_test = test_df[FEATURE_COLS].values
    y_test = test_df["annual_rainfall"].values

    preds = model.predict(X_test)
    residuals = y_test - preds

    results_df = test_df[["state", "district", "year"]].copy()
    results_df["actual"] = y_test.round(1)
    results_df["predicted"] = preds.round(1)
    results_df["residual"] = residuals.round(1)
    results_df["abs_error"] = np.abs(residuals).round(1)

    summary = {
        "mean_residual": round(float(np.mean(residuals)), 2),
        "std_residual": round(float(np.std(residuals)), 2),
        "max_overprediction": round(float(np.max(-residuals)), 2),
        "max_underprediction": round(float(np.max(residuals)), 2),
    }

    return results_df, summary


def get_feature_importances(model_name: str = "Random Forest Regressor") -> pd.DataFrame:
    """Returns sorted feature importance table for tree-based models."""
    metadata = load_model_metadata()
    model_data = metadata.get("models", {}).get(model_name, {})
    imp_dict = model_data.get("feature_importances", {})

    if not imp_dict:
        model = get_model(model_name)
        if hasattr(model, "feature_importances_"):
            imp_dict = {col: round(float(imp), 4) for col, imp in zip(FEATURE_COLS, model.feature_importances_)}

    if not imp_dict:
        return pd.DataFrame()

    df = pd.DataFrame([
        {"Feature": k, "Importance": v} for k, v in imp_dict.items()
    ]).sort_values(by="Importance", ascending=True)

    # Feature descriptions
    descriptions = {
        "rainfall_lag_1": "Rainfall (Year T-1)",
        "rainfall_lag_2": "Rainfall (Year T-2)",
        "rainfall_lag_3": "Rainfall (Year T-3)",
        "rolling_mean_5": "5-Year Rolling Average",
        "rolling_mean_10": "10-Year Rolling Average",
        "rolling_std_5": "5-Year Volatility (Std Dev)",
        "anomaly_lag_1": "Preceding Year Climate Anomaly",
        "latitude": "Latitude (N-S Geography)",
        "longitude": "Longitude (E-W Geography)",
        "monsoon_share_lag_1": "Historical Monsoon Share"
    }
    df["Description"] = df["Feature"].map(descriptions).fillna(df["Feature"])
    return df


if __name__ == "__main__":
    comp = get_model_comparison_dataframe()
    print("Model Comparison Matrix:\n", comp.to_string())

