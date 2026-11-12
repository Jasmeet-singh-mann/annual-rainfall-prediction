# RainCast AI: Intelligent Annual Rainfall Prediction & Climate Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC.svg)](https://tailwindcss.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4%2B-orange.svg)](https://scikit-learn.org/)
[![Google GenAI](https://img.shields.io/badge/Google%20GenAI-Gemini%202.5-4285F4.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **TAGLINE:** *Predict Rainfall. Understand Climate. Prepare for Tomorrow.*  
> **DEVELOPED BY:** **Jasmeet Singh Mann** (RainCast AI Climate Intelligence Laboratory)

---

## 1. Executive Summary

**RainCast AI** is an enterprise-grade, research-backed annual rainfall prediction and climate intelligence web platform tailored for the Indian subcontinent. India's agrarian economy, hydroelectric power generation, reservoir storage, and urban water security depend deeply on the Southwest Monsoon (June–September) and regional precipitation cycles.

RainCast AI integrates **125 continuous years of verified meteorological observations (1901–2025)** covering **all 36 official IMD Meteorological Subdivisions** totaling **4,476 comprehensive authentic records with zero synthetic data and complete provenance metadata**:
- **1901–2017:** India Meteorological Department (IMD) Official Gridded Subdivision Archive (4,188 records)
- **2018–2025:** ECMWF ERA5 Atmospheric Reanalysis via Open-Meteo Historical Archive (288 records)

> **Important Boundary Rule (2026 Calendar Year):** Since today is November 12, 2026, complete calendar-year rainfall totals for 2026 are not yet available. Following strict scientific integrity standards, 2026 is strictly excluded from historical observations. Multi-horizon predictive forecasts commence strictly from **2027 onward** (up to 2035).

The system leverages ensemble machine learning regressors, automated executive PDF reporting, and a context-grounded **Trilingual Generative AI Climate Assistant** (English, Hindi, Punjabi).

---

## 2. Key Web Pages & System Modules

The frontend is built with high-performance **FastAPI + Jinja2 + HTML5 / Tailwind CSS**, Lucide Icons, interactive Plotly.js charts, and a **Trilingual Language Switcher** supporting real-time detailed translations across **English**, **हिंदी (Hindi)**, and **ਪੰਜਾਬੀ (Punjabi)**:

| Page / Route | Template | Core Capabilities |
| :--- | :--- | :--- |
| **Home / Landing** (`/`) | `frontend/templates/index.html` | Hero overview, real-time KPI counters (125 Years, 36 Subdivisions, 78.0% Test $R^2$), methodology workflow pipeline, interactive module cards, system status badges. |
| **Climate Dashboard** (`/dashboard`) | `frontend/templates/dashboard.html` | Dynamic state & district selectors, 125-year historical timeline with 5-year rolling averages, 12-month climatological normal profiles, decadal anomaly tracker. |
| **Rainfall Prediction** (`/predict`) | `frontend/templates/predict.html` | Multi-horizon forecasts (2027–2035), multi-model selector, IMD anomaly speedometer gauge, expanding 90% confidence bands, agricultural suitability analysis (Kharif/Rabi), GenAI climate interpretation. |
| **AI Climate Assistant** (`/assistant`) | `frontend/templates/assistant.html` | Multilingual conversational assistant (English, Hindi, Punjabi) grounded strictly in meteorological records, with quick-prompt chips and real-time response rendering. |
| **Model Performance** (`/models`) | `frontend/templates/models.html` | Benchmark matrix comparing 4 ML ensembles vs baseline climatology, actual vs predicted parity scatter plot ($y=x$), error residual histogram, feature importance ranking. |
| **Executive Reports** (`/reports`) | `frontend/templates/reports.html` | One-click publication-grade PDF report download (ReportLab), full 125-year CSV dataset export, and live SQLite audit activity log. |

---

## 3. Technology Architecture

```
                                  RainCast AI Architecture
                                  
      [ Official IMD Meteorological Archive ]      [ ECMWF ERA5 Atmospheric Reanalysis ]
          (36 Subdivisions: 1901–2017)                  (36 Subdivisions: 2018–2025)
                       │                                             │
                       └──────────────────────┬──────────────────────┘
                                              │
                                              ▼
            ┌─────────────────────────────────────────────────────────────┐
            │          Data Cleaning & Geographical Harmonization         │
            │   - Sovereign Bounding [6.5°-37.5°N, 68.0°-97.5°E]          │
            │   - Climatological Median Imputation (<0.2% raw missing)    │
            │   - 30-Year Long Period Average (LPA Normal: 1971-2020)     │
            │   - 36 Subdivisions × 125 Years = 4,476 Authentic Records   │
            │   - Explicit `data_source` Provenance on Every Record       │
            └──────────────────────────────┬──────────────────────────────┘
                                           │
                                           ▼
            ┌─────────────────────────────────────────────────────────────┐
            │                 Feature Engineering Engine                  │
            │   - Lags: T-1, T-2, T-3                                     │
            │   - Rolling: 5-Yr Mean, 10-Yr Mean, 5-Yr Volatility         │
            │   - Seasonal: Monsoonal Share, Preceding Anomaly            │
            │   - Strict Chronological Partitioning (No temporal leakage) │
            └──────────────────────────────┬──────────────────────────────┘
                                           │
                          ┌────────────────┴────────────────┐
                          ▼                                 ▼
            ┌────────────────────────────┐   ┌────────────────────────────┐
            │   ML Regression Ensembles  │   │  Generative AI Assistant   │
            │ - HistGradientBoosting     │   │ - Google Gemini API        │
            │ - Random Forest Regressor  │   │ - Grounded Meta Context    │
            │ - Extra Trees Regressor    │   │ - Multilingual Engine      │
            │ - XGBoost Regressor        │   │   (English, Hindi, Punjabi)│
            │ - Expanding Uncertainty CI │   │ - Local Scientific Fallback│
            └─────────────┬──────────────┘   └──────────────┬─────────────┘
                          │                                 │
                          └────────────────┬────────────────┘
                                           │
                                           ▼
            ┌─────────────────────────────────────────────────────────────┐
            │            FastAPI Modern Presentation Layer                │
            │   - Pure Python ASGI Backend (FastAPI + Uvicorn)            │
            │   - Server-Rendered HTML5 + Tailwind CSS + Lucide Icons     │
            │   - Interactive Dark-Navy Plotly.js Visualizations          │
            │   - ReportLab PDF Compiler & SQLite Persistence             │
            │   - Comprehensive REST API Endpoints                        │
            └─────────────────────────────────────────────────────────────┘
```

---

## 4. Machine Learning Benchmark Results

All models were evaluated using strict **chronological data partitioning** on 100% authentic observations to guarantee zero future data leakage:
- **In-Sample Training Period:** 1911 – 2005 (3,576 authentic observations)
- **Validation Tuning Period:** 2006 – 2015 (360 authentic observations)
- **Out-of-Sample Test Period:** 2016 – 2025 (360 authentic observations, untouched)

| Architecture | Model Type | Val MAE (mm) | Val R² | Test MAE (mm) | Test R² | Improvement vs Climatology |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Historical Climatological Mean** | Baseline Reference | 687.80 | -0.0051 | 737.40 | -0.0256 | Baseline Reference |
| **Persistence (Lag-1)** | Baseline Naïve | 283.54 | 0.8144 | 325.66 | 0.7973 | +58.78% |
| **HistGradientBoosting (Selected Best)** | Gradient Boosting | **217.11** | **0.8854** | **315.98** | **0.7762** | **+68.43%** |
| **Random Forest Regressor** | Bagging Ensemble | 218.10 | 0.8840 | 309.50 | 0.7802 | +68.29% |
| **Extra Trees Regressor** | Extremely Randomized | 220.24 | 0.8826 | 306.48 | 0.7824 | +67.98% |
| **XGBoost Regressor** | Gradient Boosting | 223.19 | 0.8827 | 318.18 | 0.7602 | +67.55% |

### Multi-Horizon Uncertainty Estimation
For multi-year recursive forecasts ($h \ge 1$), uncertainty compounds with the horizon step:
$$\sigma_h = \sigma_{\text{test}} \times \sqrt{1 + 0.40 \times (h - 1)}$$

The 90% statistical confidence interval (z = 1.645) is calculated as:
$$\text{CI}_{90\%} = \left[ \max(0, \hat{y} - 1.645 \cdot \sigma_h), \; \hat{y} + 1.645 \cdot \sigma_h \right]$$

---

## 5. IMD Rainfall Categorization Standards

Precipitation anomalies are quantified as percentage departures from the 30-year Long Period Average (LPA):
$$\text{Anomaly (\%)} = \frac{\text{Precipitation} - \text{LPA}}{\text{LPA}} \times 100$$

- **Large Excess:** $\ge +60\%$
- **Excess:** $+20\%$ to $+59\%$
- **Normal:** $-19\%$ to $+19\%$
- **Deficient:** $-20\%$ to $-59\%$
- **Large Deficient:** $< -59\%$

---

## 6. Project Directory Layout

```
ARP/
├── backend/
│   ├── api.py                  # Primary FastAPI ASGI web application & REST routes
│   ├── config.py               # Central configuration, IMD parameters & file paths
│   ├── main.py                 # Backend service runner (`python backend/main.py`)
│   ├── requirements.txt        # Self-contained backend dependencies
│   ├── .env.example            # Environment variables template
│   ├── README.md               # Backend architecture & ML documentation
│   ├── database/
│   │   ├── db.py               # SQLite storage for forecasts, chat & audit logs
│   │   └── raincast.db         # Local SQLite database
│   ├── data/
│   │   ├── raw/
│   │   │   ├── Sub_Division_IMD_2017.csv       # Official IMD Subdivision Archive (1901–2017)
│   │   │   └── subdivision_era5_2018_2025.csv  # ECMWF ERA5 Reanalysis Archive (2018–2025)
│   │   ├── annual_rainfall.csv                 # 1901–2025 canonical authentic records
│   │   └── processed/
│   │       └── india_rainfall_cleaned.csv      # 4,476 cleaned & validated observations
│   ├── models/                                 # Trained model artifacts & performance metrics
│   │   ├── histgradientboosting_regressor.pkl
│   │   ├── xgboost_regressor.pkl
│   │   ├── random_forest_regressor.pkl
│   │   ├── extra_trees_regressor.pkl
│   │   └── model_metadata.json
│   ├── src/                                    # Core analytical, ML & reporting services
│   │   ├── data_collection.py                  # Authentic IMD & ERA5 data compiler
│   │   ├── data_cleaning.py                    # Geographic bounds, median imputation, LPA normal
│   │   ├── feature_engineering.py              # Lags, rolling windows, chronological partitioning
│   │   ├── train_model.py                      # ML training, baseline evaluation & serialization
│   │   ├── prediction.py                       # Recursive multi-year forecasting service (2027+)
│   │   ├── model_evaluation.py                 # Parity plots, residuals, feature importances
│   │   ├── genai_assistant.py                  # Google Gemini SDK & trilingual climate engine
│   │   ├── report_generator.py                 # ReportLab executive PDF & CSV generators
│   │   └── charts.py                           # Backend Plotly visualizer utilities
│   └── tests/                                  # Complete automated test suite
│       ├── test_data.py                        # Geographic bounds & authentic data validation
│       ├── test_prediction.py                  # Inference, recursive forecasting & CI intervals
│       ├── test_fastapi_server.py              # FastAPI routes & REST endpoint status checks
│       └── test_runtime_e2e.py                 # End-to-end integration and pipeline tests
│
├── frontend/
│   ├── README.md                               # Frontend architecture & templates documentation
│   ├── static/
│   │   ├── logo.svg                            # Custom vector branding logo
│   │   └── translations.js                     # Trilingual engine (English, Hindi, Punjabi)
│   └── templates/                              # Jinja2 HTML5 & Tailwind CSS templates
│       ├── base.html                           # Unified navigation, language switcher, footer layout
│       ├── index.html                          # Page 1: Landing & platform overview
│       ├── dashboard.html                      # Page 2: Climate analytics dashboard
│       ├── predict.html                        # Page 3: Multi-horizon ML prediction
│       ├── assistant.html                      # Page 4: Trilingual GenAI assistant
│       ├── models.html                         # Page 5: Model performance & diagnostics
│       └── reports.html                        # Page 6: Executive reports & data export
│
├── .env.example                                # Deployment environment template (copy to .env locally)
├── .gitignore                                  # Production Git exclusions (.env, caches, db)
├── app.py                                      # Root FastAPI universal entry point (`python app.py`)
├── requirements.txt                            # Production Python dependencies for cloud buildpacks
├── Dockerfile                                  # Containerized deployment blueprint
├── Procfile                                    # Render / Heroku / Railway process declaration
├── runtime.txt                                 # Target Python runtime (python-3.11.9)
└── README.md                                   # Complete system technical documentation
```

---

## 7. Quickstart & Installation

### Step 1: Clone or Open Workspace
```bash
cd ARP
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Automated Test Suite
```bash
python -m unittest discover -s backend/tests -p "test_*.py"
```

### Step 4: Launch the Web Platform
```bash
python app.py
```
Open your browser at **`http://localhost:8000`**.

Interactive OpenAPI / Swagger documentation is available at **`http://localhost:8000/docs`**.

---

## 8. REST API Reference

RainCast AI exposes clean, typed RESTful endpoints:

| Endpoint | Method | Description | Example Query / Body |
| :--- | :--- | :--- | :--- |
| `/api/districts/{state}` | `GET` | Returns list of districts/subdivisions for a state. | `/api/districts/Punjab` |
| `/api/dashboard-data` | `GET` | Historical rainfall time series, 5-yr MA, 12-month profile, anomalies. | `?state=Punjab&district=Punjab%20Sub-Division` |
| `/api/predict` | `POST` | Recursive forecast for a future year (2027–2035) with 90% CI & AI explanation. | `{"state":"Punjab", "district":"Punjab Sub-Division", "forecast_year":2027, "model_name":"HistGradientBoosting Regressor", "language":"English"}` |
| `/api/chat` | `POST` | Conversational query with the Trilingual Climate Assistant. | `{"message":"How will monsoon behave in 2027?", "language":"English", "history":[]}` |
| `/api/model-diagnostics` | `GET` | Test actuals, predictions, residuals, and feature importance. | `?model_name=HistGradientBoosting Regressor` |
| `/api/export/pdf` | `GET` | Downloads publication-grade executive PDF report. | `?state=Punjab&district=Punjab%20Sub-Division&forecast_year=2027` |
| `/api/export/csv` | `GET` | Downloads complete 125-year authentic cleaned dataset (`.csv`). | `/api/export/csv` |

---

## 9. Generative AI Configuration

RainCast AI integrates the official **Google Gemini API** (`google-genai`).

1. Obtain an API key from [Google AI Studio](https://aistudio.google.com/).
2. Set your key in the `.env` file:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
3. **Local Scientific Fallback Mode:** If no API key is configured or network is unavailable, the platform automatically switches to its **Deterministic Climate Fallback Engine**, providing rigorous, factually grounded meteorological summaries directly from IMD statistical distributions without crashing or hallucinating.

---

## 10. Production Deployment

### Option A: Docker Container
```bash
# Build Docker image
docker build -t raincast-ai .

# Run container on port 8000
docker run -d -p 8000:8000 -e GEMINI_API_KEY="your-key" --name raincast-app raincast-ai
```
Access at `http://localhost:8000`.

### Option B: Cloud Hosting (Render / Railway / Heroku)
- The project includes a configured `Procfile` (`web: uvicorn app:app --host 0.0.0.0 --port $PORT`).
- Set the environment variable `GEMINI_API_KEY` in the hosting dashboard.
- The web service starts automatically.

---

## 11. Official IMD Meteorological Disclaimer

> **SCIENTIFIC & STATUTORY NOTICE:**  
> RainCast AI provides empirical, machine-learning-based annual rainfall projections developed exclusively for academic research, agricultural planning analysis, and educational demonstration. These outputs are **NOT** official operational weather forecasts. For statutory weather warnings and official seasonal monsoon outlooks, please consult the **India Meteorological Department (IMD)**, Ministry of Earth Sciences, Government of India ([https://mausam.imd.gov.in](https://mausam.imd.gov.in)).


## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for the Render deployment guide. The repository includes `render.yaml` for Blueprint deployment.
# annual-rainfall-prediction
