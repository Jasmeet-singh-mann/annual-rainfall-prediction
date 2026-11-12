"""
Fetches authentic 2018–2025 precipitation observations from ECMWF ERA5 Reanalysis
via Open-Meteo Archive API for all 36 IMD Meteorological Subdivisions.
Saves genuine records to backend/data/raw/subdivision_era5_2018_2025.csv.
"""

import time
import requests
import pandas as pd
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BACKEND_DIR / "data" / "raw"
OUTPUT_PATH = RAW_DATA_DIR / "subdivision_era5_2018_2025.csv"

# 36 Official IMD Meteorological Subdivisions metadata mapping
IMD_SUBDIVISIONS_METADATA = {
    "Andaman & Nicobar Islands": ("Andaman and Nicobar Islands", "Andaman & Nicobar Sub-Division", 11.6234, 92.7265, 16),
    "Arunachal Pradesh": ("Arunachal Pradesh", "Arunachal Pradesh Sub-Division", 28.2180, 94.7278, 600),
    "Assam & Meghalaya": ("Assam", "Assam & Meghalaya Sub-Division", 26.1445, 91.7362, 120),
    "Bihar": ("Bihar", "Bihar Sub-Division", 25.5941, 85.1376, 53),
    "Chhattisgarh": ("Chhattisgarh", "Chhattisgarh Sub-Division", 21.2514, 81.6296, 298),
    "Coastal Andhra Pradesh": ("Andhra Pradesh", "Coastal Andhra Pradesh Sub-Division", 16.5062, 80.6480, 25),
    "Coastal Karnataka": ("Karnataka", "Coastal Karnataka Sub-Division", 13.5000, 74.8560, 30),
    "East Madhya Pradesh": ("Madhya Pradesh", "East Madhya Pradesh Sub-Division", 23.1815, 79.9864, 411),
    "East Rajasthan": ("Rajasthan", "East Rajasthan Sub-Division", 26.9124, 75.7873, 431),
    "East Uttar Pradesh": ("Uttar Pradesh", "East Uttar Pradesh Sub-Division", 26.8467, 81.9400, 105),
    "Gangetic West Bengal": ("West Bengal", "Gangetic West Bengal Sub-Division", 22.5726, 88.3639, 15),
    "Gujarat Region": ("Gujarat", "Gujarat Region Sub-Division", 23.0225, 72.5714, 55),
    "Haryana Delhi & Chandigarh": ("Haryana", "Haryana Delhi & Chandigarh Sub-Division", 28.5855, 77.1000, 220),
    "Himachal Pradesh": ("Himachal Pradesh", "Himachal Pradesh Sub-Division", 31.1048, 77.1734, 1800),
    "Jammu & Kashmir": ("Jammu and Kashmir", "Jammu & Kashmir Sub-Division", 34.0837, 74.7973, 1585),
    "Jharkhand": ("Jharkhand", "Jharkhand Sub-Division", 23.3441, 85.3096, 651),
    "Kerala": ("Kerala", "Kerala Sub-Division", 10.8505, 76.2711, 50),
    "Konkan & Goa": ("Goa", "Konkan & Goa Sub-Division", 15.4909, 73.8278, 25),
    "Lakshadweep": ("Lakshadweep", "Lakshadweep Sub-Division", 10.5667, 72.6417, 5),
    "Madhya Maharashtra": ("Maharashtra", "Madhya Maharashtra Sub-Division", 18.5204, 73.8567, 560),
    "Matathwada": ("Maharashtra", "Marathwada Sub-Division", 19.8762, 75.3433, 580),
    "Naga Mani Mizo Tripura": ("Nagaland", "Naga Mani Mizo Tripura Sub-Division", 25.6751, 94.1086, 700),
    "North Interior Karnataka": ("Karnataka", "North Interior Karnataka Sub-Division", 15.3647, 75.1240, 640),
    "Orissa": ("Odisha", "Odisha Sub-Division", 20.2961, 85.8245, 45),
    "Punjab": ("Punjab", "Punjab Sub-Division", 30.9010, 75.8573, 240),
    "Rayalseema": ("Andhra Pradesh", "Rayalaseema Sub-Division", 14.6819, 77.6006, 350),
    "Saurashtra & Kutch": ("Gujarat", "Saurashtra & Kutch Sub-Division", 22.3039, 70.8022, 120),
    "South Interior Karnataka": ("Karnataka", "South Interior Karnataka Sub-Division", 12.9716, 77.5946, 900),
    "Sub Himalayan West Bengal & Sikkim": ("West Bengal", "Sub Himalayan West Bengal & Sikkim Sub-Division", 26.7271, 88.4200, 400),
    "Tamil Nadu": ("Tamil Nadu", "Tamil Nadu Sub-Division", 11.1271, 78.6569, 150),
    "Telangana": ("Telangana", "Telangana Sub-Division", 17.3850, 78.4867, 540),
    "Uttarakhand": ("Uttarakhand", "Uttarakhand Sub-Division", 30.3165, 78.0322, 680),
    "Vidarbha": ("Maharashtra", "Vidarbha Sub-Division", 21.1458, 79.0882, 310),
    "West Madhya Pradesh": ("Madhya Pradesh", "West Madhya Pradesh Sub-Division", 22.7196, 75.8577, 550),
    "West Rajasthan": ("Rajasthan", "West Rajasthan Sub-Division", 26.9157, 70.9083, 225),
    "West Uttar Pradesh": ("Uttar Pradesh", "West Uttar Pradesh Sub-Division", 27.1767, 78.0081, 170),
}

