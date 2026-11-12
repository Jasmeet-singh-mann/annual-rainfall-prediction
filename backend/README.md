# RainCast AI - Backend Services & Machine Learning Pipeline

This directory houses the complete analytical, modeling, database, and API layer for the RainCast AI platform.

## Architecture

- **`api.py`**: High-performance FastAPI ASGI server rendering Jinja2 HTML5 views and exposing REST APIs.
- **`config.py`**: Central system constants, token management, file paths, and IMD thresholds.
- **`main.py`**: Direct executable runner for backend services (`python main.py`).
- **`data/`**:
  - `raw/Sub_Division_IMD_2017.csv`: 36 official IMD Meteorological Subdivisions (1901–2017).
  - `raw/subdivision_era5_2018_2025.csv`: Authentic ECMWF ERA5 reanalysis (2018–2025).
  - `annual_rainfall.csv`: 125 continuous years of authentic historical records (1901–2025).
  - `processed/india_rainfall_cleaned.csv`: Cleaned, validated, and normalized dataset with 4,476 authentic records.
- **`database/`**:
  - `db.py`: SQLite connection and transaction utilities.
  - `raincast.db`: Local SQLite database storing predictions, chat history, and audit logs.
- **`models/`**:
  - Trained machine learning ensemble artifacts (`*.pkl`).
  - `model_metadata.json`: Cross-validation scores, out-of-sample metrics, and feature importances.
- **`src/`**: Modular analytical services:
  - `data_collection.py`: IMD subdivision and ERA5 station data harmonization.
  - `data_cleaning.py`: Sovereign bounding, climatological median imputation, LPA baseline.
  - `feature_engineering.py`: Time-series lags (T-1..T-3), rolling means, chronological splits.
  - `train_model.py`: Multi-model ensemble training, baseline benchmarks, artifact serialization.
  - `prediction.py`: Multi-horizon recursive forecasting engine (2027–2035) with 90% confidence cone.
  - `model_evaluation.py`: Parity plots, error residual histograms, feature ranking.
  - `genai_assistant.py`: Google Gemini API client & trilingual meteorological reasoning engine.
  - `report_generator.py`: ReportLab executive PDF compiler and CSV exporter.
  - `charts.py`: Backend Plotly figure generator.
- **`tests/`**: Automated unit and end-to-end test suite (`test_*.py`).

## Quickstart (Backend Alone)

```bash
cd backend
pip install -r requirements.txt
python main.py
```
Server runs at `http://localhost:8000`.

