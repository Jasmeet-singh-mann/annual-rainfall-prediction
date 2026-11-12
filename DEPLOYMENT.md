# Deploy RainCast AI on Render

This project is a **FastAPI + Jinja2** application (not Streamlit). The included `render.yaml` configures a Python web service.

## Before publishing

1. The original uploaded `.env` file has intentionally been removed from this deployment copy.
2. If the original Gemini key was ever shared or committed, revoke it in Google AI Studio and create a new key.
3. Keep the new key only in Render Environment settings as `GEMINI_API_KEY`. Never put it in GitHub, source code, or this ZIP.
4. Review dataset provenance and model limitations before presenting predictions as verified observations.

## Deploy steps

1. Extract this ZIP. The repository root is the `ARP` folder (the folder containing `app.py`, `requirements.txt`, and `render.yaml`).
2. Create a new GitHub repository, for example `raincast-ai`.
3. Upload/push the **contents** of the `ARP` folder to the repository root. Do not upload `.env`, local secrets, or `__pycache__` files.
4. Sign in to https://render.com and choose **New + → Blueprint**.
5. Connect GitHub, select the `raincast-ai` repository, and let Render read `render.yaml`.
6. Before deploying, open the service Environment settings and add `GEMINI_API_KEY` with your newly generated key. If you skip it, the site should still run but Gemini-powered answers may use the app's fallback/error behavior.
7. Deploy. Render installs `requirements.txt` and runs `uvicorn app:app --host 0.0.0.0 --port $PORT`.
8. When the deployment finishes, open the `onrender.com` URL and test `/`, `/dashboard`, `/predict`, `/assistant`, `/models`, `/reports`, and `/docs`.

## Important hosting notes

- The service uses SQLite at `backend/database/raincast.db`. On a free Render web service, local filesystem changes are ephemeral and may be lost on restart/redeploy. For durable prediction/chat/report logs, attach a persistent disk on a supported paid plan or migrate the database to managed PostgreSQL and update the database layer.
- The project includes trained `.pkl` models. They must be loaded with compatible scikit-learn/XGBoost versions. If startup or model loading fails, pin the training versions in `requirements.txt` and retrain/re-export with those same versions.
- Free instances may spin down after inactivity and take time to wake up.
- Do not use a free instance for critical weather warnings or operational forecasting.

## Local smoke test before deployment

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open http://127.0.0.1:8000.
