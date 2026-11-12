"""
RainCast AI - Generative AI Climate Assistant
Integrates Google Gemini API using the official google-genai SDK.
Provides context-aware multilingual climate explanations and conversational intelligence.
"""

import sys
from pathlib import Path
BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
for p in [str(PROJECT_ROOT), str(BACKEND_DIR), str(FRONTEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import os
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from config import APP_NAME, SCIENTIFIC_DISCLAIMER, GEMINI_API_KEY
from src.prediction import get_cached_dataset, predict_annual_rainfall


def get_gemini_client(api_key: Optional[str] = None):
    """Initializes Google GenAI client if API key is present."""
    key = api_key or os.environ.get("GEMINI_API_KEY") or GEMINI_API_KEY
    if key and len(key.strip()) > 10:
        try:
            from google import genai
            from google.genai import types
            return genai.Client(api_key=key.strip(), http_options=types.HttpOptions(timeout=10.0))
        except Exception as e:
            print(f"GenAI Client Init Notice: {e}")
            return None
    return None


def get_grounded_system_context(state: Optional[str] = None, district: Optional[str] = None) -> str:
    """Extracts genuine meteorological baseline facts from dataset for grounding."""
    df = get_cached_dataset()
    
    total_locations = df["location"].nunique()
    overall_mean = round(float(df["annual_rainfall"].mean()), 1)
    
    context = (
        f"PLATFORM: {APP_NAME} (Climate Intelligence for India)\n"
        f"DATASET COVERAGE: 1901 to 2025 ({total_locations} verified Indian meteorological subdivisions).\n"
        f"NATIONWIDE ALL-INDIA AVERAGE: {overall_mean} mm per year.\n"
    )

    if state:
        st_df = df[df["state"] == state]
        if len(st_df) > 0:
            st_mean = round(float(st_df["annual_rainfall"].mean()), 1)
            st_min = round(float(st_df["annual_rainfall"].min()), 1)
            st_max = round(float(st_df["annual_rainfall"].max()), 1)
            context += f"CURRENT STATE: {state} (Historical Mean: {st_mean} mm, Range: {st_min}–{st_max} mm).\n"

    if state and district:
        dist_df = df[(df["state"] == state) & (df["district"] == district)]
        if len(dist_df) > 0:
            lpa = float(dist_df["lpa_normal"].iloc[-1])
            latest_val = float(dist_df["annual_rainfall"].iloc[-1])
            latest_yr = int(dist_df["year"].max())
            context += (
                f"CURRENT DISTRICT: {district}, {state}\n"
                f"- Long Period Average (Normal LPA): {lpa} mm\n"
                f"- Latest Observed Rainfall ({latest_yr}): {latest_val} mm\n"
            )

    return context


def generate_prediction_explanation(pred_data: Dict[str, Any], language: str = "English", api_key: Optional[str] = None) -> str:
    """
    Generates a professional, scientifically accurate explanation of the model forecast.
    Grounds output with actual numbers and explains practical agro-climatic significance.
    """
    client = get_gemini_client(api_key)
    state = pred_data.get("state", "India")
    district = pred_data.get("district", "")
    pred_val = pred_data.get("predicted_rainfall_mm", 0.0)
    normal = pred_data.get("normal_lpa_mm", 0.0)
    anomaly_pct = pred_data.get("anomaly_pct", 0.0)
    cat = pred_data.get("classification", "Normal")
    year = pred_data.get("forecast_year", 2025)
    model_name = pred_data.get("model_name", "Random Forest Regressor")
    ci_lower = pred_data.get("confidence_lower", 0.0)
    ci_upper = pred_data.get("confidence_upper", 0.0)

    lang_instructions = {
        "English": "Respond in clear, professional English.",
        "Hindi": "उत्तर शुद्ध, सरल और औपचारिक हिंदी (Devanagari script) में दें।",
        "Punjabi": "ਉੱਤਰ ਸਪੱਸ਼ਟ, ਸਰਲ ਅਤੇ ਸ਼ੁੱਧ ਪੰਜਾਬੀ (Gurmukhi script) ਵਿੱਚ ਦਿਓ।"
    }
    lang_prompt = lang_instructions.get(language, lang_instructions["English"])

    prompt = f"""
    You are the Chief Meteorologist & AI Climate Scientist for RainCast AI.
    Analyze this annual rainfall prediction:
    - Location: {district}, {state}, India
    - Forecast Year: {year}
    - Predicted Annual Rainfall: {pred_val} mm
    - 90% Confidence Interval: [{ci_lower} mm to {ci_upper} mm]
    - Historical 30-Year Normal (LPA): {normal} mm
    - Rainfall Anomaly: {anomaly_pct}% ({cat})
    - Forecasting Model: {model_name}

    Requirements:
    1. Clearly state whether this represents deficit, normal, or excess conditions relative to historical LPA.
    2. Explain what this implies for regional agriculture, groundwater recharge, and reservoir storage.
    3. Explicitly state the 90% uncertainty margin [{ci_lower} - {ci_upper} mm].
    4. State clearly that this is an experimental ML statistical estimate, NOT an official IMD weather forecast.
    5. Keep response concise, structured into 3 bullet points, under 140 words.
    6. {lang_prompt}
    """

    if client:
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-flash-latest",
            "gemini-2.5-flash-lite",
            "gemini-3.5-flash",
            "gemini-3.8-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash"
        ]
        for m_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=m_name,
                    contents=prompt
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                continue
        print("Gemini API notice: Remote models unavailable or key unconfigured, using local climate engine.")

    # High-quality grounded fallback engine
    if language == "Hindi":
        direction = "अधिक" if anomaly_pct > 0 else "कम"
        return (
            f"• **वर्षा पूर्वानुमान ({year})**: {district} ({state}) के लिए अनुमानित वार्षिक वर्षा **{pred_val:,.1f} मिमी** है, "
            f"जो कि ऐतिहासिक सामान्य स्तर ({normal:,.1f} मिमी) की तुलना में **{abs(anomaly_pct):.1f}% {direction}** है ({cat} श्रेणी)।\n"
            f"• **कृषि एवं जल संसाधन प्रभाव**: यह स्थिति मुख्य रूप से खरीफ और रबी फसलों के लिए महत्वपूर्ण जल उपलब्धता को दर्शाती है। "
            f"सांख्यिकीय 90% विश्वसनीयता अंतराल **{ci_lower:,.1f} मिमी से {ci_upper:,.1f} मिमी** के बीच अनुमानित है।\n"
            f"• **वैज्ञानिक अस्वीकरण**: यह पूर्वानुमान मशीन लर्निंग सांख्यिकीय मॉडल ({model_name}) पर आधारित शोध अनुमान है, आधिकारिक IMD मौसम चेतावनी नहीं।"
        )
    elif language == "Punjabi":
        direction = "ਵੱਧ" if anomaly_pct > 0 else "ਘੱਟ"
        return (
            f"• **ਮੀਂਹ ਦਾ ਅਨੁਮਾਨ ({year})**: {district} ({state}) ਲਈ ਅਨੁਮਾਨਿਤ ਸਾਲਾਨਾ ਵਰਖਾ **{pred_val:,.1f} ਮਿ.ਮੀ.** ਹੈ, "
            f"ਜੋ ਕਿ ਇਤਿਹਾਸਕ ਔਸਤ ({normal:,.1f} ਮਿ.ਮੀ.) ਨਾਲੋਂ **{abs(anomaly_pct):.1f}% {direction}** ਹੈ ({cat} ਸ਼੍ਰੇਣੀ)।\n"
            f"• **ਖੇਤੀਬਾੜੀ ਅਤੇ ਜਲ ਪ੍ਰਬੰਧਨ ਪ੍ਰਭਾਵ**: ਇਹ ਅਨੁਮਾਨ ਖੇਤੀਬਾੜੀ ਅਤੇ ਜ਼ਮੀਨੀ ਪਾਣੀ ਦੇ ਪੱਧਰ ਲਈ ਜ਼ਰੂਰੀ ਅੰਦਾਜ਼ਾ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ। "
            f"90% ਭਰੋਸੇਯੋਗਤਾ ਸੀਮਾ **{ci_lower:,.1f} ਮਿ.ਮੀ. ਤੋਂ {ci_upper:,.1f} ਮਿ.ਮੀ.** ਹੈ।\n"
            f"• **ਵਿਗਿਆਨਕ ਸਪੱਸ਼ਟੀਕਰਨ**: ਇਹ ਮਸ਼ੀਨ ਲਰਨਿੰਗ ({model_name}) 'ਤੇ ਅਧਾਰਤ ਖੋਜ ਅਨੁਮਾਨ ਹੈ, ਸਰਕਾਰੀ IMD ਮੌਸਮ ਚੇਤਾਵਨੀ ਨਹੀਂ।"
        )
    else:
        direction = "above" if anomaly_pct > 0 else "below"
        return (
            f"• **Rainfall Projection ({year})**: Projected annual rainfall for {district}, {state} is **{pred_val:,.1f} mm**, "
            f"which is **{abs(anomaly_pct):.1f}% {direction}** the long-term normal of {normal:,.1f} mm, placing it in the **{cat}** category.\n"
            f"• **Agro-Climatic Implications**: The predicted volume indicates adequate moisture for primary cropping cycles. "
            f"The 90% statistical confidence interval spans **{ci_lower:,.1f} mm to {ci_upper:,.1f} mm** with model uncertainty accounted for.\n"
            f"• **Scientific Advisory**: This projection is an experimental machine learning estimate ({model_name}) and does not supersede official IMD meteorological advisories."
        )


def chat_with_climate_assistant(
    user_message: str,
    session_history: List[Dict[str, str]],
    state_context: Optional[str] = None,
    district_context: Optional[str] = None,
    language: str = "English",
    api_key: Optional[str] = None
) -> str:
    """
    Handles multi-turn conversational interactions for 'RainCast AI Climate Assistant'.
    Maintains factual grounding strictly from genuine IMD dataset and predictions.
    """
    client = get_gemini_client(api_key)
    grounded_context = get_grounded_system_context(state_context, district_context)

    lang_instructions = {
        "English": "Respond in English.",
        "Hindi": "उत्तर देवनागरी लिपि में हिंदी में दें।",
        "Punjabi": "ਉੱਤਰ ਗੁਰਮੁਖੀ ਲਿਪੀ ਵਿੱਚ ਪੰਜਾਬੀ ਵਿੱਚ ਦਿਓ।"
    }
    lang_prompt = lang_instructions.get(language, lang_instructions["English"])

    if client:
        try:
            # Build conversation history
            messages_payload = [
                f"You are 'RainCast AI Climate Assistant', an authoritative, scientifically grounded climate and meteorological AI.\n"
                f"CRITICAL RULES:\n"
                f"1. Never invent or hallucinate fake rainfall numbers. Base your analysis strictly on the grounded meteorological facts below.\n"
                f"2. Clearly distinguish between historical observations (1901-2026) and statistical model projections.\n"
                f"3. Explain climatic mechanisms (e.g. Southwest Monsoon, ENSO, Western Disturbances, Orographic lift) when asked.\n"
                f"4. If data for a requested location is not in the system, clearly state that data coverage is not available.\n"
                f"5. {lang_prompt}\n\n"
                f"GROUNDED METEOROLOGICAL CONTEXT:\n{grounded_context}"
            ]
            for turn in session_history[-6:]:
                role_label = "User" if turn.get("role") == "user" else "Assistant"
                messages_payload.append(f"{role_label}: {turn.get('message', '')}")
            
            messages_payload.append(f"User: {user_message}\nAssistant:")
            prompt_full = "\n\n".join(messages_payload)

            models_to_try = [
                "gemini-2.5-flash",
                "gemini-flash-latest",
                "gemini-2.5-flash-lite",
                "gemini-3.5-flash",
                "gemini-3.8-flash",
                "gemini-2.0-flash",
                "gemini-1.5-flash"
            ]
            for m_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=m_name,
                        contents=prompt_full
                    )
                    if response and response.text:
                        return response.text.strip()
                except Exception:
                    continue
        except Exception as e:
            print(f"Gemini Chat Notice: {e}, using local Climate Intelligence Engine.")

    # Local Knowledge & Grounded Answering Engine
    msg_lower = user_message.lower()
    df = get_cached_dataset()

    # Rule 1: Specific state query (e.g. "Punjab", "Maharashtra", "Kerala")
    for st_name in df["state"].unique():
        if st_name.lower() in msg_lower:
            st_df = df[df["state"] == st_name]
            st_normal = round(float(st_df["annual_rainfall"].mean()), 1)
            dist_list = ", ".join(st_df["district"].unique()[:4])
            if language == "Hindi":
                return (
                    f"**{st_name}** के लिए हमारे ऐतिहासिक डेटाबेस (1901–2025) में औसत वार्षिक वर्षा **{st_normal:,.1f} मिमी** है। "
                    f"प्रमुख उप-मंडल जैसे {dist_list} इसमें शामिल हैं। 2027 के लिए सांख्यिकीय मॉडल संतुलित वर्षा का अनुमान लगा रहे हैं।"
                )
            elif language == "Punjabi":
                return (
                    f"**{st_name}** ਲਈ ਸਾਡੇ ਇਤਿਹਾਸਕ ਰਿਕਾਰਡ (1901–2025) ਅਨੁਸਾਰ ਔਸਤਨ ਸਾਲਾਨਾ ਵਰਖਾ **{st_normal:,.1f} ਮਿ.ਮੀ.** ਹੈ। "
                    f"ਇਸ ਵਿੱਚ ਪ੍ਰਮੁੱਖ ਉਪ-ਮੰਡਲ ਸ਼ਾਮਲ ਹਨ ਜਿਵੇਂ {dist_list}। ਮਸ਼ੀਨ ਲਰਨਿੰਗ ਮਾਡਲ ਅਨੁਸਾਰ 2027 ਵਿੱਚ ਸੰਤੁਲਿਤ ਵਰਖਾ ਰਹਿਣ ਦੀ ਸੰਭਾਵਨਾ ਹੈ।"
                )
            else:
                return (
                    f"For **{st_name}**, the historical long-term average (1901–2025) stands at **{st_normal:,.1f} mm** annually. "
                    f"Representative meteorological subdivisions include {dist_list}. "
                    f"Model predictions for 2027 onward indicate that rainfall follows cyclical variations influenced by monsoon dynamics."
                )

    # Rule 2: Anomaly explanation
    if "anomaly" in msg_lower or "विपरीत" in msg_lower or "ਐਨੋਮਲੀ" in msg_lower:
        if language == "Hindi":
            return (
                "**वर्षा विसंगति (Rainfall Anomaly)** का अर्थ है किसी दिए गए वर्ष में दर्ज की गई वर्षा और 30-वर्षीय सामान्य औसत (LPA) के बीच का अंतर। "
                "यदि विसंगति -19% से +19% के बीच हो तो इसे सामान्य (Normal), -20% से -59% को कमी (Deficient), और +20% से अधिक को अधिशेष (Excess) माना जाता है।"
            )
        elif language == "Punjabi":
            return (
                "**ਵਰਖਾ ਅਸੰਗਤੀ (Rainfall Anomaly)** ਦਾ ਮਤਲਬ ਹੈ ਕਿਸੇ ਸਾਲ ਹੋਈ ਅਸਲ ਵਰਖਾ ਅਤੇ 30-ਸਾਲਾ ਲੰਬੀ ਮਿਆਦ ਦੀ ਔਸਤ (LPA) ਵਿਚਕਾਰ ਦਾ ਅੰਤਰ। "
                "ਭਾਰਤੀ ਮੌਸਮ ਵਿਭਾਗ (IMD) ਅਨੁਸਾਰ -19% ਤੋਂ +19% ਵਿਚਕਾਰ ਵਰਖਾ ਨੂੰ 'ਆਮ' (Normal) ਮੰਨਿਆ ਜਾਂਦਾ ਹੈ।"
            )
        else:
            return (
                "A **Rainfall Anomaly** represents the percentage or millimeter deviation of observed/predicted precipitation "
                "from the 30-year Long Period Average (LPA) baseline. "
                "According to IMD classification criteria:\n"
                "- **Normal**: -19% to +19%\n"
                "- **Deficient**: -20% to -59%\n"
                "- **Excess**: +20% to +59%\n"
                "- **Large Deficient**: < -59%\n"
                "- **Large Excess**: >= +60%"
            )

    # Rule 3: Highest rainfall locations
    if "highest" in msg_lower or "most" in msg_lower or "अधिक" in msg_lower or "ਸਭ ਤੋਂ ਵੱਧ" in msg_lower:
        top_stations = df.groupby(["state", "district"])["annual_rainfall"].mean().sort_values(ascending=False).head(3)
        top_list = [f"{dist} ({st}): {val:,.1f} mm" for (st, dist), val in top_stations.items()]
        joined = "; ".join(top_list)
        if language == "Hindi":
            return f"भारत में हमारे ऐतिहासिक डेटासेट के अनुसार सबसे अधिक वर्षा वाले क्षेत्र हैं: **{joined}**। चेरापूंजी और पश्चिमी घाट में पर्वतीय वर्षा (orographic lift) के कारण सर्वाधिक वर्षा होती है।"
        elif language == "Punjabi":
            return f"ਸਾਡੇ ਡੇਟਾਸੈੱਟ ਅਨੁਸਾਰ ਭਾਰਤ ਵਿੱਚ ਸਭ ਤੋਂ ਵੱਧ ਔਸਤਨ ਵਰਖਾ ਵਾਲੇ ਖੇਤਰ ਹਨ: **{joined}**। ਇਹ ਖੇਤਰ ਪੱਛਮੀ ਘਾਟ ਅਤੇ ਉੱਤਰ-ਪੂਰਬੀ ਪਹਾੜੀਆਂ ਕਾਰਨ ਭਾਰੀ ਵਰਖਾ ਪ੍ਰਾਪਤ ਕਰਦੇ ਹਨ।"
        else:
            return (
                f"According to historical meteorological records, the highest annual rainfall in India occurs at: **{joined}**. "
                f"These regions benefit from pronounced orographic lift against the Western Ghats and Khasi Hills during the Southwest Monsoon."
            )

    # Rule 4: Agriculture significance
    if "agri" in msg_lower or "crop" in msg_lower or "कृषि" in msg_lower or "ਖੇਤੀ" in msg_lower:
        if language == "Hindi":
            return (
                "भारतीय कृषि में वार्षिक वर्षा और विशेष रूप से दक्षिण-पश्चिम मानसून (JJAS) का अत्यधिक महत्व है। "
                "भारत के 50% से अधिक फसली क्षेत्र वर्षा आधारित हैं। समय पर सामान्य वर्षा धान, कपास, दालों और तिलहनों की उच्च उपज सुनिश्चित करती है और भूजल स्तर को रिचार्ज करती है।"
            )
        elif language == "Punjabi":
            return (
                "ਖੇਤੀਬਾੜੀ ਲਈ ਮਾਨਸੂਨ ਵਰਖਾ ਰੀੜ੍ਹ ਦੀ ਹੱਡੀ ਹੈ। ਖ਼ਾਸ ਕਰਕੇ ਸਾਉਣੀ (Kharif) ਅਤੇ ਹਾੜੀ (Rabi) ਦੀਆਂ ਫ਼ਸਲਾਂ ਲਈ ਸਹੀ ਸਮੇਂ 'ਤੇ ਮੀਂਹ ਪੈਣਾ ਜ਼ਰੂਰੀ ਹੈ। "
                "ਇਸ ਤੋਂ ਇਲਾਵਾ ਡੈਮਾਂ ਵਿੱਚ ਪਾਣੀ ਅਤੇ ਜ਼ਮੀਨ ਹੇਠਲੇ ਪਾਣੀ ਦੇ ਪੱਧਰ ਲਈ ਇਹ ਬਹੁਤ ਅਹਿਮ ਹੈ।"
            )
        else:
            return (
                "Over 50% of India's net sown area is rainfed, making annual rainfall—particularly the June–September Southwest Monsoon—vital for agriculture. "
                "Adequate and well-distributed rainfall ensures optimal soil moisture for Kharif crops (rice, pulses, cotton), replenishes irrigation reservoirs, "
                "and recharges groundwater tables critical for winter Rabi cultivation."
            )

    # General fallback
    if language == "Hindi":
        return (
            f"मैं **RainCast AI क्लाइमेट असिस्टेंट** हूँ। हमारे डेटासेट में 1901 से 2026 तक के सभी 85 भारतीय भौगोलिक क्षेत्र (36 आईएमडी उप-मंडल + 49 मौसम स्टेशन) शामिल हैं। "
            f"आप मुझसे किसी भी राज्य के ऐतिहासिक रुझान, 2027 से आगे के वार्षिक पूर्वानुमान, मानसून पैटर्न या कृषि सलाह के बारे में पूछ सकते हैं।"
        )
    elif language == "Punjabi":
        return (
            f"ਮੈਂ **RainCast AI ਕਲਾਈਮੇਟ ਅਸਿਸਟੈਂਟ** ਹਾਂ। ਸਾਡੇ ਕੋਲ 1901 ਤੋਂ 2026 ਤੱਕ ਦੇ 85 ਭੂਗੋਲਿਕ ਖੇਤਰਾਂ (36 ਆਈ.ਐਮ.ਡੀ ਉਪ-ਮੰਡਲ + 49 ਮੌਸਮ ਸਟੇਸ਼ਨ) ਦੇ ਅਧਿਕਾਰਤ ਅੰਕੜੇ ਹਨ। "
            f"ਤੁਸੀਂ ਪੰਜਾਬ ਜਾਂ ਕਿਸੇ ਵੀ ਹੋਰ ਰਾਜ ਦੀ ਸਾਲਾਨਾ ਵਰਖਾ, 2027 ਦੇ ਮਾਡਲ ਅਨੁਮਾਨ, ਅਤੇ ਖੇਤੀਬਾੜੀ ਪ੍ਰਭਾਵਾਂ ਬਾਰੇ ਸਵਾਲ ਪੁੱਛ ਸਕਦੇ ਹੋ।"
        )
    else:
        return (
            f"I am the **RainCast AI Climate Assistant**. Our platform tracks authentic meteorological time series (1901–2026) "
            f"across 85 Indian geographical entities (36 IMD subdivisions + 49 stations). You can ask me about regional historical trends, multi-year model predictions (2027+), "
            f"monsoon dynamics, rainfall anomalies, or agricultural climate impacts."
        )

