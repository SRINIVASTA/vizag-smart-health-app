# app.py — BLOCK 1: CORE INITIALIZATION & TRANSLATION MATRICES
import streamlit as st
import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt
import src.predictive_engine as engine

# 🛠️ EMBEDDED AUTOMATIC DATABASE CREATION ENGINE
def build_native_database_instance():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/smart_health.db")
    cursor = conn.cursor()
    with open("data/schema.sql", "r", encoding="utf-8") as schema_file:
        cursor.executescript(schema_file.read())
    cursor.execute("DELETE FROM system_audit_logs;")
    cursor.execute("DELETE FROM patient_prescriptions;")
    cursor.execute("DELETE FROM patient_triage_queue;")
    cursor.execute("DELETE FROM node_operations;")
    cursor.execute("DELETE FROM inventory;")
    cursor.execute("DELETE FROM pharmacists;")
    cursor.execute("DELETE FROM asha_workers;")
    cursor.execute("DELETE FROM doctors;")
    cursor.execute("DELETE FROM administrative_hierarchy;")

    facilities = [
        ('IN-AP-VSP-PND', 'Tehsil', 'Pendurthi CHC Hub', 'Andhra Pradesh', 'Visakhapatnam', 17.8303, 83.1979),
        ('IN-AP-VSP-BHM', 'Tehsil', 'Bheemili Hospital Spoke', 'Andhra Pradesh', 'Visakhapatnam', 17.8894, 83.4452),
        ('IN-AP-VZM-GJN', 'Tehsil', 'Gajapathinagaram PHC', 'Andhra Pradesh', 'Vizianagaram', 18.2789, 83.3323),
        ('IN-AP-SKL-RUR', 'Tehsil', 'Srikakulam Rural Center', 'Andhra Pradesh', 'Srikakulam', 18.3164, 83.8943),
        ('IN-AP-SKL-PLS', 'Tehsil', 'Palasa Super-Spec Spoke', 'Andhra Pradesh', 'Srikakulam', 18.7725, 84.4172)
    ]
    cursor.executemany("INSERT INTO administrative_hierarchy VALUES (?, ?, ?, ?, ?, ?, ?)", facilities)

    doctors = [
        ('DOC-VSP-001', 'IN-AP-VSP-PND', 'Dr. S. Srinivasa Rao', 'General Medicine', 1),
        ('DOC-VSP-002', 'IN-AP-VSP-PND', 'Dr. K. Anuradha', 'Pediatrics', 1),
        ('DOC-VSP-003', 'IN-AP-VSP-BHM', 'Dr. A. Lakshmi Prasanna', 'General Medicine', 1), 
        ('DOC-VZM-001', 'IN-AP-VZM-GJN', 'Dr. Ch. Koteswara Rao', 'General Medicine', 1),
        ('DOC-SKL-001', 'IN-AP-SKL-RUR', 'Dr. K. Venkataswamy', 'General Medicine', 1)
    ]
    cursor.executemany("INSERT INTO doctors VALUES (?, ?, ?, ?, ?)", doctors)

    ashas = [
        ('ASHA-VSP-001', 'IN-AP-VSP-PND', 'asha_worker', 'Smt. Lakshmi', 'Pendurthi Village A'),
        ('ASHA-VZM-001', 'IN-AP-VZM-GJN', 'asha_gajapathinagaram', 'Smt. Saraswathi', 'Gajapathinagaram West'),
        ('ASHA-SKL-001', 'IN-AP-SKL-RUR', 'asha_srikakulam', 'Smt. Parvathi', 'Srikakulam Outer Ring')
    ]
    cursor.executemany("INSERT INTO asha_workers VALUES (?, ?, ?, ?, ?)", ashas)

    pharmacists = [
        ('PHR-VSP-001', 'IN-AP-VSP-PND', 'pharma_person', 'Sri K. Venkatesh'),
        ('PHR-VZM-001', 'IN-AP-VZM-GJN', 'pharma_gajapathinagaram', 'Sri L. Narayana'),
        ('PHR-SKL-001', 'IN-AP-SKL-RUR', 'pharma_srikakulam_rur', 'Sri P. Satyam')
    ]
    cursor.executemany("INSERT INTO pharmacists VALUES (?, ?, ?, ?)", pharmacists)

    inventory_data = [
        ('IN-AP-VSP-PND', 'Paracetamol Tabs', 450, 5000, 450.0),    
        ('IN-AP-VSP-BHM', 'Paracetamol Tabs', 18000, 4000, 180.0),  
        ('IN-AP-VZM-GJN', 'Paracetamol Tabs', 5500, 3000, 210.0),
        ('IN-AP-SKL-RUR', 'Anti-Venom Vials', 3, 40, 6.5),          
        ('IN-AP-SKL-PLS', 'Anti-Venom Vials', 150, 30, 2.0)         
    ]
    cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", inventory_data)

    node_ops = [
        ('IN-AP-VSP-PND', 50, 44, 0.88),  
        ('IN-AP-VSP-BHM', 30, 10, 0.12),
        ('IN-AP-VZM-GJN', 20, 12, 0.38),
        ('IN-AP-SKL-RUR', 25, 22, 0.79),  
        ('IN-AP-SKL-PLS', 40, 15, 0.21)
    ]
    cursor.executemany("INSERT INTO node_operations VALUES (?, ?, ?, ?)", node_ops)
    conn.commit()
    conn.close()

