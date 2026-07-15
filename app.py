# app.py — BLOCK 1: CORE ENGINE SETUP & LOCALIZATION DICTIONARIES
import streamlit as st 
import pandas as pd 
import sqlite3 
import os 
import matplotlib.pyplot as plt 
import src.predictive_engine as engine

# EMBEDDED AUTOMATIC DATABASE CREATION ENGINE
def build_native_database_instance(): 
    """Initialises relational SQLite files natively on execution to avoid import conflicts."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/smart_health.db")
    cursor = conn.cursor()
    with open("data/schema.sql", "r", encoding="utf-8") as schema_file: 
        cursor.executescript(schema_file.read())
 
    # Reset datasets to allow clean test loops on container hot-reloads
    cursor.execute("DELETE FROM system_audit_logs;")
    cursor.execute("DELETE FROM patient_prescriptions;")
    cursor.execute("DELETE FROM patient_triage_queue;")
    cursor.execute("DELETE FROM node_operations;")
    cursor.execute("DELETE FROM inventory;")
    cursor.execute("DELETE FROM pharmacists;")
    cursor.execute("DELETE FROM asha_workers;")
    cursor.execute("DELETE FROM doctors;")
    cursor.execute("DELETE FROM administrative_hierarchy;")
    
    # 1. Seed Geographic Nodes Matrix
    facilities = [ 
        ('IN-AP-VSP-PND', 'Tehsil', 'Pendurthi CHC Hub', 'Andhra Pradesh', 'Visakhapatnam', 17.8303, 83.1979),
        ('IN-AP-VSP-BHM', 'Tehsil', 'Bheemili Hospital Spoke', 'Andhra Pradesh', 'Visakhapatnam', 17.8894, 83.4452),
        ('IN-AP-VZM-GJN', 'Tehsil', 'Gajapathinagaram PHC', 'Andhra Pradesh', 'Vizianagaram', 18.2789, 83.3323),
        ('IN-AP-SKL-RUR', 'Tehsil', 'Srikakulam Rural Center', 'Andhra Pradesh', 'Srikakulam', 18.3164, 83.8943),
        ('IN-AP-SKL-PLS', 'Tehsil', 'Palasa Super-Spec Spoke', 'Andhra Pradesh', 'Srikakulam', 18.7725, 84.4172)
    ] 
    cursor.executemany("INSERT INTO administrative_hierarchy VALUES (?, ?, ?, ?, ?, ?, ?)", facilities)
    
    # 2. Seed Medical Officers Registry
    doctors = [ 
        ('DOC-VSP-001', 'IN-AP-VSP-PND', 'Dr. S. Srinivasa Rao', 'General Medicine', 1),
        ('DOC-VSP-002', 'IN-AP-VSP-PND', 'Dr. K. Anuradha', 'Pediatrics', 1),
        ('DOC-VSP-003', 'IN-AP-VSP-BHM', 'Dr. A. Lakshmi Prasanna', 'General Medicine', 1),
        ('DOC-VZM-001', 'IN-AP-VZM-GJN', 'Dr. Ch. Koteswara Rao', 'General Medicine', 1),
        ('DOC-SKL-001', 'IN-AP-SKL-RUR', 'Dr. K. Venkataswamy', 'General Medicine', 1)
    ] 
    cursor.executemany("INSERT INTO doctors VALUES (?, ?, ?, ?, ?)", doctors)
    
    # 3. Seed Ground Intake Workers Directory
    ashas = [ 
        ('ASHA-VSP-001', 'IN-AP-VSP-PND', 'asha_worker', 'Smt. Lakshmi', 'Pendurthi Village A'),
        ('ASHA-VZM-001', 'IN-AP-VZM-GJN', 'asha_gajapathinagaram', 'Smt. Saraswathi', 'Gajapathinagaram West'),
        ('ASHA-SKL-001', 'IN-AP-SKL-RUR', 'asha_srikakulam', 'Smt. Parvathi', 'Srikakulam Outer Ring')
    ] 
    cursor.executemany("INSERT INTO asha_workers VALUES (?, ?, ?, ?, ?)", ashas)
    
    # 4. Seed Pharmacy Store Unit Operators
    pharmacists = [ 
        ('PHR-VSP-001', 'IN-AP-VSP-PND', 'pharma_person', 'Sri K. Venkatesh'),
        ('PHR-VZM-001', 'IN-AP-VZM-GJN', 'pharma_gajapathinagaram', 'Sri L. Narayana'),
        ('PHR-SKL-001', 'IN-AP-SKL-RUR', 'pharma_srikakulam_rur', 'Sri P. Satyam')
    ] 
    cursor.executemany("INSERT INTO pharmacists VALUES (?, ?, ?, ?)", pharmacists)
    
    # 5. Seed Medicine Inventory Grid
    inventory_data = [ 
        ('IN-AP-VSP-PND', 'Paracetamol Tabs', 450, 5000, 450.0),
        ('IN-AP-VSP-BHM', 'Paracetamol Tabs', 18000, 4000, 180.0),
        ('IN-AP-VZM-GJN', 'Paracetamol Tabs', 5500, 3000, 210.0),
        ('IN-AP-SKL-RUR', 'Anti-Venom Vials', 3, 40, 6.5),
        ('IN-AP-SKL-PLS', 'Anti-Venom Vials', 150, 30, 2.0)
    ] 
    cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", inventory_data)
    
    # 6. Seed Baseline Clinical Queues
    triage_data = [ 
        ('AP-1422', 'IN-AP-VSP-PND', 'sha256_hash_xyz1', '9848022338', 'High Fever, Vomiting | BP: 135/85 mmHg | Mode: e-Sanjeevani Video Call Telehealth', 'WAITING'),
        ('AP-1423', 'IN-AP-SKL-RUR', 'sha256_hash_xyz2', '9440123456', 'Acute Snake Bite | BP: 140/90 mmHg | Mode: Physical Local OPD Desk', 'WAITING')
    ] 
    cursor.executemany("INSERT INTO patient_triage_queue VALUES (?, ?, ?, ?, ?, ?)", triage_data)
    
    # 7. Seed Bed Capacity Metrics
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

LANG_PACK = { 
    "English": { 
        "title": "📋 Bharat Health AI: Multi-Role Operations Matrix", 
        "subtitle": "Track 3: Smart Health Dashboard — End-to-End Workflow Verification",
        "lock_msg": "🔒 Please use the Quick Demo Login buttons or sign in via the left sidebar to unlock records.",
        "role_label": "Select Your System Role", 
        "pass_label": "Enter Password (For manual demo, use: demo123)",
        "lang_label": "🌐 Change UI Language",
        "stock_title": "AI Supply Depletion & Stock Grid Monitor", 
        "risk_title": "Outbreak Risk Multiplier",
        "asha_title": "Frontline Patient Intake Registration Matrix", 
        "pt_phone": "Patient Contact Mobile Number", 
        "symptoms": "Logged Symptoms Description",
        "sys_bp": "Vitals: Systolic Blood Pressure (mmHg)", 
        "dia_bp": "Vitals: Diastolic Blood Pressure (mmHg)",
        "consult_mode": "Requested Consultation Mode",
        "submit_intake": "🚀 Push Triage Metrics to Clinical Queue", 
        "doc_title": "🧑‍⚕️ Medical Practitioner Evaluation Pool", 
        "select_pt": "Select Active Patient Token to Treat",
        "prescribe": "Prescribe Necessary Medical Formulation", 
        "dosage": "Dosage Regulation Instructions", 
        "sign_rx": "✍️ Authorize and Sign Digital Prescription",
        "pharma_title": "💊 Pharmacy Dispensation Desk & Aero-Logistics Network", 
        "select_rx": "Select Prescription ID to Dispense", 
        "logistics_path": "Fulfillment Logistics Path",
        "dispatch": "📦 Finalize Dispensation Order", 
        "ai_title": "🧠 Gemini 2.5 Flash Autonomous Intervention Planner", 
        "run_ai": "⚡ Run AI Demand Analytics",
        "btn_login": "🔑 Authenticate & Login", 
        "btn_logout": "🚪 Secure Session Logout"
    },
    "िहंतो (Hindi)": { 
        "title": "📋 भारत हेल्थ एआई: मल्टी-रोल ऑपरेशंस मैट्रिक्स", 
        "subtitle": "ट्रैक 3: स्मार्ट हेल्थ डैशबोर्ड — एंड-टू-एंड वर्कफ़्लो सत्यापन",
        "lock_msg": "🔒 रिकॉर्ड अनलॉक करने के लिए कृपया त्वरित डेमो लॉगिन का उपयोग करें या साइन इन करें।",
        "role_label": "अपनी सिस्टम भूमिका चुनें", 
        "pass_label": "पासवर्ड दर्ज करें (डेमो के लिए: demo123)",
        "lang_label": "🌐 यूआई भाषा बदलें",
        "stock_title": "एआई आपूर्ति कमी और स्टॉक ग्रिड मॉनिटर", 
        "risk_title": "प्रकोप जोखिम गुणक",
        "asha_title": "आशा कार्यकर्ता रोगी पंजीकरण फॉर्म", 
        "pt_phone": "रोगी का मोबाइल नंबर", 
        "symptoms": "रोगी के लक्षणों का विवरण",
        "sys_bp": "सिस्टोलिक रक्तचाप (Systolic BP)", 
        "dia_bp": "डायस्टोलिक रक्तचाप (Diastolic BP)",
        "consult_mode": "परामर्श का अनुरोधित तरीका",
        "submit_intake": "रोगी के विवरण क्लिनिकल कतार में भेजें", 
        "doc_title": "चिकित्सक मूल्यांकन पोर्टल", 
        "select_pt": "उपचार के लिए सक्रिय रोगी टोकन चुनें",
        "prescribe": "आवश्यक दवा फॉर्मूलेशन लिखें", 
        "dosage": "दवा की खुराक के निर्देश", 
        "sign_rx": "डिजिटल नुस्खा प्रमाणित करें",
        "pharma_title": "फार्मेसी वितरण डेस्क और ड्रोन रसद (Logistics)", 
        "select_rx": "वितरण के लिए प्रिस्क्रिप्शन आईडी चुनें", 
        "logistics_path": "वितरण रसद पथ",
        "dispatch": "वितरण आदेश अंतिम रूप दें", 
        "ai_title": "जेमिनी एआई मांग और हस्तक्षेप योजनाकार",
        "run_ai": "एआई मांग विश्लेषण चलाएं",
        "btn_login": "लॉग इन करें", 
        "btn_logout": "सुरक्षित सत्र लॉगआउट"
    }
}

st.sidebar.header("🌐 Localization Setup")
ui_lang = st.sidebar.selectbox("Select Display Language", ["English", "िहंतो (Hindi)"])
L = LANG_PACK[ui_lang]
# app.py — BLOCK 2: PASSWORDLESS ACCESS AUTHENTICATION MAPPING & DASHBOARDS
st.markdown(f""" 
 <div style='background-color:#003A70;padding:15px;border-radius:10px;margin-bottom:20px'> 
 <h1 style='color:white;margin:0;font-family:sans-serif;'>{L['title']}</h1> 
 <p style='color:#FFC107;margin:5px 0 0 0;'>{L['subtitle']}</p> 
 </div> 
