"""
RainCast AI - Automated Test Suite for FastAPI + HTML/Tailwind Server
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

for p in [str(ROOT_DIR), str(BACKEND_DIR), str(FRONTEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import unittest
import urllib.request
import json


class TestFastAPIServer(unittest.TestCase):
    BASE_URL = "http://localhost:8000"

    def test_01_home_page(self):
        url = f"{self.BASE_URL}/"
        resp = urllib.request.urlopen(url)
        self.assertEqual(resp.status, 200)
        content = resp.read().decode("utf-8")
        self.assertIn("RainCast", content)
        self.assertIn("Enterprise Suite", content)

    def test_02_dashboard_page(self):
        url = f"{self.BASE_URL}/dashboard"
        resp = urllib.request.urlopen(url)
        self.assertEqual(resp.status, 200)
        content = resp.read().decode("utf-8")
        self.assertIn("Climate Analytics Dashboard", content)

    def test_03_predict_page(self):
        url = f"{self.BASE_URL}/predict"
        resp = urllib.request.urlopen(url)
        self.assertEqual(resp.status, 200)
        content = resp.read().decode("utf-8")
        self.assertIn("Annual Rainfall Prediction Engine", content)

    def test_04_assistant_page(self):
        url = f"{self.BASE_URL}/assistant"
        resp = urllib.request.urlopen(url)
        self.assertEqual(resp.status, 200)
        content = resp.read().decode("utf-8")
        self.assertIn("Climate AI Assistant", content)

    def test_05_models_page(self):
        url = f"{self.BASE_URL}/models"
        resp = urllib.request.urlopen(url)
        self.assertEqual(resp.status, 200)
        content = resp.read().decode("utf-8")
        self.assertIn("Model Rigor", content)

    def test_06_reports_page(self):
        url = f"{self.BASE_URL}/reports"
        resp = urllib.request.urlopen(url)
        self.assertEqual(resp.status, 200)
        content = resp.read().decode("utf-8")
        self.assertIn("Executive Climate Reports", content)

    def test_07_districts_api(self):
        url = f"{self.BASE_URL}/api/districts/Punjab"
        resp = urllib.request.urlopen(url)
        self.assertEqual(resp.status, 200)
        districts = json.loads(resp.read().decode("utf-8"))
        self.assertTrue(len(districts) > 0)
        self.assertIn("Punjab Sub-Division", districts)

    def test_08_dashboard_data_api(self):
        url = f"{self.BASE_URL}/api/dashboard-data?state=Punjab&district=Punjab%20Sub-Division"
        resp = urllib.request.urlopen(url)
        self.assertEqual(resp.status, 200)
        data = json.loads(resp.read().decode("utf-8"))
        self.assertIn("lpa_normal", data)
        self.assertIn("annual_series", data)
        self.assertEqual(len(data["years"]), 125)

    def test_09_predict_api(self):
        url = f"{self.BASE_URL}/api/predict"
        payload = json.dumps({
            "state": "Punjab",
            "district": "Ludhiana",
            "forecast_year": 2027,
            "model_name": "Random Forest Regressor",
            "language": "English"
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req)
        self.assertEqual(resp.status, 200)
        res = json.loads(resp.read().decode("utf-8"))
        self.assertIn("predicted_rainfall_mm", res)
        self.assertGreater(res["predicted_rainfall_mm"], 50.0)
        self.assertIn(res["classification"], ["Normal", "Deficient", "Excess", "Large Deficient", "Large Excess"])
        self.assertIn("ai_explanation", res)

    def test_10_diagnostics_api(self):
        url = f"{self.BASE_URL}/api/model-diagnostics"
        resp = urllib.request.urlopen(url)
        self.assertEqual(resp.status, 200)
        data = json.loads(resp.read().decode("utf-8"))
        self.assertIn("actuals", data)
        self.assertIn("predictions", data)
        self.assertEqual(len(data["actuals"]), 360)

    def test_11_chat_api(self):
        url = f"{self.BASE_URL}/api/chat"
        payload = json.dumps({
            "message": "What is the expected monsoon for Punjab in 2027?",
            "language": "English",
            "history": []
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req)
        self.assertEqual(resp.status, 200)
        res = json.loads(resp.read().decode("utf-8"))
        self.assertIn("response", res)
        self.assertGreater(len(res["response"]), 20)

    def test_12_pdf_export_api(self):
        url = f"{self.BASE_URL}/api/export/pdf?state=Punjab&district=Ludhiana&forecast_year=2027&model_name=Random%20Forest%20Regressor"
        resp = urllib.request.urlopen(url)
        self.assertEqual(resp.status, 200)
        content = resp.read()
        self.assertTrue(content.startswith(b"%PDF"), "Response is not a valid PDF file")

    def test_13_static_translations(self):
        url = f"{self.BASE_URL}/static/translations.js"
        resp = urllib.request.urlopen(url)
        self.assertEqual(resp.status, 200)
        content = resp.read().decode("utf-8")
        self.assertIn("TRANSLATIONS", content)
        self.assertIn("en:", content)
        self.assertIn("hi:", content)
        self.assertIn("pa:", content)
        self.assertIn("English", content)
        self.assertIn("हिंदी", content)
        self.assertIn("ਪੰਜਾਬੀ", content)

    def test_14_predict_api_multilingual(self):
        for lang in ["Hindi", "Punjabi"]:
            url = f"{self.BASE_URL}/api/predict"
            payload = json.dumps({
                "state": "Punjab",
                "district": "Ludhiana",
                "forecast_year": 2027,
                "model_name": "Random Forest Regressor",
                "language": lang
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req)
            self.assertEqual(resp.status, 200)
            res = json.loads(resp.read().decode("utf-8"))
            self.assertIn("ai_explanation", res)
            self.assertGreater(len(res["ai_explanation"]), 20)

    def test_15_chat_api_multilingual(self):
        for lang, expected_char in [("Hindi", "ह"), ("Punjabi", "ਪ")]:
            url = f"{self.BASE_URL}/api/chat"
            payload = json.dumps({
                "message": "वर्षा की क्या स्थिति है?" if lang == "Hindi" else "ਮੀਂਹ ਦਾ ਕੀ ਹਾਲ ਹੈ?",
                "language": lang,
                "history": []
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req)
            self.assertEqual(resp.status, 200)
            res = json.loads(resp.read().decode("utf-8"))
            self.assertIn("response", res)
            self.assertGreater(len(res["response"]), 10)


if __name__ == "__main__":
    unittest.main()