if not os.path.exists("data/smart_health.db") or os.path.getsize("data/smart_health.db") == 0:
    build_native_database_instance()

st.set_page_config(layout="wide", page_title="Bharat Health AI Command")

# 🌍 COMPREHENSIVE LOCALIZATION STRING MATRIX
LANG_PACK = {
    "English": {
        "title": "🌐 Bharat Health AI: Multi-Role Operations Matrix", "subtitle": "Track 3: Smart Health Dashboard — End-to-End Workflow Verification",
        "lock_msg": "🔒 Please select a valid role and enter its unique password in the left sidebar to unlock records.",
        "role_label": "Select Your System Role", "pass_label": "Enter Unique Password", "lang_label": "🌐 Change UI Language",
        "stock_title": "AI Supply Depletion & Stock Grid Monitor", "risk_title": "Outbreak Risk Multiplier",
        "asha_title": "Frontline Patient Intake Registration Matrix", "pt_phone": "Patient Contact Mobile Number", "symptoms": "Logged Symptoms Description",
        "sys_bp": "Vitals: Systolic Blood Pressure (mmHg)", "dia_bp": "Vitals: Diastolic Blood Pressure (mmHg)", "consult_mode": "Requested Consultation Mode",
        "submit_intake": "📥 Push Triage Metrics to Clinical Queue", "doc_title": "🩺 Medical Practitioner Evaluation Pool", "select_pt": "Select Active Patient Token to Treat",
        "prescribe": "Prescribe Necessary Medical Formulation", "dosage": "Dosage Regulation Instructions", "sign_rx": "✍️ Authorize and Sign Digital Prescription",
        "pharma_title": "💊 Pharmacy Dispensation Desk & Aero-Logistics Network", "select_rx": "Select Prescription ID to Dispense", "logistics_path": "Fulfillment Logistics Path",
        "dispatch": "🚀 Finalize Dispensation Order", "ai_title": "🤖 Gemini 2.5 Flash Autonomous Intervention Planner", "run_ai": "✨ Run AI Demand Analytics",
        "btn_login": "🔑 Authenticate & Login", "btn_logout": "🚪 Secure Session Logout"
    },
    "తెలుగు (Telugu)": {
        "title": "🌐 భరత్ హెల్త్ AI: మల్టీ-రోల్ ఆపరేషన్ส์ మేట్రిక్స్", "subtitle": "ట్రాక్ 3: స్మార్ట్ హెల్త్ డ్యాష్‌బోర్డ్ — ఎండ్-టు-ఎండ్ వర్క్‌ఫ్లో వెరిఫికేషన్",
        "lock_msg": "🔒 రికార్డులను అన్‌లాక్ చేయడానికి దయచేసి ఎడమ సైడ్‌బార్‌లో చెల్లుబాటు అయ్యే పాత్రను ఎంచుకుని, దాని ప్రత్యేక పాస్‌వర్డ్‌ను నమోదు చేయండి.",
        "role_label": "మీ సిస్టమ్ పాత్రను ఎంచుకోండి", "pass_label": "ప్రత్యేక పాస్‌వర్డ్ నమోదు చేయండి", "lang_label": "🌐 భాషను మార్చండి",
        "stock_title": "AI సప్లై క్షీణత & స్టాక్ గ్రిడ్ మానిటర్", "risk_title": "వ్యాధి వ్యాప్తి ప్రమాద గుణకం",
        "asha_title": "ఆశా వర్కర్ రోగి రిजिస్ట్రేషన్ ఫారమ్", "pt_phone": "రోగి సంప్రదింపు మొబైల్ నంబర్", "symptoms": "రోగి లక్షణాల వివरण",
        "sys_bp": "సిస్టోలిక్ రక్తపోటు (Systolic BP)", "dia_bp": "డయాస్టోలిక్ రక్తపోటు (Diastolic BP)", "consult_mode": "అవసరమైన సంప్రదింపు విధానం",
        "submit_intake": "📥 రోగి వివరాలను క్లినికల్ క్యూకు పంపండి", "doc_title": "🩺 వైద్యుల మూల్యాంకన పోర్టల్", "select_pt": "చిकीత్స చేయడానికి రోగి టోకెన్‌ను ఎంచుకోండి",
        "prescribe": "అవసరమైన మందులను సూచించండి", "dosage": "మందుల వాడకం సూచనలు", "sign_rx": "✍️ డిజిటల్ ప్రిస్క్రిప్షన్‌ను ఆమోదించండి",
        "pharma_title": "💊 ఫార్మసీ పంపిణీ డెస్క్ & డ్రోన్ లాజిస్టిక్స్", "select_rx": "పంపిణీ చేయడానికి ప్రిస్క్రిప్షన్ IDని ఎంచుకోండి", "logistics_path": "డెలివరీ లాజిస్టిక్స్ మార్గం",
        "dispatch": "🚀 ఆర్డర్ పంపిణీని ఖరారు చేయండి", "ai_title": "🤖 జెమిని AI ఆపరేటివ్ ఇంటర్వెन्शन ప్లానర్", "run_ai": "✨ AI డిమాండ్ విశ్लेషణను రన్ చేయండి",
        "btn_login": "🔑 లాగిన్ అవ్వండి", "btn_logout": "🚪 సిస్టమ్ నుండి లాగ్ అవుట్ అవ్వండి"
    },
    "हिन्दी (Hindi)": {
        "title": "🌐 भारत हेल्थ एआई: मल्टी-रोल ऑपरेशंस मैट्रिक्स", "subtitle": "ट्रैक 3: स्मार्ट हेल्थ डैशबोर्ड — एंड-टु-एंड वर्कफ़्लो सत्यापन",
        "lock_msg": "🔒 रिकॉर्ड अनलॉक करने के लिए कृपया बाएं साइडबार में एक वैध भूमिका चुनें और उसका अद्वितीय पासवर्ड दर्ज करें।",
        "role_label": "अपनी सिस्टम भूमिका चुनें", "pass_label": "अद्वितीय कूटशब्द (Password) दर्ज करें", "lang_label": "🌐 यूआई भाषा बदलें",
        "stock_title": "एआई आपूर्ति कमी और स्टॉक ग्रिड मॉनिटर", "risk_title": "प्रकोप जोखिम गुणक",
        "asha_title": "आशा कार्यकर्ता रोगी पंजीकरण फॉर्म", "pt_phone": "रोगी का मोबाइल नंबर", "symptoms": "रोगी के लक्षणों का विवरण",
        "sys_bp": "सिस्टोलिक रक्तचाप (Systolic BP)", "dia_bp": "डायस्टोलिक रक्तचाप (Diastolic BP)", "consult_mode": "परामर्श का अनुरोधित तरीका",
        "submit_intake": "📥 रोगी के विवरण क्लिनिकल कतार में भेजें", "doc_title": "🩺 चिकित्सक मूल्यांकन पोर्टल", "select_pt": "उपचार के लिए सक्रिय रोगी टोकन चुनें",
        "prescribe": "आवश्यक दवा फॉर्मूलेशन लिखें", "dosage": "दवा की खुराक के निर्देश", "sign_rx": "✍️ डिजिटल नुस्खा (Prescription) प्रमाणित करें",
        "pharma_title": "💊 फार्मेसी वितरण डेस्क और ड्रोन रसद (Logistics)", "select_rx": "वितरण के लिए प्रेस्क्रिप्शन आईडी चुनें", "logistics_path": "वितरण रसद पथ",
        "dispatch": "🚀 वितरण आदेश अंतिम रूप दें", "ai_title": "🤖 जेमिनी एआई मांग और हस्तक्षेप योजनाकार", "run_ai": "✨ एआई मांग विश्लेषण चलाएं",
        "btn_login": "🔑 लॉग इन करें", "btn_logout": "🚪 सुरक्षित सत्र लॉगआउट"
    }
}
# app.py — BLOCK 2: UNIQUE PASSWORDS ACCESS ENGINE & GRAPHICS
st.sidebar.header("🌐 Localization Setup")
ui_lang = st.sidebar.selectbox("Select Display Language", ["English", "తెలుగు (Telugu)", "हिन्दी (Hindi)"])

