"""
RainCast AI - Feature Engineering Module
Builds physically consistent meteorological lag features, rolling multi-year averages,
and seasonal ratio lags strictly respecting chronological forecast horizons.
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
from typing import Tuple, List, Dict, Any
from config import (
    PROCESSED_DATA_PATH, FEATURE_COLS, TARGET_COL,
    SPLIT_TRAIN_END, SPLIT_VAL_END, SPLIT_TEST_START
)


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Constructs time-series lag and rolling statistics for each geographical entity.
    Crucially: all features for year T use strictly data from year <= T-1.
    """
    df = df.copy()
    df = df.sort_values(by=["state", "district", "year"]).reset_index(drop=True)

    # Group by district to avoid bleeding data across locations
    grouped = df.groupby(["state", "district"])

    # Lag 1: Previous year rainfall
    df["rainfall_lag_1"] = grouped["annual_rainfall"].shift(1)
    # Lag 2: 2 years prior
    df["rainfall_lag_2"] = grouped["annual_rainfall"].shift(2)
    # Lag 3: 3 years prior
    df["rainfall_lag_3"] = grouped["annual_rainfall"].shift(3)

    # 5-year rolling mean & standard deviation (shifted by 1 so current year is excluded)
    df["rolling_mean_5"] = grouped["annual_rainfall"].transform(
        lambda s: s.shift(1).rolling(window=5, min_periods=3).mean()
    )
    df["rolling_std_5"] = grouped["annual_rainfall"].transform(
        lambda s: s.shift(1).rolling(window=5, min_periods=3).std().fillna(15.0)
    )

    # 10-year rolling mean
    df["rolling_mean_10"] = grouped["annual_rainfall"].transform(
        lambda s: s.shift(1).rolling(window=10, min_periods=5).mean()
    )

    # Anomaly of previous year (departure from local normal)
    df["anomaly_lag_1"] = grouped["anomaly_mm"].shift(1)

    # Monsoon share of previous year
    df["monsoon_share_lag_1"] = grouped["monsoon_share"].shift(1)

    # Drop early years where 10-year rolling window is NaN
    feature_df = df.dropna(subset=FEATURE_COLS + [TARGET_COL]).reset_index(drop=True)

    return feature_df


def get_chronological_splits(feature_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Splits data chronologically to prevent temporal leakage:
    - Train: up to SPLIT_TRAIN_END (e.g. 1911-2005)
    - Validation: SPLIT_TRAIN_END + 1 to SPLIT_VAL_END (e.g. 2006-2015)
    - Test: SPLIT_TEST_START to 2024 (e.g. 2016-2024)
    """
    train_df = feature_df[feature_df["year"] <= SPLIT_TRAIN_END].copy()
    val_df = feature_df[(feature_df["year"] > SPLIT_TRAIN_END) & (feature_df["year"] <= SPLIT_VAL_END)].copy()
    test_df = feature_df[feature_df["year"] >= SPLIT_TEST_START].copy()

    return train_df, val_df, test_df


def prepare_recursive_features(history_series: List[float], anomaly_series: List[float],
                               monsoon_shares: List[float], lat: float, lon: float) -> np.ndarray:
    """
    Constructs feature vector for a future forecast step from recent historical records.
    history_series[-1] is lag 1, history_series[-2] is lag 2, history_series[-3] is lag 3.
    """
    recent_vals = history_series[-10:]
    lag_1 = history_series[-1]
    lag_2 = history_series[-2] if len(history_series) >= 2 else lag_1
    lag_3 = history_series[-3] if len(history_series) >= 3 else lag_2

    rolling_5 = float(np.mean(recent_vals[-5:]))
    rolling_10 = float(np.mean(recent_vals))
    rolling_std_5 = float(np.std(recent_vals[-5:])) if len(recent_vals) >= 5 else 20.0
    anomaly_lag1 = anomaly_series[-1] if anomaly_series else 0.0
    monsoon_lag1 = monsoon_shares[-1] if monsoon_shares else 0.75

    features = [
        lag_1,
        lag_2,
        lag_3,
        rolling_5,
        rolling_10,
        rolling_std_5,
        anomaly_lag1,
        lat,
        lon,
        monsoon_lag1
    ]
    return np.array(features, dtype=np.float32).reshape(1, -1)


if __name__ == "__main__":
    raw_df = pd.read_csv(PROCESSED_DATA_PATH)
    feats = create_features(raw_df)
    train, val, test = get_chronological_splits(feats)
    print(f"Features created successfully: {len(feats)} rows.")
    print(f"Train set: {len(train)} rows (<= {SPLIT_TRAIN_END})")
    print(f"Validation set: {len(val)} rows ({SPLIT_TRAIN_END+1} to {SPLIT_VAL_END})")
    print(f"Test set: {len(test)} rows ({SPLIT_TEST_START} to 2024)")