all_records = []
url = "https://archive-api.open-meteo.com/v1/archive"
headers = {"User-Agent": "RainCastAI/2.4 (Academic Climate Research; info@raincast.ai)"}

month_names = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

print(f"Fetching authentic ERA5 reanalysis data for {len(IMD_SUBDIVISIONS_METADATA)} subdivisions (2018–2025)...", flush=True)

for i, (sub_name, (state, district, lat, lon, elev)) in enumerate(IMD_SUBDIVISIONS_METADATA.items(), 1):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2018-01-01",
        "end_date": "2025-12-31",
        "daily": "precipitation_sum",
        "timezone": "Asia/Kolkata"
    }
    
    success = False
    for attempt in range(3):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                daily = data.get("daily", {})
                times = daily.get("time", [])
                precip = daily.get("precipitation_sum", [])
                if times and precip:
                    df_d = pd.DataFrame({"date": times, "precip": precip})
                    df_d["date"] = pd.to_datetime(df_d["date"])
                    df_d["year"] = df_d["date"].dt.year
                    df_d["month"] = df_d["date"].dt.month
                    
                    for yr in range(2018, 2026):
                        sub_yr = df_d[df_d["year"] == yr]
                        if len(sub_yr) > 0:
                            m_sums = []
                            for m in range(1, 13):
                                m_val = round(float(sub_yr[sub_yr["month"] == m]["precip"].sum()), 1)
                                m_sums.append(m_val)
                            ann_val = round(float(sum(m_sums)), 1)
                            rainy_cnt = int(sub_yr[sub_yr["precip"] >= 2.5]["precip"].count())
                            
                            rec = {
                                "SUBDIVISION": sub_name,
                                "state": state,
                                "district": district,
                                "latitude": lat,
                                "longitude": lon,
                                "elevation": elev,
                                "year": yr,
                                "annual_rainfall": ann_val,
                                "rainy_days": rainy_cnt,
                                "data_source": "ECMWF ERA5 Atmospheric Reanalysis"
                            }
                            for m_idx, m_name in enumerate(month_names):
                                rec[f"{m_name}_rainfall"] = m_sums[m_idx]
                            all_records.append(rec)
                    success = True
                    print(f" [{i}/{len(IMD_SUBDIVISIONS_METADATA)}] {sub_name}: 8 years fetched successfully", flush=True)
                    break
            time.sleep(0.5)
        except Exception as e:
            print(f" [{i}/{len(IMD_SUBDIVISIONS_METADATA)}] {sub_name} attempt {attempt+1} retry: {e}", flush=True)
            time.sleep(1.0)
    
    if not success:
        print(f"WARNING: Failed to fetch ERA5 for {sub_name}", flush=True)
    time.sleep(0.3)

df_out = pd.DataFrame(all_records)
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
df_out.to_csv(OUTPUT_PATH, index=False)
print(f"DONE: Successfully saved {len(df_out)} genuine ERA5 records (2018–2025) to {OUTPUT_PATH}!", flush=True)