""", unsafe_allow_html=True)

if "auth_logged_in" not in st.session_state: 
    st.session_state["auth_logged_in"] = False 
    st.session_state["cached_role"] = None 
    st.session_state["cached_district"] = "All Districts" 
    st.session_state["cached_facility"] = "ALL"

def local_stock_chart(df, title_txt): 
    fig, ax = plt.subplots(figsize=(7, 3.2)) 
    df_sorted = df.sort_values(by='current_stock') 
    colors = ['#DC3545' if x <= r['min_required_threshold'] else '#28A745' for x, r in zip(df_sorted['current_stock'], df_sorted.to_dict('records'))]
    ax.barh(df_sorted['node_name'], df_sorted['current_stock'], color=colors, height=0.5)
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

if not st.session_state["auth_logged_in"]: 
    st.sidebar.header("⚖️ Judge Quick Demo Login")
    st.sidebar.caption("Click any role to log in instantly without a password:")
    
    if st.sidebar.button("👑 Log in as State Admin", use_container_width=True):
        st.session_state["auth_logged_in"] = True
        st.session_state["cached_role"] = "State Administrator"
        st.session_state["cached_district"] = "All Districts"
        st.rerun()

    if st.sidebar.button("📊 Log in as District Officer", use_container_width=True):
        st.session_state["auth_logged_in"] = True
        st.session_state["cached_role"] = "District Officer"
        st.session_state["cached_district"] = "Visakhapatnam"
        st.rerun()

    if st.sidebar.button("🩺 Log in as Medical Doctor", use_container_width=True):
        st.session_state["auth_logged_in"] = True
        st.session_state["cached_role"] = "Medical Doctor"
        st.session_state["cached_facility"] = "IN-AP-VSP-PND"
        st.session_state["cached_district"] = "Visakhapatnam"
        st.rerun()

    if st.sidebar.button("🌾 Log in as ASHA Worker", use_container_width=True):
        st.session_state["auth_logged_in"] = True
        st.session_state["cached_role"] = "ASHA Worker"
        st.session_state["cached_facility"] = "IN-AP-VSP-PND"
        st.session_state["cached_district"] = "Visakhapatnam"
        st.rerun()

    if st.sidebar.button("💊 Log in as Pharmacist", use_container_width=True):
        st.session_state["auth_logged_in"] = True
        st.session_state["cached_role"] = "Pharmacist"
        st.session_state["cached_facility"] = "IN-AP-VSP-PND"
        st.session_state["cached_district"] = "Visakhapatnam"
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.header("🔑 Manual Staging Sign-In")
    selected_role = st.sidebar.selectbox(L['role_label'], ["Choose Role", "State Administrator", "District Officer", "ASHA Worker", "Medical Doctor", "Pharmacist"])
    password_input = st.sidebar.text_input(L['pass_label'], type="password", placeholder="••••••••••••")
    clean_pass = password_input.strip()
    
    if st.sidebar.button(L['btn_login']):
        if clean_pass == "demo123" and selected_role != "Choose Role":
            st.session_state["auth_logged_in"] = True
            st.session_state["cached_role"] = selected_role
            if selected_role == "State Administrator":
                st.session_state["cached_district"] = "All Districts"
            else:
                st.session_state["cached_facility"] = "IN-AP-VSP-PND"
                st.session_state["cached_district"] = "Visakhapatnam"
            st.rerun()
        elif clean_pass != "":
            st.sidebar.error("❌ Unique Password Mismatch.")
else: 
    st.sidebar.header("Active Session Identity")
    st.sidebar.info(f"Role: {st.session_state['cached_role']} | Area: {st.session_state['cached_district']}")
    if st.sidebar.button(L['btn_logout'], type="primary"):
        st.session_state["auth_logged_in"] = False 
        st.session_state["cached_role"] = None 
        st.session_state["cached_district"] = "All Districts" 
        st.session_state["cached_facility"] = "ALL"
        st.rerun()
# app.py — BLOCK 3: FRONT-END WORKFLOW INTERFACES WITH GEOSPATIAL MAPS
if st.session_state["auth_logged_in"]: 
    conn = sqlite3.connect("data/smart_health.db")
    inventory_df = pd.read_sql_query("SELECT i.*, h.node_name, h.district_name, h.latitude, h.longitude FROM inventory i JOIN administrative_hierarchy h ON i.node_id = h.node_id", conn)
    conn.close()
    if st.session_state["cached_district"] != "All Districts": 
        inventory_df = inventory_df[inventory_df['district_name'] == st.session_state["cached_district"]]
    if st.session_state["cached_role"] in ["State Administrator", "District Officer"]:
        st.subheader(f"Surveillance Operations Panel: [{st.session_state['cached_district']}]")
        col_g1, col_g2 = st.columns(2) 
        with col_g1: st.pyplot(local_stock_chart(inventory_df, L['stock_title']))
        with col_g2: st.pyplot(local_risk_chart(st.session_state["cached_district"], L['risk_title']))

    st.markdown("---") 
    st.subheader(f"Active Operational Workspace: {st.session_state['cached_role']} Tier")
 
    # ROLE WORKFLOW VIEW 1: ASHA PATIENT TRIAGE COUNTER
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
                count_tuple = cursor.execute('SELECT COUNT(*) FROM patient_triage_queue').fetchone()[0]
                token = f"AP-{count_tuple + 1001}"
                vitals_summary = f"{symptoms} | BP: {sys_bp}/{dia_bp} mmHg | Mode: {consult_mode}"
                cursor.execute("INSERT INTO patient_triage_queue VALUES (?, ?, ?, ?, ?, 'WAITING')", (token, st.session_state["cached_facility"], "sha256_hash", pt_phone, vitals_summary))
                conn.commit()
                conn.close()
                st.success(f"Saved! Token Assigned: **{token}**")

    # ROLE WORKFLOW VIEW 2: DOCTOR EVALUATION POOL
    elif st.session_state["cached_role"] == "Medical Doctor": 
        st.subheader(L['doc_title'])
        conn = sqlite3.connect("data/smart_health.db")
        waiting_df = pd.read_sql_query("SELECT * FROM patient_triage_queue WHERE node_id = ? AND status = 'WAITING'", conn, params=(st.session_state["cached_facility"],))
        conn.close()
 
        if not waiting_df.empty: 
            video_cases = waiting_df[waiting_df['symptoms_logged'].str.contains("e-Sanjeevani", na=False)]
            if not video_cases.empty: 
                st.components.v1.html("<script>var msg = new SpeechSynthesisUtterance(); msg.text = 'Attention Doctor. A new e Sanjeevani Telehealth patient has joined.'; msg.rate = 1.0; window.speechSynthesis.speak(msg);</script>", height=0, width=0)
                st.markdown("<div style='background-color:#1E1E1E; padding:20px; border-radius:10px; border:2px solid #007BFF; text-align:center;'><h4>Connected Tele-Consultation Stream</h4><p style='color:#28A745;'>Secure Pipeline Active</p></div>", unsafe_allow_html=True)
 
            st.dataframe(waiting_df[['token_id', 'symptoms_logged']], use_container_width=True, hide_index=True)
            with st.form("doc_prescription_form"): 
                target_token = st.selectbox(L['select_pt'], waiting_df['token_id'].tolist())
                rx_med = st.selectbox(L['prescribe'], ["Paracetamol Tabs", "Anti-Venom Vials", "Amoxicillin Caps"])
                rx_dose = st.text_input(L['dosage'], "1 tablet twice daily after meals")
 
                if st.form_submit_button(L['sign_rx']):
                    conn = sqlite3.connect("data/smart_health.db")
                    cursor = conn.cursor()
                    vitals_txt = cursor.execute("SELECT symptoms_logged FROM patient_triage_queue WHERE token_id = ?", (target_token,)).fetchone()[0]
                    mode = "e-Sanjeevani Video Call Telehealth" if "Video" in vitals_txt else "Physical Local OPD Desk"
                    cursor.execute("INSERT INTO patient_prescriptions (token_id, node_id, doctor_name, medication_name, dosage_instructions, consult_mode, status) VALUES (?, ?, ?, ?, ?, ?, 'PENDING')", (target_token, st.session_state["cached_facility"], "Attending Doctor", rx_med, rx_dose, mode))
                    cursor.execute("UPDATE patient_triage_queue SET status = 'COMPLETED' WHERE token_id = ?", (target_token,))
                    conn.commit()
                    conn.close()
                    st.success("Prescription Transmitted to Pharmacy Desk!")
                    st.rerun()
        else: 
            st.success("No patients waiting in your facility consultation queue.")
# app.py — BLOCK 4: PHARMACIST DELIVERY DESK & ADMINISTRATIVE LEDGER
    elif st.session_state["cached_role"] == "Pharmacist": 
        st.subheader(L['pharma_title'])
        conn = sqlite3.connect("data/smart_health.db")
        orders_df = pd.read_sql_query("SELECT p.*, h.node_name, h.latitude, h.longitude FROM patient_prescriptions p JOIN administrative_hierarchy h ON p.node_id = h.node_id WHERE p.node_id = ? AND p.status = 'PENDING'", conn, params=(st.session_state["cached_facility"],))
        conn.close()
 
        if not orders_df.empty: 
            st.dataframe(orders_df[['prescription_id', 'token_id', 'medication_name', 'consult_mode']], use_container_width=True, hide_index=True)
            with st.form("pharma_fulfillment_form"): 
                target_rx = st.selectbox(L['select_rx'], orders_df['prescription_id'].tolist())
                delivery_method = st.radio(L['logistics_path'], ["Over-the-Counter Counter Handout", "Autonomous BVLOS Drone Resupply Flight Path"])
 
                if st.form_submit_button(L['dispatch']):
                    conn = sqlite3.connect("data/smart_health.db")
                    cursor = conn.cursor()
                    rx_item = cursor.execute("SELECT medication_name FROM patient_prescriptions WHERE prescription_id = ?", (target_rx,)).fetchone()[0]
                    cursor.execute("UPDATE inventory SET current_stock = current_stock - 1 WHERE node_id = ? AND item_name = ?", (st.session_state["cached_facility"], rx_item))
                    cursor.execute("UPDATE patient_prescriptions SET status = 'FULFILLED' WHERE prescription_id = ?", (target_rx,))
                    conn.commit()
                    conn.close()
                    st.success(f"Order #{target_rx} Dispatched!")
 
                    if "Drone" in delivery_method: 
                        target_row = orders_df[orders_df['prescription_id'] == target_rx].iloc[0]
                        st.warning("Launching drone resupply payload.")
                        map_data = pd.DataFrame({'lat': [float(target_row['latitude'])], 'lon': [float(target_row['longitude'])]})
                        st.map(map_data, zoom=12, use_container_width=True)
                        st.rerun()
        else: 
            st.success("No pending orders require processing at your pharmacy unit.")

    if st.session_state["cached_role"] in ["State Administrator", "District Officer"]:
        conn = sqlite3.connect("data/smart_health.db")
        global_triage = pd.read_sql_query("SELECT t.token_id, h.node_name, t.symptoms_logged, t.status, h.district_name FROM patient_triage_queue t JOIN administrative_hierarchy h ON t.node_id = h.node_id", conn)
        conn.close()
 
        if st.session_state["cached_district"] != "All Districts": 
            global_triage = global_triage[global_triage['district_name'] == st.session_state["cached_district"]]
 
        st.subheader(f"Administrative Triage Ledger: [{st.session_state['cached_district']}] Scope")
        if not global_triage.empty: 
            st.dataframe(global_triage[['token_id', 'node_name', 'symptoms_logged', 'status']], use_container_width=True, hide_index=True)
        else: 
            st.info(f"Clearance Status: No active records logged within {st.session_state['cached_district']}.")
 
    # UNIFIED MEMORY-SAFE GEMINI 2.5 FLASH SURVEILLANCE GENERATOR
    if st.session_state["cached_role"] in ["State Administrator", "District Officer"]: 
        st.markdown("---") 
        st.subheader(L['ai_title'])
        typed_api_key = st.text_input("Paste Gemini API Key to unlock AI Module", type="password", placeholder="Enter your key string...")
 
        if st.button(L['run_ai']):
            clean_api_key = typed_api_key.strip()
            if len(clean_api_key) > 5: 
                with st.spinner("Analyzing data streams with Gemini..."):
                    try: 
                        client = engine.genai.Client(api_key=clean_api_key)
                        summary_txt = inventory_df[['node_name', 'item_name', 'current_stock', 'min_required_threshold', 'daily_avg_consumption']].to_string()
                        prompt = f"Provide a concise 2-sentence summary intervention plan for this data:\n{summary_txt}"
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                        st.subheader("Executive Strategic Health Summary")
                        st.warning(response.text)
                    except Exception as e: 
                        st.error(f"Gemini API Execution Error: {str(e)}")
            else: 
                st.error("Key Error: Please paste your active developer Gemini API key into the field box above.")
else: 
    st.info(LANG_PACK[ui_lang]['lock_msg'])