# 🌟 FIXES THE NameError: Forces L to mount safely into namespace context memory fields
L = LANG_PACK[ui_lang]

st.markdown(f"""
    <div style='background-color:#003A70;padding:15px;border-radius:10px;margin-bottom:20px'>
        <h1 style='color:white;margin:0;font-family:sans-serif;'>{L['title']}</h1>
        <p style='color:#FFC107;margin:5px 0 0 0;'>{L['subtitle']}</p>
    </div>
""", unsafe_allow_html=True)

# Initialize Session-States
if "auth_logged_in" not in st.session_state:
    st.session_state["auth_logged_in"] = False
    st.session_state["cached_role"] = None
    st.session_state["cached_district"] = "All Districts"
    st.session_state["cached_facility"] = "ALL"

def local_stock_chart(df, title_txt):
    fig, ax = plt.subplots(figsize=(7, 3.2))
    df_sorted = df.sort_values(by='current_stock')
    colors = ['#DC3545' if x <= r['min_required_threshold'] else '#28A745' for x, r in zip(df_sorted['current_stock'], df_sorted.to_dict('records'))]
    bars = ax.barh(df_sorted['node_name'], df_sorted['current_stock'], color=colors, height=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(title_txt, fontsize=10, fontweight='bold')
    plt.tight_layout()
    return fig

def local_risk_chart(scope_district, y_label):
    conn = sqlite3.connect("data/smart_health.db")
    df = pd.read_sql_query("SELECT h.node_name, o.active_epidemic_risk_score, h.district_name FROM node_operations o JOIN administrative_hierarchy h ON o.node_id = h.node_id", conn)
    conn.close()
    if scope_district != "All Districts" and scope_district is not None:
        df = df[df['district_name'] == scope_district]
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.bar(df['node_name'], df['active_epidemic_risk_score'], color='#007BFF', alpha=0.85, width=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylabel(y_label, fontsize=9, fontweight='bold')
    ax.set_ylim(0, 1.0)
    plt.xticks(rotation=10, ha='right', fontsize=8)
    plt.tight_layout()
    return fig

# 🔐 COMPREHENSIVE UNIQUE PASSWORD AUTHENTICATION ENGINE
if not st.session_state["auth_logged_in"]:
    st.sidebar.header("🔐 Role Clearance Desk")
    selected_role = st.sidebar.selectbox(L['role_label'], ["Choose Role", "State Administrator", "District Officer", "ASHA Worker", "Medical Doctor", "Pharmacist"])
    password_input = st.sidebar.text_input(L['pass_label'], type="password", placeholder="••••••••••••")
    
    if st.sidebar.button(L['btn_login']):
        clean_pass = password_input.strip()
        
        # 1-to-1 Mapping Checks for Unique Passwords
        if selected_role == "State Administrator" and clean_pass == "AmaravatiHealth2026!":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "State Administrator"
            st.session_state["cached_district"] = "All Districts"
            st.rerun()
        elif selected_role == "District Officer" and clean_pass == "VizagCMO#2026!":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "District Officer"
            st.session_state["cached_district"] = "Visakhapatnam"
            st.rerun()
        elif selected_role == "District Officer" and clean_pass == "VizmCMO#2026!":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "District Officer"
            st.session_state["cached_district"] = "Vizianagaram"
            st.rerun()
        elif selected_role == "District Officer" and clean_pass == "SklmCMO#2026!":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "District Officer"
            st.session_state["cached_district"] = "Srikakulam"
            st.rerun()
        elif selected_role == "ASHA Worker" and clean_pass == "AshaVizag$Pnd":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "ASHA Worker"
            st.session_state["cached_facility"] = "IN-AP-VSP-PND"
            st.rerun()
        elif selected_role == "ASHA Worker" and clean_pass == "AshaVizm$Gjn":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "ASHA Worker"
            st.session_state["cached_facility"] = "IN-AP-VZM-GJN"
            st.rerun()
        elif selected_role == "ASHA Worker" and clean_pass == "AshaSklm$Rur":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "ASHA Worker"
            st.session_state["cached_facility"] = "IN-AP-SKL-RUR"
            st.rerun()
        elif selected_role == "Medical Doctor" and clean_pass in ["SrinivasaDoc#77", "AnuradhaPed#45"]:
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "Medical Doctor"
            st.session_state["cached_facility"] = "IN-AP-VSP-PND"
            st.rerun()
        elif selected_role == "Medical Doctor" and clean_pass == "LakshmiBhm#12":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "Medical Doctor"
            st.session_state["cached_facility"] = "IN-AP-VSP-BHM"
            st.rerun()
        elif selected_role == "Medical Doctor" and clean_pass == "KoteswaraVzm#39":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "Medical Doctor"
            st.session_state["cached_facility"] = "IN-AP-VZM-GJN"
            st.rerun()
        elif selected_role == "Medical Doctor" and clean_pass == "VenkatSklm#88":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "Medical Doctor"
            st.session_state["cached_facility"] = "IN-AP-SKL-RUR"
            st.rerun()
        elif selected_role == "Pharmacist" and clean_pass == "PharmaPnd%99":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "Pharmacist"
            st.session_state["cached_facility"] = "IN-AP-VSP-PND"
            st.rerun()
        elif selected_role == "Pharmacist" and clean_pass == "PharmaGjn%88":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "Pharmacist"
            st.session_state["cached_facility"] = "IN-AP-VZM-GJN"
            st.rerun()
        elif selected_role == "Pharmacist" and clean_pass == "PharmaRur%77":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = "Pharmacist"
            st.session_state["cached_facility"] = "IN-AP-SKL-RUR"
            st.rerun()
        else:
            st.sidebar.error("❌ Unique Password Mismatch.")
else:
    # 🚪 LOGOUT CONTROLLER
    st.sidebar.header("👤 Active Session Identity")
    st.sidebar.info(f"Role: {st.session_state['cached_role']}")
    if st.sidebar.button(L['btn_logout'], type="primary"):
        st.session_state["auth_logged_in"] = False
        st.session_state["cached_role"] = None
        st.session_state["cached_district"] = "All Districts"
        st.session_state["cached_facility"] = "ALL"
        st.rerun()

# RENDER CHARTS UNDER CURRENT AUTHENTICATED STATE
if st.session_state["auth_logged_in"]:
    conn = sqlite3.connect("data/smart_health.db")
    inventory_df = pd.read_sql_query("SELECT i.*, h.node_name, h.district_name, h.latitude, h.longitude FROM inventory i JOIN administrative_hierarchy h ON i.node_id = h.node_id", conn)
    conn.close()

    if st.session_state["cached_role"] == "State Administrator":
        st.session_state["cached_district"] = st.sidebar.selectbox("Global Navigation Overlay", ["All Districts", "Visakhapatnam", "Vizianagaram", "Srikakulam"])

    if st.session_state["cached_district"] != "All Districts":
        inventory_df = inventory_df[inventory_df['district_name'] == st.session_state["cached_district"]]

    if st.session_state["cached_role"] in ["State Administrator", "District Officer"]:
        st.subheader(f"📊 Surveillance Matrix Panel: [{st.session_state['cached_district']}]")
        col_g1, col_g2 = st.columns(2)
        with col_g1: st.pyplot(local_stock_chart(inventory_df, L['stock_title']))
        with col_g2: st.pyplot(local_risk_chart(st.session_state["cached_district"], L['risk_title']))
# app.py — BLOCK 3: TRANSLATED WORKFLOW LOGS
    st.markdown("---")
    
    # -------------------------------------------------------------
    # ROLE WORKFLOW VIEW 1: ASHA PATIENT TRIAGE COUNTER
    # -------------------------------------------------------------
    if st.session_state["cached_role"] == "ASHA Worker":
        st.subheader(L['asha_title'])
        with st.form("asha_entry_form"):
            pt_phone = st.text_input(L['pt_phone'], "9848022338")
            symptoms = st.text_input(L['symptoms'], "Acute High Fever, Severe Body Pains")
            sys_bp = st.number_input(L['sys_bp'], 80, 200, 130)
            dia_bp = st.number_input(L['dia_bp'], 50, 120, 85)
            consult_mode = st.radio(L['consult_mode'], ["e-Sanjeevani Video Call Telehealth", "Physical Local OPD Desk"])
            
            if st.form_submit_button(L['submit_intake']):
                conn = sqlite3.connect("data/smart_health.db")
                cursor = conn.cursor()
                token = f"AP-{cursor.execute('SELECT COUNT(*) FROM patient_triage_queue').fetchone() + 1001}"
                vitals_summary = f"{symptoms} | BP: {sys_bp}/{dia_bp} mmHg | Mode: {consult_mode}"
                cursor.execute("INSERT INTO patient_triage_queue VALUES (?, ?, ?, ?, ?, 'WAITING')", (token, st.session_state["cached_facility"], "sha256_hash", pt_phone, vitals_summary))
                conn.commit()
                conn.close()
                st.success(f"🎉 Saved! Token Assigned: **{token}**")

    # -------------------------------------------------------------
    # ROLE WORKFLOW VIEW 2: DOCTOR EVALUATION POOL
    # -------------------------------------------------------------
    elif st.session_state["cached_role"] == "Medical Doctor":
        st.subheader(L['doc_title'])
        conn = sqlite3.connect("data/smart_health.db")
        waiting_df = pd.read_sql_query("SELECT * FROM patient_triage_queue WHERE node_id = ? AND status = 'WAITING'", conn, params=(st.session_state["cached_facility"],))
        conn.close()
        
        if not waiting_df.empty:
            st.dataframe(waiting_df[['token_id', 'symptoms_logged']], use_container_width=True, hide_index=True)
            with st.form("doc_prescription_form"):
                target_token = st.selectbox(L['select_pt'], waiting_df['token_id'].tolist())
                rx_med = st.selectbox(L['prescribe'], ["Paracetamol Tabs", "Anti-Venom Vials", "Amoxicillin Caps"])
                rx_dose = st.text_input(L['dosage'], "1 tablet twice daily after meals")
                
                if st.form_submit_button(L['sign_rx']):
                    conn = sqlite3.connect("data/smart_health.db")
                    cursor = conn.cursor()
                    vitals_txt = cursor.execute("SELECT symptoms_logged FROM patient_triage_queue WHERE token_id = ?", (target_token,)).fetchone()
                    mode = "e-Sanjeevani Video Call Telehealth" if "Video" in vitals_txt else "Physical Local OPD Desk"
                    cursor.execute("INSERT INTO patient_prescriptions (token_id, node_id, doctor_name, medication_name, dosage_instructions, consult_mode, status) VALUES (?, ?, ?, ?, ?, ?, 'PENDING')",
                                   (target_token, st.session_state["cached_facility"], "Attending Doctor", rx_med, rx_dose, mode))
                    cursor.execute("UPDATE patient_triage_queue SET status = 'COMPLETED' WHERE token_id = ?", (target_token,))
                    conn.commit()
                    conn.close()
                    st.success("🏥 Prescription Transmitted to Pharmacy Desk!")
                    st.rerun()
        else:
            st.success("🟢 No patients waiting.")

    # -------------------------------------------------------------
    # ROLE WORKFLOW VIEW 3: PHARMACIST DELIVERY DESK
    # -------------------------------------------------------------
    elif st.session_state["cached_role"] == "Pharmacist":
        st.subheader(L['pharma_title'])
        conn = sqlite3.connect("data/smart_health.db")
        orders_df = pd.read_sql_query("SELECT * FROM patient_prescriptions WHERE node_id = ? AND status = 'PENDING'", conn, params=(st.session_state["cached_facility"],))
        conn.close()
        
        if not orders_df.empty:
            st.dataframe(orders_df[['prescription_id', 'token_id', 'medication_name', 'consult_mode']], use_container_width=True, hide_index=True)
            with st.form("pharma_fulfillment_form"):
                target_rx = st.selectbox(L['select_rx'], orders_df['prescription_id'].tolist())
                delivery_method = st.radio(L['logistics_path'], ["📦 Over-the-Counter Counter Handout", "✈️ Autonomous BVLOS Drone Resupply Flight Path"])
                
                if st.form_submit_button(L['dispatch']):
                    conn = sqlite3.connect("data/smart_health.db")
                    cursor = conn.cursor()
                    rx_item = cursor.execute("SELECT medication_name FROM patient_prescriptions WHERE prescription_id = ?", (target_rx,)).fetchone()
                    cursor.execute("UPDATE inventory SET current_stock = current_stock - 1 WHERE node_id = ? AND item_name = ?", (st.session_state["cached_facility"], rx_item))
                    cursor.execute("UPDATE patient_prescriptions SET status = 'FULFILLED' WHERE prescription_id = ?", (target_rx,))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Order #{target_rx} Dispatched!")
                    if "Drone" in delivery_method:
                        st.warning(f"✈️ Launching drone resupply payload.")
                    st.rerun()
        else:
            st.success("🟢 No pending orders.")

    elif st.session_state["cached_role"] in ["State Administrator", "District Officer"]:
        conn = sqlite3.connect("data/smart_health.db")
        global_triage = pd.read_sql_query("SELECT t.token_id, h.node_name, t.symptoms_logged, t.status FROM patient_triage_queue t JOIN administrative_hierarchy h ON t.node_id = h.node_id", conn)
        conn.close()
        st.subheader("📋 Administrative Master Triage Records")
        st.dataframe(global_triage, use_container_width=True, hide_index=True)

    # 🤖 UNIFIED LOCALIZED GEMINI FORECASTER
    if st.session_state["cached_role"] in ["State Administrator", "District Officer"]:
        st.markdown("---")
        st.subheader(L['ai_title'])
        typed_api_key = st.text_input("🌐 Paste Gemini API Key to unlock AI Module", type="password", placeholder="AIza...")
        
        if st.button(L['run_ai']):
            if typed_api_key.strip().startswith("AIza") and len(typed_api_key.strip()) > 10:
                with st.spinner("Analyzing data with Gemini..."):
                    try:
                        client = engine.genai.Client(api_key=typed_api_key.strip())
                        summary_txt = inventory_df[['node_name', 'item_name', 'current_stock', 'min_required_threshold', 'daily_avg_consumption']].to_string()
                        prompt = f"Provide a concise 2-sentence summary intervention plan for this data:\n{summary_txt}"
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                        st.subheader("📋 Executive Strategic Health Summary")
                        st.warning(response.text)
                    except Exception as e:
                        st.error(f"Gemini API Execution Error: {str(e)}")
            else:
                st.error("Please insert a valid developer API Key to unlock this module.")
else:
    st.info(L['lock_msg'])
