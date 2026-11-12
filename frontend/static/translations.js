/**
 * RainCast AI - Comprehensive Trilingual Translation Engine
 * Languages: English (en), Hindi (hi), Punjabi (pa)
 */

const TRANSLATIONS = {
    en: {
        // Nav & Common
        app_tagline: "CLIMATE INTELLIGENCE",
        nav_overview: "Overview",
        nav_dashboard: "Dashboard",
        nav_predict: "ML Prediction",
        nav_assistant: "AI Assistant",
        nav_models: "Model Rigor",
        nav_reports: "Reports",
        nav_records: "4,476 Records (1901–2025)",
        nav_launch_model: "Launch Model →",
        lang_select_title: "Change Language",
        lang_english: "English",
        lang_hindi: "हिंदी (Hindi)",
        lang_punjabi: "ਪੰਜਾਬੀ (Punjabi)",
        
        // Footer & Disclaimer
        disclaimer_title: "Official India Meteorological Department (IMD) Scientific Advisory",
        disclaimer_text: "RainCast AI delivers experimental machine learning climate projections based on 125 years of authentic meteorological observations (1901–2025). Forecasts for 2027 and beyond are statistical indicators subject to planetary climate variability and ocean-atmosphere oscillations (ENSO / IOD). Official advisories issued by the India Meteorological Department (IMD) remain the sole statutory authority for administrative, disaster management, and operational decision-making.",
        footer_version: "Version 2.4.0-Enterprise • FastAPI + Tailwind Architecture",
        footer_author: "Developed by Jasmeet Singh Mann",
        footer_subdivisions: "36 Official IMD Meteorological Subdivisions • Authentic Observations (1901–2025)",

        // Home (index.html)
        hero_badge: "RainCast AI Enterprise Suite v2.4.0",
        hero_title_1: "Predict Rainfall. Understand Climate.",
        hero_title_2: "Prepare for Tomorrow.",
        hero_subtitle: "India's advanced meteorological intelligence platform combining 125 continuous years of authentic meteorological observations (1901–2025), robust machine learning ensembles, and Trilingual Generative AI. Engineered for agricultural planning, water resource managers, and climate researchers starting from 2027 onward.",
        btn_launch_ml: "Launch ML Prediction Engine",
        btn_explore_dashboard: "Explore Climate Dashboard",
        kpi_coverage_title: "Coverage",
        kpi_coverage_value: "36 Subdivisions",
        kpi_coverage_sub: "All 36 Official IMD Meteorological Subdivisions",
        kpi_history_title: "Verified History",
        kpi_history_value: "4,476 Records",
        kpi_history_sub: "125 continuous years (1901–2025 Authentic History)",
        kpi_precision_title: "Model Precision",
        kpi_precision_value: "78.0% Test R²",
        kpi_precision_sub: "HistGradientBoosting & Random Forest (68.4% MAE reduction)",
        kpi_horizon_title: "Forecasting Horizon",
        kpi_horizon_value: "2027 – 2035",
        kpi_horizon_sub: "Recursive multi-step with 90% confidence bands",
        modules_heading: "Enterprise Climate Intelligence Modules",
        modules_subheading: "Scientifically validated methodologies designed to deliver transparent, reproducible predictions.",
        module_dash_title: "Climate Analytics Dashboard",
        module_dash_desc: "Examine 125 continuous years of monthly and seasonal rainfall records (1901–2025), 1971–2020 Long Period Average (LPA) baselines, and decadal anomaly shifts across all 36 meteorological subdivisions.",
        module_dash_link: "View Analytics →",
        module_ml_title: "ML Prediction Engine",
        module_ml_desc: "Deploy trained regressors on chronological splits to predict annual rainfall volumes from 2027 through 2035 with statistical uncertainty intervals and official IMD categorization.",
        module_ml_link: "Run Predictions →",
        module_ai_title: "Trilingual GenAI Advisory",
        module_ai_desc: "Powered by Google Gemini 2.5 Flash, generating contextualized agro-meteorological advisories in English, Hindi, and Punjabi directly grounded in statistical forecasts.",
        module_ai_link: "Ask AI Assistant →",

        // Dashboard (dashboard.html)
        dash_meta: "Descriptive Meteorology",
        dash_title: "Climate Analytics Dashboard",
        dash_subtitle: "Explore 125 continuous years of authentic meteorological observations, seasonal distributions, and historical extremes (1901–2025).",
        dash_baseline: "Baseline Normal Period: 1971 – 2020 LPA",
        dash_state_label: "Select State / Territory",
        dash_district_label: "Select District / Subdivision",
        dash_btn_update: "Update Analytics",
        stat_lpa_title: "Normal Annual (LPA)",
        stat_lpa_sub: "1971–2020 Standard Benchmark",
        stat_latest_title: "2025 Observed Rainfall",
        stat_latest_sub: "Latest Verified Historical Observation",
        stat_anomaly_title: "2025 Anomaly Departure",
        stat_rainy_days_title: "Annual Rainy Days",
        stat_rainy_days_sub: "Days with precipitation ≥ 2.5 mm",
        chart_trend_title: "Historical Annual Rainfall Trend (1901–2025)",
        chart_trend_sub: "125-year chronological timeline with 5-year moving average & LPA reference.",
        chart_monthly_title: "Monthly Climatological Profile",
        chart_monthly_sub: "12-month normal seasonal distribution in mm.",
        chart_anomaly_title: "Historical Climatological Anomalies (% Departure from Normal)",
        chart_anomaly_sub: "Cyan bars denote Excess monsoon years; Coral bars denote Deficient drought years.",
        trace_annual: "Annual Rainfall (mm)",
        trace_ma5: "5-Yr Moving Avg",
        trace_lpa: "LPA Normal",
        axis_rainfall: "Rainfall (mm)",
        axis_departure: "Departure (%)",

        // Prediction (predict.html)
        pred_meta: "Machine Learning Inference",
        pred_title: "Annual Rainfall Prediction Engine",
        pred_subtitle: "Deploy validated regressors to forecast future rainfall volumes from 2027 through 2035 with expanding uncertainty intervals.",
        pred_state_label: "State / Territory",
        pred_district_label: "District / Subdivision",
        pred_year_label: "Forecast Horizon Year",
        pred_model_label: "Model Architecture",
        pred_btn_run: "Run Forecast",
        pred_btn_running: "Forecasting...",
        pred_target_label: "ML Forecast Target",
        pred_bounds_title: "Uncertainty Bounds",
        pred_bounds_sub: "90% Statistical Confidence Interval (P05 – P95)",
        pred_lower_label: "Lower Bound (P05)",
        pred_upper_label: "Upper Bound (P95)",
        pred_margin_label: "Model Uncertainty Margin:",
        pred_gauge_title: "IMD Anomaly Gauge",
        pred_gauge_sub: "Relative departure from standard normal",
        pred_gauge_legend: "Deficient (<-19%) • Normal (±19%) • Excess (>+19%)",
        pred_chart_title: "Historical Trajectory & Multi-Horizon Forecast",
        pred_chart_sub: "Recent observed history (2014–2025) connecting to forecast horizon with 90% expanding confidence cone.",
        pred_agri_title: "Agricultural & Crop Suitability Advisory",
        pred_agri_sub: "Agro-Climatic Intelligence",
        pred_kharif_title: "Kharif Season (Monsoon)",
        pred_kharif_sub: "Paddy, Maize, Soybean, Cotton",
        pred_rabi_title: "Rabi Season (Winter)",
        pred_rabi_sub: "Wheat, Mustard, Barley, Gram",
        pred_water_title: "Groundwater Recharge Index",
        pred_water_sub: "Aquifer replenishment potential",
        pred_ai_title: "AI Meteorological Interpretation",
        pred_copy_btn: "Copy",
        pred_copied: "Copied AI Meteorological Explanation to clipboard!",
        pred_loading_ai: "Loading climate interpretation...",
        suit_highly_favorable: "Highly Favorable",
        suit_adequate: "Adequate Moisture",
        suit_high_potential: "High Potential",
        suit_moderate: "Moderate Support",
        suit_irrigation_needed: "Supplemental Irrigation Needed",

        // Assistant (assistant.html)
        asst_meta: "Conversational Intelligence",
        asst_title: "Climate AI Assistant",
        asst_subtitle: "Chat with our climate reasoning model grounded strictly in 126 years of IMD data and model predictions.",
        asst_lang_label: "Response Language:",
        asst_prompts_label: "Quick Prompts:",
        asst_chip_1: "🌦️ What is the 2027 rainfall forecast for Punjab?",
        asst_chip_2: "💧 Which subdivisions face deficient monsoon risk in 2027?",
        asst_chip_3: "📈 How does Coastal Karnataka compare to Vidarbha?",
        asst_chip_4: "🌾 Recommended crops for normal monsoon conditions",
        asst_welcome_title: "Namaste! I am the RainCast Climate Intelligence Assistant.",
        asst_welcome_text: "I have direct access to 125 years of authentic meteorological subdivision records (1901–2025) and machine learning forecasts for 2027–2035. How can I assist your climate research or agricultural planning today?",
        asst_placeholder: "Ask about rainfall predictions, drought risks, crop suitability, or regional trends...",
        asst_send_btn: "Send",
        asst_synthesizing: "Synthesizing meteorological intelligence...",
        asst_you: "You",
        asst_ai: "AI",

        // Models (models.html)
        mod_meta: "Scientific Validation",
        mod_title: "Model Rigor & Benchmark Diagnostics",
        mod_subtitle: "Multi-model benchmark evaluation on chronological splits strictly preventing future data leakage.",
        mod_badge: "Out-of-Sample Test Period: 2016 – 2025 (10 Yrs)",
        mod_table_title: "Machine Learning Model Comparison",
        mod_table_sub: "Evaluated across all 36 IMD Meteorological Subdivisions on strict out-of-sample test records.",
        th_arch: "Model Architecture",
        th_val_mae: "Validation MAE",
        th_val_r2: "Validation R²",
        th_test_mae: "Test MAE (2016–2025)",
        th_test_r2: "Test R² (2016–2025)",
        th_climatology: "vs Climatology",
        th_status: "Status",
        status_best: "Selected Best",
        status_baseline: "Baseline",
        status_high: "High Precision",
        mod_parity_title: "Actual vs Predicted Parity Plot",
        mod_parity_sub: "Out-of-sample test samples clustered tightly along the 45° 1:1 identity line.",
        mod_residuals_title: "Test Residuals Distribution (Errors)",
        mod_residuals_sub: "Unbiased symmetric error curve confirming absence of systematic drift.",
        mod_features_title: "Key Meteorological Feature Drivers",
        mod_features_sub: "Relative contribution of historical lag features, spatial coordinates, and rolling statistics.",

        // Reports (reports.html)
        rep_meta: "Automated Documentation",
        rep_title: "Executive Climate Reports & Data Export",
        rep_subtitle: "Generate IMD-compliant PDF executive summaries and export full verified research datasets.",
        rep_badge: "ReportLab & Pandas Generation Engine",
        rep_pdf_title: "Generate Executive Climate PDF",
        rep_pdf_sub: "Official memorandum containing ML projections, uncertainty bands, and AI advisory.",
        rep_label_state: "State / UT",
        rep_label_district: "District / Sub-Div",
        rep_label_year: "Horizon Year",
        rep_label_model: "Model",
        rep_pdf_btn: "Download Executive PDF",
        rep_csv_title: "Export Cleaned Research Dataset",
        rep_csv_sub: "Complete harmonized meteorological records spanning 1901 to 2025.",
        rep_csv_samples: "Total Samples:",
        rep_csv_samples_val: "4,476 Records",
        rep_csv_coverage: "Geographic Coverage:",
        rep_csv_coverage_val: "36 Official IMD Subdivisions",
        rep_csv_temporal: "Temporal Span:",
        rep_csv_temporal_val: "1901 – 2025 (125 Continuous Years)",
        rep_csv_btn: "Download Cleaned CSV Dataset",
        rep_audit_title: "System Activity & Prediction Audit Log",
        rep_audit_sub: "Real-time transaction history logged in SQLite database (raincast.db).",
        th_time: "Timestamp",
        th_state: "State",
        th_district: "District",
        th_year: "Target Year",
        th_pred: "Predicted (mm)",
        th_anomaly: "Anomaly",
        th_class: "Category",
        th_model: "Model Used"
    },

    hi: {
        // Nav & Common
        app_tagline: "जलवायु बुद्धिमत्ता",
        nav_overview: "अवलोकन",
        nav_dashboard: "डैशबोर्ड",
        nav_predict: "एमएल भविष्यवाणी",
        nav_assistant: "एआई सहायक",
        nav_models: "मॉडल प्रदर्शन",
        nav_reports: "रिपोर्ट्स",
        nav_records: "4,476 रिकॉर्ड (1901–2025)",
        nav_launch_model: "मॉडल शुरू करें →",
        lang_select_title: "भाषा बदलें",
        lang_english: "English",
        lang_hindi: "हिंदी (Hindi)",
        lang_punjabi: "ਪੰਜਾਬੀ (Punjabi)",

        // Footer & Disclaimer
        disclaimer_title: "भारत मौसम विज्ञान विभाग (IMD) आधिकारिक वैज्ञानिक परामर्श",
        disclaimer_text: "रेनकास्ट एआई 125 वर्षों के प्रामाणिक मौसम विज्ञान अवलोकनों (1901–2025) पर आधारित प्रायोगिक मशीन लर्निंग जलवायु अनुमान प्रस्तुत करता है। 2027 और उसके बाद के पूर्वानुमान सांख्यिकीय संकेतक हैं जो ग्रहीय जलवायु परिवर्तनशीलता और महासागर-वायुमंडलीय दोलनों (ईएनएसओ / आईओडी) के अधीन हैं। भारत मौसम विज्ञान विभाग (आईएमडी) द्वारा जारी आधिकारिक सलाह ही प्रशासनिक, आपदा प्रबंधन और परिचालन निर्णय लेने का एकमात्र वैधानिक अधिकार है।",
        footer_version: "संस्करण 2.4.0-एंटरप्राइज • फास्टएपीआई + टेलविंड आर्किटेक्चर",
        footer_author: "जसमीत सिंह मान द्वारा विकसित",
        footer_subdivisions: "36 आधिकारिक आईएमडी उप-मंडल • प्रामाणिक अवलोकन (1901–2025)",

        // Home (index.html)
        hero_badge: "रेनकास्ट एआई एंटरप्राइज सूट v2.4.0",
        hero_title_1: "वर्षा का सटीक पूर्वानुमान। जलवायु को समझें।",
        hero_title_2: "कल के लिए तैयार रहें।",
        hero_subtitle: "भारत का उन्नत मौसम संबंधी खुफिया प्लेटफॉर्म जो भारत मौसम विज्ञान विभाग के 125 निरंतर वर्षों के प्रामाणिक अवलोकन (1901–2025), मजबूत मशीन लर्निंग मॉडल और त्रिभाषी जनरेटिव एआई को जोड़ता है। 2027 से आगे के कृषि नियोजन, जल संसाधन प्रबंधकों और जलवायु शोधकर्ताओं के लिए विशेष रूप से डिज़ाइन किया गया।",
        btn_launch_ml: "एमएल भविष्यवाणी इंजन शुरू करें",
        btn_explore_dashboard: "जलवायु डैशबोर्ड देखें",
        kpi_coverage_title: "भौगोलिक कवरेज",
        kpi_coverage_value: "36 उप-मंडल",
        kpi_coverage_sub: "पूरे भारत में 36 मौसम उप-मंडल + 49 स्टेशन",
        kpi_history_title: "सत्यापित इतिहास",
        kpi_history_value: "4,476 रिकॉर्ड",
        kpi_history_sub: "125 निरंतर वर्ष (1901–2025 प्रामाणिक इतिहास)",
        kpi_precision_title: "मॉडल सटीकता",
        kpi_precision_value: "78.0% टेस्ट R²",
        kpi_precision_sub: "हिस्टग्रेडिएंटबूस्टिंग और रैंडम फॉरेस्ट एन्सेम्बल",
        kpi_horizon_title: "पूर्वानुमान क्षितिज",
        kpi_horizon_value: "2027 – 2035",
        kpi_horizon_sub: "90% विश्वास अंतराल के साथ बहु-वर्षीय अनुमान",
        modules_heading: "एंटरप्राइज जलवायु खुफिया मॉड्यूल",
        modules_subheading: "पारदर्शी, प्रतिलिपि प्रस्तुत करने योग्य पूर्वानुमान प्रदान करने के लिए वैज्ञानिक रूप से मान्य विधियाँ।",
        module_dash_title: "जलवायु विश्लेषण डैशबोर्ड",
        module_dash_desc: "सभी 36 मौसम संबंधी उप-मंडलों में 125 निरंतर वर्षों के प्रामाणिक वर्षा रिकॉर्ड (1901–2025), 1971–2020 लंबी अवधि के औसत (एलपीए) और दशकीय विसंगतियों का विश्लेषण करें।",
        module_dash_link: "विश्लेषण देखें →",
        module_ml_title: "एमएल भविष्यवाणी इंजन",
        module_ml_desc: "सांख्यिकीय अनिश्चितता अंतराल और आधिकारिक आईएमडी वर्गीकरण के साथ 2027 से 2035 तक वार्षिक वर्षा की भविष्यवाणी करने के लिए प्रशिक्षित मॉडल लागू करें।",
        module_ml_link: "भविष्यवाणी करें →",
        module_ai_title: "त्रिभाषी जनरेटिव एआई परामर्श",
        module_ai_desc: "गूगल जेमिनी 2.5 फ्लैश द्वारा संचालित, जो सांख्यिकीय पूर्वानुमानों पर आधारित अंग्रेजी, हिंदी और पंजाबी में प्रासंगिक कृषि-मौसम परामर्श तैयार करता है।",
        module_ai_link: "एआई सहायक से पूछें →",

        // Dashboard (dashboard.html)
        dash_meta: "वर्णनात्मक मौसम विज्ञान",
        dash_title: "जलवायु विश्लेषण डैशबोर्ड",
        dash_subtitle: "125 निरंतर वर्षों के प्रामाणिक मौसम पैटर्न, मौसमी वितरण और चरम सीमाओं (1901–2025) का अन्वेषण करें।",
        dash_baseline: "आधारभूत सामान्य अवधि: 1971 – 2020 एलपीए",
        dash_state_label: "राज्य / केंद्र शासित प्रदेश चुनें",
        dash_district_label: "ज़िला / उप-मंडल चुनें",
        dash_btn_update: "विश्लेषण अपडेट करें",
        stat_lpa_title: "सामान्य वार्षिक वर्षा (एलपीए)",
        stat_lpa_sub: "1971–2020 मानक बेंचमार्क",
        stat_latest_title: "2025 दर्ज वर्षा",
        stat_latest_sub: "अंतिम ऐतिहासिक रिकॉर्ड",
        stat_anomaly_title: "2025 विसंगति प्रस्थान",
        stat_rainy_days_title: "वार्षिक वर्षा दिवस",
        stat_rainy_days_sub: "वर्षा वाले दिन ≥ 2.5 मिमी",
        chart_trend_title: "ऐतिहासिक वार्षिक वर्षा रुझान (1901–2026)",
        chart_trend_sub: "5-वर्षीय चलती औसत और एलपीए संदर्भ के साथ 126-वर्षीय समयरेखा।",
        chart_monthly_title: "मासिक जलवायु प्रोफ़ाइल",
        chart_monthly_sub: "मिमी में 12 महीने का सामान्य मौसमी वितरण।",
        chart_anomaly_title: "ऐतिहासिक जलवायु विसंगतियाँ (सामान्य से % प्रस्थान)",
        chart_anomaly_sub: "सियान बार अतिरिक्त मानसून दर्शाते हैं; कोरल बार कम वर्षा वाले सूखे वर्षों को दर्शाते हैं।",
        trace_annual: "वार्षिक वर्षा (मिमी)",
        trace_ma5: "5-वर्षीय चलती औसत",
        trace_lpa: "एलपीए सामान्य",
        axis_rainfall: "वर्षा (मिमी)",
        axis_departure: "प्रस्थान (%)",

        // Prediction (predict.html)
        pred_meta: "मशीन लर्निंग अनुमान",
        pred_title: "वार्षिक वर्षा भविष्यवाणी इंजन",
        pred_subtitle: "विस्तृत अनिश्चितता अंतराल के साथ 2027 से 2035 तक भविष्य की वर्षा का अनुमान लगाने के लिए मॉडल चलाएं।",
        pred_state_label: "राज्य / केंद्र शासित प्रदेश",
        pred_district_label: "ज़िला / उप-मंडल",
        pred_year_label: "पूर्वानुमान वर्ष",
        pred_model_label: "मॉडल आर्किटेक्चर",
        pred_btn_run: "पूर्वानुमान चलाएं",
        pred_btn_running: "पूर्वानुमान जारी है...",
        pred_target_label: "एमएल पूर्वानुमान लक्ष्य",
        pred_bounds_title: "अनिश्चितता सीमाएं",
        pred_bounds_sub: "90% सांख्यिकीय विश्वास अंतराल (P05 – P95)",
        pred_lower_label: "निचली सीमा (P05)",
        pred_upper_label: "ऊपरी सीमा (P95)",
        pred_margin_label: "मॉडल अनिश्चितता मार्जिन:",
        pred_gauge_title: "आईएमडी विसंगति गेज",
        pred_gauge_sub: "मानक सामान्य से सापेक्ष विचलन",
        pred_gauge_legend: "कम वर्षा (<-19%) • सामान्य (±19%) • अधिक वर्षा (>+19%)",
        pred_chart_title: "ऐतिहासिक प्रक्षेपवक्र और बहु-वर्षीय पूर्वानुमान",
        pred_chart_sub: "90% विश्वास शंकु के साथ पूर्वानुमान क्षितिज से जुड़ता हालिया इतिहास (2015–2026)।",
        pred_agri_title: "कृषि और फसल उपयुक्तता परामर्श",
        pred_agri_sub: "कृषि-जलवायु खुफिया",
        pred_kharif_title: "खरीफ सीजन (मानसून)",
        pred_kharif_sub: "धान, मक्का, सोयाबीन, कपास",
        pred_rabi_title: "रबी सीजन (सर्दियां)",
        pred_rabi_sub: "गेहूं, सरसों, जौ, चना",
        pred_water_title: "भूजल पुनर्भरण सूचकांक",
        pred_water_sub: "जलभृत पुनर्भरण क्षमता",
        pred_ai_title: "एआई मौसम विज्ञान व्याख्या",
        pred_copy_btn: "कॉपी करें",
        pred_copied: "एआई मौसम विज्ञान व्याख्या क्लिपबोर्ड पर कॉपी हो गई!",
        pred_loading_ai: "जलवायु व्याख्या लोड हो रही है...",
        suit_highly_favorable: "अत्यधिक अनुकूल",
        suit_adequate: "पर्याप्त नमी",
        suit_high_potential: "उच्च क्षमता",
        suit_moderate: "मध्यम समर्थन",
        suit_irrigation_needed: "अतिरिक्त सिंचाई आवश्यक",

        // Assistant (assistant.html)
        asst_meta: "संवादात्मक बुद्धिमत्ता",
        asst_title: "जलवायु एआई सहायक",
        asst_subtitle: "126 वर्षों के आईएमडी डेटा और मॉडल भविष्यवाणियों पर आधारित जलवायु मॉडल से बात करें।",
        asst_lang_label: "प्रतिक्रिया भाषा:",
        asst_prompts_label: "त्वरित संकेत:",
        asst_chip_1: "🌦️ पंजाब के लिए 2027 वर्षा का क्या पूर्वानुमान है?",
        asst_chip_2: "💧 2027 में किन उप-मंडलों में कम वर्षा का जोखिम है?",
        asst_chip_3: "📈 तटीय कर्नाटक की तुलना विदर्भ से कैसे की जाती है?",
        asst_chip_4: "🌾 सामान्य मानसून स्थितियों के लिए अनुशंसित फसलें",
        asst_welcome_title: "नमस्ते! मैं रेनकास्ट जलवायु खुफिया सहायक हूँ।",
        asst_welcome_text: "मेरे पास 125 वर्षों के प्रामाणिक मौसम विज्ञान उप-मंडल रिकॉर्ड (1901–2025) और 2027–2035 के मशीन लर्निंग पूर्वानुमानों तक सीधी पहुंच है। आज मैं आपकी योजना या शोध में कैसे सहायता कर सकता हूँ?",
        asst_placeholder: "वर्षा के पूर्वानुमान, सूखे के जोखिम, फसल उपयुक्तता या क्षेत्रीय रुझानों के बारे में पूछें...",
        asst_send_btn: "भेजें",
        asst_synthesizing: "मौसम विज्ञान विश्लेषण तैयार किया जा रहा है...",
        asst_you: "आप",
        asst_ai: "एआई",

        // Models (models.html)
        mod_meta: "वैज्ञानिक सत्यापन",
        mod_title: "मॉडल प्रदर्शन और बेंचमार्क निदान",
        mod_subtitle: "कालानुक्रमिक विभाजन पर बहु-मॉडल मूल्यांकन जो भविष्य के डेटा लीकेज को रोकता है।",
        mod_badge: "आउट-ऑफ-सैंपल परीक्षण अवधि: 2016 – 2025 (10 वर्ष)",
        mod_table_title: "मशीन लर्निंग मॉडल तुलना",
        mod_table_sub: "कड़े आउट-ऑफ-सैंपल परीक्षण रिकॉर्ड पर सभी 36 आधिकारिक आईएमडी मौसम विज्ञान उप-मंडलों में मूल्यांकन किया गया।",
        th_arch: "मॉडल आर्किटेक्चर",
        th_val_mae: "सत्यापन MAE",
        th_val_r2: "सत्यापन R²",
        th_test_mae: "टेस्ट MAE (2017–2026)",
        th_test_r2: "टेस्ट R² (2017–2026)",
        th_climatology: "बनाम जलवायु विज्ञान",
        th_status: "स्थिति",
        status_best: "चयनित सर्वश्रेष्ठ",
        status_baseline: "बेसलाइन",
        status_high: "उच्च परिशुद्धता",
        mod_parity_title: "वास्तविक बनाम अनुमानित समानता प्लॉट",
        mod_parity_sub: "आउट-ऑफ-सैंपल परीक्षण नमूने 45° 1:1 पहचान रेखा के साथ कसकर संरेखित हैं।",
        mod_residuals_title: "टेस्ट अवशिष्ट वितरण (त्रुटियां)",
        mod_residuals_sub: "निष्पक्ष सममित त्रुटि वक्र जो व्यवस्थित बहाव की अनुपस्थिति की पुष्टि करता है।",
        mod_features_title: "प्रमुख मौसम संबंधी विशेषता चालक",
        mod_features_sub: "ऐतिहासिक अंतराल सुविधाओं, स्थानिक निर्देशांक और रोलिंग आंकड़ों का सापेक्ष योगदान।",

        // Reports (reports.html)
        rep_meta: "स्वचालित दस्तावेज़ीकरण",
        rep_title: "कार्यकारी जलवायु रिपोर्ट और डेटा निर्यात",
        rep_subtitle: "आईएमडी-अनुरूप पीडीएफ कार्यकारी सारांश तैयार करें और पूर्ण शोध डेटासेट निर्यात करें।",
        rep_badge: "रिपोर्टलैब और पांडा जनरेशन इंजन",
        rep_pdf_title: "कार्यकारी जलवायु पीडीएफ तैयार करें",
        rep_pdf_sub: "एमएल अनुमान, अनिश्चितता बैंड और एआई सलाह युक्त आधिकारिक ज्ञापन।",
        rep_label_state: "राज्य / केंद्र शासित प्रदेश",
        rep_label_district: "ज़िला / उप-मंडल",
        rep_label_year: "पूर्वानुमान वर्ष",
        rep_label_model: "मॉडल",
        rep_pdf_btn: "कार्यकारी पीडीएफ डाउनलोड करें",
        rep_csv_title: "स्वच्छ अनुसंधान डेटासेट निर्यात करें",
        rep_csv_sub: "1901 से 2025 तक के पूर्ण सामंजस्यपूर्ण मौसम विज्ञान रिकॉर्ड।",
        rep_csv_samples: "कुल नमूने:",
        rep_csv_samples_val: "10,710 रिकॉर्ड",
        rep_csv_coverage: "भौगोलिक कवरेज:",
        rep_csv_coverage_val: "36 आधिकारिक आईएमडी उप-मंडल",
        rep_csv_temporal: "समय सीमा:",
        rep_csv_temporal_val: "1901 – 2025 (125 निरंतर वर्ष)",
        rep_csv_btn: "पूर्ण CSV डेटासेट डाउनलोड करें",
        rep_audit_title: "सिस्टम गतिविधि और ऑडिट लॉग",
        rep_audit_sub: "SQLite डेटाबेस (raincast.db) में वास्तविक समय का लेन-देन इतिहास।",
        th_time: "समय",
        th_state: "राज्य",
        th_district: "ज़िला",
        th_year: "लक्षित वर्ष",
        th_pred: "अनुमानित (मिमी)",
        th_anomaly: "विसंगति",
        th_class: "श्रेणी",
        th_model: "प्रयुक्त मॉडल"
    },

    pa: {
        // Nav & Common
        app_tagline: "ਜਲਵਾਯੂ ਖੁਫੀਆ ਜਾਣਕਾਰੀ",
        nav_overview: "ਸੰਖੇਪ ਜਾਣਕਾਰੀ",
        nav_dashboard: "ਡੈਸ਼ਬੋਰਡ",
        nav_predict: "ਐਮ.ਐਲ ਭਵਿੱਖਬਾਣੀ",
        nav_assistant: "ਏ.ਆਈ ਸਹਾਇਕ",
        nav_models: "ਮਾਡਲ ਪ੍ਰਦਰਸ਼ਨ",
        nav_reports: "ਰਿਪੋਰਟਾਂ",
        nav_records: "4,476 ਰਿਕਾਰਡ (1901–2025)",
        nav_launch_model: "ਮਾਡਲ ਸ਼ੁਰੂ ਕਰੋ →",
        lang_select_title: "ਭਾਸ਼ਾ ਬਦਲੋ",
        lang_english: "English",
        lang_hindi: "हिंदी (Hindi)",
        lang_punjabi: "ਪੰਜਾਬੀ (Punjabi)",

        // Footer & Disclaimer
        disclaimer_title: "ਭਾਰਤ ਮੌਸਮ ਵਿਗਿਆਨ ਵਿਭਾਗ (IMD) ਅਧਿਕਾਰਤ ਵਿਗਿਆਨਕ ਸਲਾਹ",
        disclaimer_text: "ਰੇਨਕਾਸਟ ਏ.ਆਈ 125 ਸਾਲਾਂ ਦੇ ਪ੍ਰਮਾਣਿਕ ਮੌਸਮ ਸੰਬੰਧੀ ਨਿਰੀਖਣਾਂ (1901–2025) ਦੇ ਆਧਾਰ 'ਤੇ ਪ੍ਰਯੋਗਾਤਮਕ ਮਸ਼ੀਨ ਲਰਨਿੰਗ ਜਲਵਾਯੂ ਅਨੁਮਾਨ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ। 2027 ਅਤੇ ਉਸ ਤੋਂ ਬਾਅਦ ਦੇ ਅਨੁਮਾਨ ਅੰਕੜਾਤਮਕ ਸੂਚਕ ਹਨ ਜੋ ਗ੍ਰਹਿ ਜਲਵਾਯੂ ਪਰਿਵਰਤਨਸ਼ੀਲਤਾ ਅਤੇ ਸਮੁੰਦਰੀ-ਵਾਯੂਮੰਡਲ ਉਤਰਾਅ-ਚੜ੍ਹਾਅ (ENSO / IOD) ਦੇ ਅਧੀਨ ਹਨ। ਭਾਰਤ ਮੌਸਮ ਵਿਗਿਆਨ ਵਿਭਾਗ (IMD) ਦੁਆਰਾ ਜਾਰੀ ਅਧਿਕਾਰਤ ਸਲਾਹ ਪ੍ਰਸ਼ਾਸਕੀ, ਆਫ਼ਤ ਪ੍ਰਬੰਧਨ ਅਤੇ ਕਾਰਜਸ਼ੀਲ ਫੈਸਲੇ ਲੈਣ ਲਈ ਇਕਲੌਤਾ ਕਾਨੂੰਨੀ ਅਧਿਕਾਰ ਹੈ।",
        footer_version: "ਵਰਜਨ 2.4.0-ਐਂਟਰਪ੍ਰਾਈਜ਼ • ਫਾਸਟਏਪੀਆਈ + ਟੇਲਵਿੰਡ ਆਰਕੀਟੈਕਚਰ",
        footer_author: "ਜਸਮੀਤ ਸਿੰਘ ਮਾਨ ਦੁਆਰਾ ਵਿਕਸਤ",
        footer_subdivisions: "36 ਅਧਿਕਾਰਤ ਆਈ.ਐਮ.ਡੀ ਉਪ-ਮੰਡਲ • ਪ੍ਰਮਾਣਿਕ ਨਿਰੀਖਣ (1901–2025)",

        // Home (index.html)
        hero_badge: "ਰੇਨਕਾਸਟ ਏ.ਆਈ ਐਂਟਰਪ੍ਰਾਈਜ਼ ਸੂਟ v2.4.0",
        hero_title_1: "ਮੀਂਹ ਦੀ ਸਹੀ ਭਵਿੱਖਬਾਣੀ। ਜਲਵਾਯੂ ਨੂੰ ਸਮਝੋ।",
        hero_title_2: "ਭਲਕ ਲਈ ਤਿਆਰ ਰਹੋ।",
        hero_subtitle: "ਭਾਰਤ ਦਾ ਉੱਨਤ ਮੌਸਮ ਵਿਗਿਆਨਿਕ ਖੁਫੀਆ ਪਲੇਟਫਾਰਮ ਜੋ ਭਾਰਤ ਮੌਸਮ ਵਿਗਿਆਨ ਵਿਭਾਗ ਦੇ 125 ਲਗਾਤਾਰ ਸਾਲਾਂ ਦੇ ਪ੍ਰਮਾਣਿਕ ਰਿਕਾਰਡਾਂ (1901–2025), ਮਜ਼ਬੂਤ ਮਸ਼ੀਨ ਲਰਨਿੰਗ ਮਾਡਲਾਂ ਅਤੇ ਤ੍ਰਿਭਾਸ਼ੀ ਜਨਰੇਟਿਵ ਏ.ਆਈ ਨੂੰ ਜੋੜਦਾ ਹੈ। 2027 ਤੋਂ ਅੱਗੇ ਲਈ ਖੇਤੀਬਾੜੀ ਯੋਜਨਾਬੰਦੀ, ਜਲ ਸਰੋਤ ਪ੍ਰਬੰਧਕਾਂ ਅਤੇ ਜਲਵਾਯੂ ਖੋਜਕਾਰਾਂ ਲਈ ਵਿਸ਼ੇਸ਼ ਤੌਰ 'ਤੇ ਤਿਆਰ ਕੀਤਾ ਗਿਆ।",
        btn_launch_ml: "ਐਮ.ਐਲ ਭਵਿੱਖਬਾਣੀ ਇੰਜਣ ਸ਼ੁਰੂ ਕਰੋ",
        btn_explore_dashboard: "ਜਲਵਾਯੂ ਡੈਸ਼ਬੋਰਡ ਵੇਖੋ",
        kpi_coverage_title: "ਭੂਗੋਲਿਕ ਕਵਰੇਜ",
        kpi_coverage_value: "36 ਉਪ-ਮੰਡਲ",
        kpi_coverage_sub: "ਪੂਰੇ ਭਾਰਤ ਵਿੱਚ 36 ਮੌਸਮ ਉਪ-ਮੰਡਲ + 49 ਸਟੇਸ਼ਨ",
        kpi_history_title: "ਪ੍ਰਮਾਣਿਤ ਇਤਿਹਾਸ",
        kpi_history_value: "4,476 ਰਿਕਾਰਡ",
        kpi_history_sub: "125 ਲਗਾਤਾਰ ਸਾਲ (1901–2025 ਪ੍ਰਮਾਣਿਕ ਇਤਿਹਾਸ)",
        kpi_precision_title: "ਮਾਡਲ ਸ਼ੁੱਧਤਾ",
        kpi_precision_value: "78.0% ਟੈਸਟ R²",
        kpi_precision_sub: "ਹਿਸਟਗਰੇਡੀਐਂਟਬੂਸਟਿੰਗ ਅਤੇ ਰੈਂਡਮ ਫਾਰੈਸਟ ਐਨਸੈਂਬਲ",
        kpi_horizon_title: "ਭਵਿੱਖਬਾਣੀ ਦਾ ਸਮਾਂ",
        kpi_horizon_value: "2027 – 2035",
        kpi_horizon_sub: "90% ਵਿਸ਼ਵਾਸ ਅੰਤਰਾਲ ਨਾਲ ਬਹੁ-ਸਾਲਾ ਅਨੁਮਾਨ",
        modules_heading: "ਐਂਟਰਪ੍ਰਾਈਜ਼ ਜਲਵਾਯੂ ਖੁਫੀਆ ਮੌਡਿਊਲ",
        modules_subheading: "ਪਾਰਦਰਸ਼ੀ ਅਤੇ ਭਰੋਸੇਯੋਗ ਭਵਿੱਖਬਾਣੀਆਂ ਪ੍ਰਦਾਨ ਕਰਨ ਲਈ ਵਿਗਿਆਨਕ ਤੌਰ 'ਤੇ ਪ੍ਰਮਾਣਿਤ ਵਿਧੀਆਂ।",
        module_dash_title: "ਜਲਵਾਯੂ ਵਿਸ਼ਲੇਸ਼ਣ ਡੈਸ਼ਬੋਰਡ",
        module_dash_desc: "ਸਾਰੇ 36 ਮੌਸਮ ਸੰਬੰਧੀ ਉਪ-ਮੰਡਲਾਂ ਵਿੱਚ 126 ਸਾਲਾਂ ਦੇ ਮਾਸਿਕ ਅਤੇ ਮੌਸਮੀ ਮੀਂਹ ਦੇ ਰਿਕਾਰਡ, 1971–2020 ਲੰਮੀ ਮਿਆਦ ਦੀ ਔਸਤ (LPA) ਅਤੇ ਦਹਾਕੇਵਾਰ ਉਤਰਾਅ-ਚੜ੍ਹਾਅ ਦੀ ਜਾਂਚ ਕਰੋ।",
        module_dash_link: "ਵਿਸ਼ਲੇਸ਼ਣ ਵੇਖੋ →",
        module_ml_title: "ਐਮ.ਐਲ ਭਵਿੱਖਬਾਣੀ ਇੰਜਣ",
        module_ml_desc: "ਅੰਕੜਾਤਮਕ ਅਨਿਸ਼ਚਿਤਤਾ ਅੰਤਰਾਲ ਅਤੇ ਅਧਿਕਾਰਤ ਆਈ.ਐਮ.ਡੀ ਵਰਗੀਕਰਨ ਦੇ ਨਾਲ 2027 ਤੋਂ 2035 ਤੱਕ ਸਾਲਾਨਾ ਵਰਖਾ ਦੀ ਭਵਿੱਖਬਾਣੀ ਕਰਨ ਲਈ ਸਿਖਲਾਈ ਪ੍ਰਾਪਤ ਮਾਡਲ ਲਾਗੂ ਕਰੋ।",
        module_ml_link: "ਭਵਿੱਖਬਾਣੀ ਕਰੋ →",
        module_ai_title: "ਤ੍ਰਿਭਾਸ਼ੀ ਜਨਰੇਟਿਵ ਏ.ਆਈ ਸਲਾਹ",
        module_ai_desc: "ਗੂਗਲ ਜੈਮਿਨੀ 2.5 ਫਲੈਸ਼ ਦੁਆਰਾ ਸੰਚਾਲਿਤ, ਜੋ ਅੰਕੜਾਤਮਕ ਭਵਿੱਖਬਾਣੀਆਂ ਦੇ ਆਧਾਰ 'ਤੇ ਅੰਗਰੇਜ਼ੀ, ਹਿੰਦੀ ਅਤੇ ਪੰਜਾਬੀ ਵਿੱਚ ਪ੍ਰਸੰਗਿਕ ਖੇਤੀ-ਮੌਸਮ ਸੰਬੰਧੀ ਸਲਾਹ ਤਿਆਰ ਕਰਦਾ ਹੈ।",
        module_ai_link: "ਏ.ਆਈ ਸਹਾਇਕ ਨੂੰ ਪੁੱਛੋ →",

        // Dashboard (dashboard.html)
        dash_meta: "ਵਰਣਨਾਤਮਕ ਮੌਸਮ ਵਿਗਿਆਨ",
        dash_title: "ਜਲਵਾਯੂ ਵਿਸ਼ਲੇਸ਼ਣ ਡੈਸ਼ਬੋਰਡ",
        dash_subtitle: "125 ਲਗਾਤਾਰ ਸਾਲਾਂ ਦੇ ਪ੍ਰਮਾਣਿਕ ਮੌਸਮ ਦੇ ਨਮੂਨੇ, ਮੌਸਮੀ ਵੰਡ ਅਤੇ ਅਤਿਅੰਤ ਸਥਿਤੀਆਂ (1901–2025) ਦੀ ਪੜਚੋਲ ਕਰੋ।",
        dash_baseline: "ਆਧਾਰਭੂਤ ਆਮ ਮਿਆਦ: 1971 – 2020 ਐੱਲ.ਪੀ.ਏ",
        dash_state_label: "ਸੂਬਾ / ਕੇਂਦਰ ਸ਼ਾਸਤ ਪ੍ਰਦੇਸ਼ ਚੁਣੋ",
        dash_district_label: "ਜ਼ਿਲ੍ਹਾ / ਉਪ-ਮੰਡਲ ਚੁਣੋ",
        dash_btn_update: "ਵਿਸ਼ਲੇਸ਼ਣ ਅੱਪਡੇਟ ਕਰੋ",
        stat_lpa_title: "ਆਮ ਸਾਲਾਨਾ ਵਰਖਾ (LPA)",
        stat_lpa_sub: "1971–2020 ਮਿਆਰੀ ਬੈਂਚਮਾਰਕ",
        stat_latest_title: "2025 ਦਰਜ ਕੀਤੀ ਵਰਖਾ",
        stat_latest_sub: "ਆਖਰੀ ਇਤਿਹਾਸਕ ਰਿਕਾਰਡ",
        stat_anomaly_title: "2025 ਉਤਰਾਅ-ਚੜ੍ਹਾਅ",
        stat_rainy_days_title: "ਸਾਲਾਨਾ ਮੀਂਹ ਦੇ ਦਿਨ",
        stat_rainy_days_sub: "ਵਰਖਾ ਵਾਲੇ ਦਿਨ ≥ 2.5 ਮਿਲੀਮੀਟਰ",
        chart_trend_title: "ਇਤਿਹਾਸਕ ਸਾਲਾਨਾ ਮੀਂਹ ਦਾ ਰੁਝਾਨ (1901–2025)",
        chart_trend_sub: "5-ਸਾਲਾ ਚਲਦੀ ਔਸਤ ਅਤੇ LPA ਹਵਾਲੇ ਦੇ ਨਾਲ 126-ਸਾਲਾ ਸਮਾਂ-ਰੇਖਾ।",
        chart_monthly_title: "ਮਾਸਿਕ ਜਲਵਾਯੂ ਪ੍ਰੋਫਾਈਲ",
        chart_monthly_sub: "ਮਿਲੀਮੀਟਰ ਵਿੱਚ 12 ਮਹੀਨਿਆਂ ਦੀ ਆਮ ਮੌਸਮੀ ਵੰਡ।",
        chart_anomaly_title: "ਇਤਿਹਾਸਕ ਜਲਵਾਯੂ ਉਤਰਾਅ-ਚੜ੍ਹਾਅ (ਆਮ ਨਾਲੋਂ % ਫ਼ਰਕ)",
        chart_anomaly_sub: "ਸਿਆਨ ਬਾਰ ਵਾਧੂ ਮਾਨਸੂਨ ਦਰਸਾਉਂਦੇ ਹਨ; ਕੋਰਲ ਬਾਰ ਘੱਟ ਮੀਂਹ ਵਾਲੇ ਸੋਕੇ ਦੇ ਸਾਲ ਦਰਸਾਉਂਦੇ ਹਨ।",
        trace_annual: "ਸਾਲਾਨਾ ਵਰਖਾ (ਮਿਲੀਮੀਟਰ)",
        trace_ma5: "5-ਸਾਲਾ ਚਲਦੀ ਔਸਤ",
        trace_lpa: "LPA ਆਮ",
        axis_rainfall: "ਮੀਂਹ (ਮਿਲੀਮੀਟਰ)",
        axis_departure: "ਫ਼ਰਕ (%)",

        // Prediction (predict.html)
        pred_meta: "ਮਸ਼ੀਨ ਲਰਨਿੰਗ ਅਨੁਮਾਨ",
        pred_title: "ਸਾਲਾਨਾ ਮੀਂਹ ਭਵਿੱਖਬਾਣੀ ਇੰਜਣ",
        pred_subtitle: "ਵਿਸਤ੍ਰਿਤ ਅਨਿਸ਼ਚਿਤਤਾ ਅੰਤਰਾਲਾਂ ਦੇ ਨਾਲ 2027 ਤੋਂ 2035 ਤੱਕ ਭਵਿੱਖ ਦੀ ਵਰਖਾ ਦਾ ਅਨੁਮਾਨ ਲਗਾਉਣ ਲਈ ਮਾਡਲ ਚਲਾਓ।",
        pred_state_label: "ਸੂਬਾ / ਕੇਂਦਰ ਸ਼ਾਸਤ ਪ੍ਰਦੇਸ਼",
        pred_district_label: "ਜ਼ਿਲ੍ਹਾ / ਉਪ-ਮੰਡਲ",
        pred_year_label: "ਭਵਿੱਖਬਾਣੀ ਦਾ ਸਾਲ",
        pred_model_label: "ਮਾਡਲ ਆਰਕੀਟੈਕਚਰ",
        pred_btn_run: "ਭਵਿੱਖਬਾਣੀ ਚਲਾਓ",
        pred_btn_running: "ਭਵਿੱਖਬਾਣੀ ਜਾਰੀ ਹੈ...",
        pred_target_label: "ਐਮ.ਐਲ ਭਵਿੱਖਬਾਣੀ ਟੀਚਾ",
        pred_bounds_title: "ਅਨਿਸ਼ਚਿਤਤਾ ਸੀਮਾਵਾਂ",
        pred_bounds_sub: "90% ਅੰਕੜਾਤਮਕ ਵਿਸ਼ਵਾਸ ਅੰਤਰਾਲ (P05 – P95)",
        pred_lower_label: "ਹੇਠਲੀ ਸੀਮਾ (P05)",
        pred_upper_label: "ਉਪਰਲੀ ਸੀਮਾ (P95)",
        pred_margin_label: "ਮਾਡਲ ਅਨਿਸ਼ਚਿਤਤਾ ਮਾਰਜਿਨ:",
        pred_gauge_title: "ਆਈ.ਐਮ.ਡੀ ਉਤਰਾਅ-ਚੜ੍ਹਾਅ ਗੇਜ",
        pred_gauge_sub: "ਮਿਆਰੀ ਔਸਤ ਤੋਂ ਸਾਪੇਖਿਕ ਫ਼ਰਕ",
        pred_gauge_legend: "ਘੱਟ ਮੀਂਹ (<-19%) • ਆਮ (±19%) • ਵੱਧ ਮੀਂਹ (>+19%)",
        pred_chart_title: "ਇਤਿਹਾਸਕ ਰੁਝਾਨ ਅਤੇ ਬਹੁ-ਸਾਲਾ ਭਵਿੱਖਬਾਣੀ",
        pred_chart_sub: "90% ਵਿਸਤ੍ਰਿਤ ਵਿਸ਼ਵਾਸ ਕੋਨ ਦੇ ਨਾਲ ਭਵਿੱਖਬਾਣੀ ਨਾਲ ਜੁੜਦਾ ਹਾਲੀਆ ਇਤਿਹਾਸ (2014–2025)।",
        pred_agri_title: "ਖੇਤੀਬਾੜੀ ਅਤੇ ਫਸਲ ਅਨੁਕੂਲਤਾ ਸਲਾਹ",
        pred_agri_sub: "ਖੇਤੀ-ਜਲਵਾਯੂ ਖੁਫੀਆ",
        pred_kharif_title: "ਸਾਉਣੀ ਸੀਜ਼ਨ (ਮਾਨਸੂਨ)",
        pred_kharif_sub: "ਝੋਨਾ, ਮੱਕੀ, ਸੋਇਆਬੀਨ, ਨਰਮਾ",
        pred_rabi_title: "ਹਾੜ੍ਹੀ ਸੀਜ਼ਨ (ਸਰਦੀਆਂ)",
        pred_rabi_sub: "ਕਣਕ, ਸਰ੍ਹੋਂ, ਜੌਂ, ਛੋਲੇ",
        pred_water_title: "ਧਰਤੀ ਹੇਠਲੇ ਪਾਣੀ ਦਾ ਰੀਚਾਰਜ ਸੂਚਕਾਂਕ",
        pred_water_sub: "ਜਲ-ਭੰਡਾਰ ਰੀਚਾਰਜ ਸਮਰੱਥਾ",
        pred_ai_title: "ਏ.ਆਈ ਮੌਸਮ ਵਿਗਿਆਨ ਵਿਆਖਿਆ",
        pred_copy_btn: "ਕਾਪੀ ਕਰੋ",
        pred_copied: "ਏ.ਆਈ ਮੌਸਮ ਵਿਗਿਆਨ ਵਿਆਖਿਆ ਕਲਿੱਪਬੋਰਡ 'ਤੇ ਕਾਪੀ ਹੋ ਗਈ!",
        pred_loading_ai: "ਜਲਵਾਯੂ ਵਿਆਖਿਆ ਲੋਡ ਹੋ ਰਹੀ ਹੈ...",
        suit_highly_favorable: "ਬਹੁਤ ਅਨੁਕੂਲ",
        suit_adequate: "ਲੋੜੀਂਦੀ ਨਮੀ",
        suit_high_potential: "ਉੱਚ ਸਮਰੱਥਾ",
        suit_moderate: "ਦਰਮਿਆਨਾ ਸਮਰਥਨ",
        suit_irrigation_needed: "ਵਾਧੂ ਸਿੰਚਾਈ ਦੀ ਲੋੜ",

        // Assistant (assistant.html)
        asst_meta: "ਗੱਲਬਾਤ ਆਧਾਰਿਤ ਖੁਫੀਆ",
        asst_title: "ਜਲਵਾਯੂ ਏ.ਆਈ ਸਹਾਇਕ",
        asst_subtitle: "126 ਸਾਲਾਂ ਦੇ ਆਈ.ਐਮ.ਡੀ ਡੇਟਾ ਅਤੇ ਮਾਡਲ ਭਵਿੱਖਬਾਣੀਆਂ 'ਤੇ ਆਧਾਰਿਤ ਜਲਵਾਯੂ ਮਾਡਲ ਨਾਲ ਗੱਲ ਕਰੋ।",
        asst_lang_label: "ਜਵਾਬ ਦੀ ਭਾਸ਼ਾ:",
        asst_prompts_label: "ਤੁਰੰਤ ਸੁਝਾਅ:",
        asst_chip_1: "🌦️ ਪੰਜਾਬ ਲਈ 2027 ਦੇ ਮੀਂਹ ਦੀ ਕੀ ਭਵਿੱਖਬਾਣੀ ਹੈ?",
        asst_chip_2: "💧 2027 ਵਿੱਚ ਕਿਹੜੇ ਉਪ-ਮੰਡਲਾਂ ਵਿੱਚ ਘੱਟ ਮੀਂਹ ਦਾ ਖਤਰਾ ਹੈ?",
        asst_chip_3: "📈 ਤੱਟਵਰਤੀ ਕਰਨਾਟਕ ਦੀ ਤੁਲਨਾ ਵਿਦਰਭ ਨਾਲ ਕਿਵੇਂ ਕੀਤੀ ਜਾਂਦੀ ਹੈ?",
        asst_chip_4: "🌾 ਆਮ ਮਾਨਸੂਨ ਹਾਲਤਾਂ ਲਈ ਸਿਫਾਰਸ਼ ਕੀਤੀਆਂ ਫਸਲਾਂ",
        asst_welcome_title: "ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ! ਮੈਂ ਰੇਨਕਾਸਟ ਜਲਵਾਯੂ ਖੁਫੀਆ ਸਹਾਇਕ ਹਾਂ।",
        asst_welcome_text: "ਮੇਰੇ ਕੋਲ 125 ਸਾਲਾਂ ਦੇ ਪ੍ਰਮਾਣਿਕ ਮੌਸਮ ਸੰਬੰਧੀ ਉਪ-ਮੰਡਲ ਰਿਕਾਰਡਾਂ (1901–2025) ਅਤੇ 2027–2035 ਲਈ ਮਸ਼ੀਨ ਲਰਨਿੰਗ ਭਵਿੱਖਬਾਣੀਆਂ ਤੱਕ ਸਿੱਧੀ ਪਹੁੰਚ ਹੈ। ਅੱਜ ਮੈਂ ਤੁਹਾਡੀ ਖੋਜ ਜਾਂ ਖੇਤੀਬਾੜੀ ਯੋਜਨਾ ਵਿੱਚ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ?",
        asst_placeholder: "ਮੀਂਹ ਦੀ ਭਵਿੱਖਬਾਣੀ, ਸੋਕੇ ਦੇ ਜੋਖਮ, ਫਸਲ ਅਨੁਕੂਲਤਾ ਜਾਂ ਖੇਤਰੀ ਰੁਝਾਨਾਂ ਬਾਰੇ ਪੁੱਛੋ...",
        asst_send_btn: "ਭੇਜੋ",
        asst_synthesizing: "ਮੌਸਮ ਵਿਗਿਆਨਿਕ ਵਿਸ਼ਲੇਸ਼ਣ ਤਿਆਰ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ...",
        asst_you: "ਤੁਸੀਂ",
        asst_ai: "ਏ.ਆਈ",

        // Models (models.html)
        mod_meta: "ਵਿਗਿਆਨਕ ਪ੍ਰਮਾਣੀਕਰਨ",
        mod_title: "ਮਾਡਲ ਪ੍ਰਦਰਸ਼ਨ ਅਤੇ ਬੈਂਚਮਾਰਕ ਨਿਦਾਨ",
        mod_subtitle: "ਕਾਲਕ੍ਰਮ ਅਨੁਸਾਰ ਵੰਡ 'ਤੇ ਬਹੁ-ਮਾਡਲ ਮੁਲਾਂਕਣ ਜੋ ਭਵਿੱਖ ਦੇ ਡੇਟਾ ਲੀਕ ਨੂੰ ਰੋਕਦਾ ਹੈ।",
        mod_badge: "ਨਮੂਨੇ ਤੋਂ ਬਾਹਰ ਟੈਸਟ ਮਿਆਦ: 2016 – 2025 (10 ਸਾਲ)",
        mod_table_title: "ਮਸ਼ੀਨ ਲਰਨਿੰਗ ਮਾਡਲ ਤੁਲਨਾ",
        mod_table_sub: "ਸਖ਼ਤ ਟੈਸਟ ਰਿਕਾਰਡਾਂ 'ਤੇ ਸਾਰੇ 36 ਅਧਿਕਾਰਤ ਆਈ.ਐਮ.ਡੀ ਮੌਸਮ ਵਿਗਿਆਨਿਕ ਉਪ-ਮੰਡਲਾਂ ਵਿੱਚ ਮੁਲਾਂਕਣ ਕੀਤਾ ਗਿਆ।",
        th_arch: "ਮਾਡਲ ਆਰਕੀਟੈਕਚਰ",
        th_val_mae: "ਪੜਤਾਲ MAE",
        th_val_r2: "ਪੜਤਾਲ R²",
        th_test_mae: "ਟੈਸਟ MAE (2017–2026)",
        th_test_r2: "ਟੈਸਟ R² (2017–2026)",
        th_climatology: "ਬਨਾਮ ਜਲਵਾਯੂ ਵਿਗਿਆਨ",
        th_status: "ਸਥਿਤੀ",
        status_best: "ਚੁਣਿਆ ਗਿਆ ਸਭ ਤੋਂ ਵਧੀਆ",
        status_baseline: "ਬੇਸਲਾਈਨ",
        status_high: "ਉੱਚ ਸ਼ੁੱਧਤਾ",
        mod_parity_title: "ਅਸਲ ਬਨਾਮ ਭਵਿੱਖਬਾਣੀ ਸਮਾਨਤਾ ਪਲਾਟ",
        mod_parity_sub: "ਟੈਸਟ ਨਮੂਨੇ 45° 1:1 ਪਛਾਣ ਰੇਖਾ ਦੇ ਨਾਲ ਕੱਸ ਕੇ ਜੁੜੇ ਹੋਏ ਹਨ।",
        mod_residuals_title: "ਟੈਸਟ ਬਕਾਇਆ ਵੰਡ (ਗਲਤੀਆਂ)",
        mod_residuals_sub: "ਨਿਰਪੱਖ ਗਲਤੀ ਵਕਰ ਜੋ ਕਿਸੇ ਵੀ ਭਟਕਾਅ ਦੀ ਅਣਹੋਂਦ ਦੀ ਪੁਸ਼ਟੀ ਕਰਦਾ ਹੈ।",
        mod_features_title: "ਮੁੱਖ ਮੌਸਮ ਵਿਗਿਆਨਿਕ ਵਿਸ਼ੇਸ਼ਤਾ ਚਾਲਕ",
        mod_features_sub: "ਇਤਿਹਾਸਕ ਪਛੜ ਵਿਸ਼ੇਸ਼ਤਾਵਾਂ, ਭੂਗੋਲਿਕ ਨਿਰਦੇਸ਼ਾਂਕ ਅਤੇ ਰੋਲਿੰਗ ਅੰਕੜਿਆਂ ਦਾ ਸਾਪੇਖਿਕ ਯੋਗਦਾਨ।",

        // Reports (reports.html)
        rep_meta: "ਸਵੈਚਾਲਿਤ ਦਸਤਾਵੇਜ਼ੀਕਰਨ",
        rep_title: "ਕਾਰਜਕਾਰੀ ਜਲਵਾਯੂ ਰਿਪੋਰਟਾਂ ਅਤੇ ਡੇਟਾ ਨਿਰਯਾਤ",
        rep_subtitle: "ਆਈ.ਐਮ.ਡੀ-ਅਨੁਕੂਲ ਪੀਡੀਐਫ ਸਾਰ ਤਿਆਰ ਕਰੋ ਅਤੇ ਪੂਰਾ ਖੋਜ ਡੇਟਾਸੈੱਟ ਨਿਰਯਾਤ ਕਰੋ।",
        rep_badge: "ਰਿਪੋਰਟਲੈਬ ਅਤੇ ਪਾਂਡਾਸ ਜਨਰੇਸ਼ਨ ਇੰਜਣ",
        rep_pdf_title: "ਕਾਰਜਕਾਰੀ ਜਲਵਾਯੂ ਪੀਡੀਐਫ ਤਿਆਰ ਕਰੋ",
        rep_pdf_sub: "ਐਮ.ਐਲ ਅਨੁਮਾਨ, ਅਨਿਸ਼ਚਿਤਤਾ ਬੈਂਡ ਅਤੇ ਏ.ਆਈ ਸਲਾਹ ਵਾਲਾ ਅਧਿਕਾਰਤ ਮੈਮੋਰੰਡਮ।",
        rep_label_state: "ਸੂਬਾ / ਕੇਂਦਰ ਸ਼ਾਸਤ ਪ੍ਰਦੇਸ਼",
        rep_label_district: "ਜ਼ਿਲ੍ਹਾ / ਉਪ-ਮੰਡਲ",
        rep_label_year: "ਭਵਿੱਖਬਾਣੀ ਦਾ ਸਾਲ",
        rep_label_model: "ਮਾਡਲ",
        rep_pdf_btn: "ਕਾਰਜਕਾਰੀ ਪੀਡੀਐਫ ਡਾਊਨਲੋਡ ਕਰੋ",
        rep_csv_title: "ਸਾਫ਼ ਕੀਤਾ ਖੋਜ ਡੇਟਾਸੈੱਟ ਨਿਰਯਾਤ ਕਰੋ",
        rep_csv_sub: "1901 ਤੋਂ 2025 ਤੱਕ ਦੇ ਮੁਕੰਮਲ ਮੌਸਮ ਸੰਬੰਧੀ ਰਿਕਾਰਡ।",
        rep_csv_samples: "ਕੁੱਲ ਨਮੂਨੇ:",
        rep_csv_samples_val: "10,710 ਰਿਕਾਰਡ",
        rep_csv_coverage: "ਭੂਗੋਲਿਕ ਕਵਰੇਜ:",
        rep_csv_coverage_val: "36 ਅਧਿਕਾਰਤ ਆਈ.ਐਮ.ਡੀ ਉਪ-ਮੰਡਲ",
        rep_csv_temporal: "ਸਮਾਂ ਸੀਮਾ:",
        rep_csv_temporal_val: "1901 – 2025 (125 ਲਗਾਤਾਰ ਸਾਲ)",
        rep_csv_btn: "ਪੂਰਾ CSV ਡੇਟਾਸੈੱਟ ਡਾਊਨਲੋਡ ਕਰੋ",
        rep_audit_title: "ਸਿਸਟਮ ਗਤੀਵਿਧੀ ਅਤੇ ਆਡਿਟ ਲੌਗ",
        rep_audit_sub: "SQLite ਡੇਟਾਬੇਸ (raincast.db) ਵਿੱਚ ਰੀਅਲ-ਟਾਈਮ ਲੌਗ ਕੀਤਾ ਇਤਿਹਾਸ।",
        th_time: "ਸਮਾਂ",
        th_state: "ਸੂਬਾ",
        th_district: "ਜ਼ਿਲ੍ਹਾ",
        th_year: "ਟੀਚਾ ਸਾਲ",
        th_pred: "ਅਨੁਮਾਨਿਤ (ਮਿਲੀਮੀਟਰ)",
        th_anomaly: "ਫ਼ਰਕ",
        th_class: "ਸ਼੍ਰੇਣੀ",
        th_model: "ਵਰਤਿਆ ਗਿਆ ਮਾਡਲ"
    }
};

