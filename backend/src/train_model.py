"""
RainCast AI - Machine Learning Model Training Engine
Trains Random Forest, Extra Trees, XGBoost, and HistGradientBoosting regressors.
Evaluates against Persistence and Climatological baselines using chronological splits.
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
from typing import Dict, Any, Tuple
from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    HistGradientBoostingRegressor
)
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

from config import (
    PROCESSED_DATA_PATH, MODELS_DIR, FEATURE_COLS, TARGET_COL,
    RANDOM_STATE, SPLIT_TRAIN_END, SPLIT_VAL_END, SPLIT_TEST_START
)
from src.feature_engineering import create_features, get_chronological_splits


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculates MAE, RMSE, R2, and MAPE."""
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(root_mean_squared_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    # MAPE with epsilon to avoid division by zero
    non_zero = y_true > 10.0
    if np.any(non_zero):
        mape = float(np.mean(np.abs((y_true[non_zero] - y_pred[non_zero]) / y_true[non_zero])) * 100.0)
    else:
        mape = 0.0
    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2": round(r2, 4),
        "mape": round(mape, 2)
    }


def train_and_evaluate_all():
    """Trains 4 ML architectures plus 2 baselines on chronological splits."""
    print("=" * 60)
    print("RainCast AI: Starting Machine Learning Training Engine")
    print("=" * 60)
    
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(PROCESSED_DATA_PATH)
    feats = create_features(df)
    train_df, val_df, test_df = get_chronological_splits(feats)

    X_train = train_df[FEATURE_COLS].values
    y_train = train_df[TARGET_COL].values

    X_val = val_df[FEATURE_COLS].values
    y_val = val_df[TARGET_COL].values

    X_test = test_df[FEATURE_COLS].values
    y_test = test_df[TARGET_COL].values

    # Baselines
    # Baseline 1: Climatological Mean (Historical Average)
    train_mean = float(np.mean(y_train))
    y_val_clim = np.full_like(y_val, fill_value=train_mean)
    y_test_clim = np.full_like(y_test, fill_value=train_mean)
    metrics_clim_val = calculate_metrics(y_val, y_val_clim)
    metrics_clim_test = calculate_metrics(y_test, y_test_clim)

    # Baseline 2: Persistence (Lag-1)
    y_val_pers = val_df["rainfall_lag_1"].values
    y_test_pers = test_df["rainfall_lag_1"].values
    metrics_pers_val = calculate_metrics(y_val, y_val_pers)
    metrics_pers_test = calculate_metrics(y_test, y_test_pers)

    print(f"\nBaseline 1 (Climatological Mean): Val MAE={metrics_clim_val['mae']} mm, RMSE={metrics_clim_val['rmse']} mm")
    print(f"Baseline 2 (Persistence / Lag-1): Val MAE={metrics_pers_val['mae']} mm, RMSE={metrics_pers_val['rmse']} mm\n")

    # ML Algorithms definition
    models = {
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=180,
            max_depth=14,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=RANDOM_STATE,
            n_jobs=-1
        ),
        "Extra Trees Regressor": ExtraTreesRegressor(
            n_estimators=180,
            max_depth=16,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=RANDOM_STATE,
            n_jobs=-1
        ),
        "XGBoost Regressor": xgb.XGBRegressor(
            n_estimators=160,
            max_depth=6,
            learning_rate=0.06,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=RANDOM_STATE,
            n_jobs=-1
        ),
        "HistGradientBoosting Regressor": HistGradientBoostingRegressor(
            max_iter=150,
            max_depth=8,
            learning_rate=0.05,
            random_state=RANDOM_STATE
        )
    }

    results = {}
    best_val_mae = float("inf")
    best_model_name = None
    best_model_obj = None

    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)

        # Validation evaluation
        y_val_pred = model.predict(X_val)
        val_metrics = calculate_metrics(y_val, y_val_pred)

        # Test evaluation (on untouched 2016-2024 test period)
        y_test_pred = model.predict(X_test)
        test_metrics = calculate_metrics(y_test, y_test_pred)

        # Calculate improvement over climatological baseline
        mae_imp_pct = round(((metrics_clim_val["mae"] - val_metrics["mae"]) / metrics_clim_val["mae"]) * 100.0, 2)

        # Feature importances where available
        feature_importances = {}
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            feature_importances = {col: round(float(imp), 4) for col, imp in zip(FEATURE_COLS, importances)}

        # Save individual model pickle
        slug = name.lower().replace(" ", "_")
        model_path = MODELS_DIR / f"{slug}.pkl"
        joblib.dump(model, model_path)

        # Residuals on test
        residuals = (y_test - y_test_pred).tolist()
        std_residual = float(np.std(y_test - y_test_pred))

        results[name] = {
            "validation_metrics": val_metrics,
            "test_metrics": test_metrics,
            "improvement_over_climatology_pct": mae_imp_pct,
            "feature_importances": feature_importances,
            "test_residuals_std": round(std_residual, 2),
            "sample_residuals": [round(r, 2) for r in residuals[:30]],
            "file_path": str(model_path.name)
        }

        print(f" -> Val MAE: {val_metrics['mae']} mm | Val R²: {val_metrics['r2']} | Test MAE: {test_metrics['mae']} mm | Test R²: {test_metrics['r2']}")

        if val_metrics["mae"] < best_val_mae:
            best_val_mae = val_metrics["mae"]
            best_model_name = name
            best_model_obj = model

    print(f"\nBest Performing Model selected by Validation MAE: '{best_model_name}' (Val MAE: {best_val_mae} mm)")

    # Save metadata summary
    metadata = {
        "train_period": f"1911 - {SPLIT_TRAIN_END}",
        "train_samples": int(len(train_df)),
        "val_period": f"{SPLIT_TRAIN_END + 1} - {SPLIT_VAL_END}",
        "val_samples": int(len(val_df)),
        "test_period": f"{SPLIT_TEST_START} - {int(test_df['year'].max())}",
        "test_samples": int(len(test_df)),
        "best_model": best_model_name,
        "features": FEATURE_COLS,
        "baselines": {
            "climatological_mean": {
                "validation": metrics_clim_val,
                "test": metrics_clim_test
            },
            "persistence_lag1": {
                "validation": metrics_pers_val,
                "test": metrics_pers_test
            }
        },
        "models": results
    }

    metadata_path = MODELS_DIR / "model_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Model metadata & metrics saved to {metadata_path}")
    print("Training pipeline finished successfully!\n")
    return metadata


if __name__ == "__main__":
    train_and_evaluate_all()