class I18nManager {
    constructor() {
        this.currentLang = localStorage.getItem('raincast_lang') || 'en';
        if (!['en', 'hi', 'pa'].includes(this.currentLang)) {
            this.currentLang = 'en';
        }
    }

    t(key) {
        const langData = TRANSLATIONS[this.currentLang] || TRANSLATIONS['en'];
        return langData[key] || TRANSLATIONS['en'][key] || key;
    }

    setLanguage(lang) {
        if (!['en', 'hi', 'pa'].includes(lang)) return;
        this.currentLang = lang;
        localStorage.setItem('raincast_lang', lang);
        document.documentElement.lang = lang;

        this.applyTranslations();
        this.updateButtons();

        // Dispatch custom event for page scripts (charts, etc.)
        window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }));
    }

    applyTranslations() {
        // Elements with data-i18n
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            const translation = this.t(key);
            if (translation) {
                el.textContent = translation;
            }
        });

        // Elements with data-i18n-html
        document.querySelectorAll('[data-i18n-html]').forEach(el => {
            const key = el.getAttribute('data-i18n-html');
            const translation = this.t(key);
            if (translation) {
                el.innerHTML = translation;
            }
        });

        // Elements with data-i18n-placeholder
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            const translation = this.t(key);
            if (translation) {
                el.setAttribute('placeholder', translation);
            }
        });

        // Elements with data-i18n-title
        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.getAttribute('data-i18n-title');
            const translation = this.t(key);
            if (translation) {
                el.setAttribute('title', translation);
            }
        });
    }

    updateButtons() {
        // Update any language button label/active indicators
        const displayMap = {
            en: 'English',
            hi: 'हिंदी',
            pa: 'ਪੰਜਾਬੀ'
        };
        const currentLabel = displayMap[this.currentLang] || 'English';
        
        const labelEl = document.getElementById('currentLangLabel');
        if (labelEl) labelEl.textContent = currentLabel;
        const mobileLabelEl = document.getElementById('currentLangLabelMobile');
        if (mobileLabelEl) mobileLabelEl.textContent = currentLabel;

        // Active class on dropdown items
        ['en', 'hi', 'pa'].forEach(l => {
            document.querySelectorAll(`.lang-opt-${l}`).forEach(btn => {
                if (l === this.currentLang) {
                    btn.classList.add('text-cyan-400', 'font-bold', 'bg-navy-800');
                    btn.classList.remove('text-gray-300');
                } else {
                    btn.classList.remove('text-cyan-400', 'font-bold', 'bg-navy-800');
                    btn.classList.add('text-gray-300');
                }
            });
        });
    }
}

// Global instance
window.i18n = new I18nManager();

document.addEventListener('DOMContentLoaded', () => {
    window.i18n.applyTranslations();
    window.i18n.updateButtons();
});

