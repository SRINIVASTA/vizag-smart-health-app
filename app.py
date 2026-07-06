import streamlit as st
import pandas as pd
import sqlite3
import datetime
import random

# Import modular components directly from the package architecture
from src.language_pack import LOCALIZATION_DATA, LANGUAGE_NAME_MAP
from src.auth import USER_REGISTRY, log_transaction
from src.predictive_engine import (
    calculate_days_to_depletion, 
    run_cross_tier_supply_balancing, 
    generate_stock_prediction_chart, 
    generate_epidemic_risk_chart
)
from src.drone_logistics import map_cross_tier_drone_grid
from src.telehealth import build_esanjeevani_routing_gateway

# ==========================================
# IDEMPOTENT DB PILOT PHASE INITIALIZATION
# ==========================================
def init_ap_pilot_db():
    conn = sqlite3.connect("smart_health.db")
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS administrative_hierarchy (node_id TEXT PRIMARY KEY, node_level TEXT, node_name TEXT, state_name TEXT, district_name TEXT, latitude REAL, longitude REAL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS doctors (doctor_id TEXT PRIMARY KEY, node_id TEXT, doctor_name TEXT, specialization TEXT, active_status INT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS asha_workers (asha_id TEXT PRIMARY KEY, node_id TEXT, username TEXT, worker_name TEXT, assigned_village TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS pharmacists (pharma_id TEXT PRIMARY KEY, node_id TEXT, username TEXT, employee_name TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS inventory (node_id TEXT, item_name TEXT, current_stock INT, min_required_threshold INT, daily_avg_consumption REAL, PRIMARY KEY (node_id, item_name));")
    cursor.execute("CREATE TABLE IF NOT EXISTS patient_triage_queue (token_id TEXT PRIMARY KEY, node_id TEXT, aadhaar_hash TEXT, patient_phone TEXT, symptoms_logged TEXT, status TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS node_operations (node_id TEXT PRIMARY KEY, total_beds INT, occupied_beds INT, active_epidemic_risk_score REAL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS system_audit_logs (log_id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, user_role TEXT, node_id TEXT, action_type TEXT, details TEXT);")
    
    cursor.execute("SELECT COUNT(*) FROM administrative_hierarchy;")
    if cursor.fetchone() == 0:
        # 🏥 SEED 1: 10 AP Pilot Health Facilities (Visakhapatnam, Srikakulam, Vizianagaram)
        nodes = [
            ("IN-AP-VSP-PND", "Tehsil", "Pendurthi CHC Hub", "Andhra Pradesh", "Visakhapatnam", 17.8344, 83.2014),
            ("IN-AP-VSP-BHM", "Tehsil", "Bheemili Hospital Spoke", "Andhra Pradesh", "Visakhapatnam", 17.8903, 83.4447),
            ("IN-AP-VSP-GJV", "Tehsil", "Gajuwaka Industrial PHC", "Andhra Pradesh", "Visakhapatnam", 17.6896, 83.2089),
            ("IN-AP-VSP-ANA", "Tehsil", "Anakapalle Referral CHC", "Andhra Pradesh", "Visakhapatnam", 17.6895, 83.0024),
            ("IN-AP-VZM-GJM", "Tehsil", "Gajapathinagaram PHC", "Andhra Pradesh", "Vizianagaram", 18.2750, 83.3314),
            ("IN-AP-VZM-CHB", "Tehsil", "Cheepurupalli Spoke CHC", "Andhra Pradesh", "Vizianagaram", 18.3094, 83.5656),
            ("IN-AP-VZM-SKR", "Tehsil", "Sravankota Rural PHC", "Andhra Pradesh", "Vizianagaram", 18.4210, 83.4110),
            ("IN-AP-SKL-RUR", "Tehsil", "Srikakulam Rural Health Center", "Andhra Pradesh", "Srikakulam", 18.2949, 83.8938),
            ("IN-AP-SKL-PLM", "Tehsil", "Palasa Super-Specialty Spoke", "Andhra Pradesh", "Srikakulam", 18.7702, 84.4178),
            ("IN-AP-SKL-TKK", "Tehsil", "Tekkali Area Referral CHC", "Andhra Pradesh", "Srikakulam", 18.6134, 84.2324)
        ]
        cursor.executemany("INSERT INTO administrative_hierarchy VALUES (?, ?, ?, ?, ?, ?, ?);", nodes)
        
        # 🩺 SEED 2: 10 Shift On-Duty Doctors
        cursor.executemany("INSERT INTO doctors VALUES (?, ?, ?, ?, ?);", [
            ("DOC001", "IN-AP-VSP-PND", "Dr. S. Srinivasa Rao", "General Medicine", 1),
            ("DOC002", "IN-AP-VSP-PND", "Dr. K. Anuradha", "Gynaecology Specialist", 1),
            ("DOC003", "IN-AP-VSP-BHM", "Dr. A. Lakshmi Prasanna", "Pediatrics", 1),
            ("DOC004", "IN-AP-VSP-GJV", "Dr. P. Venkatesh", "Occupational Health", 1),
            ("DOC005", "IN-AP-VSP-ANA", "Dr. G. Satyanarayana", "General Surgery", 1),
            ("DOC006", "IN-AP-VZM-GJM", "Dr. Ch. Koteswara Rao", "Family Physician", 1),
            ("DOC007", "IN-AP-VZM-CHB", "Dr. M. Sridevi", "Internal Medicine", 1),
            ("DOC008", "IN-AP-VZM-SKR", "Dr. J. Ramana", "Emergency Care Triage", 1),
            ("DOC009", "IN-AP-SKL-RUR", "Dr. K. Venkataswamy", "Epidemiology Specialist", 1),
            ("DOC010", "IN-AP-SKL-PLM", "Dr. Y. Appala Naidu", "Nephrology Consultant", 1)
        ])
        
        # 🎒 SEED 3: 10 Local ASHA Workers with specific Usernames mapped to Facilities
        cursor.executemany("INSERT INTO asha_workers VALUES (?, ?, ?, ?, ?);", [
            ("ASHA001", "IN-AP-VSP-PND", "asha_worker", "Smt. T. Appalanamma", "Pendurthi Sector 1"),
            ("ASHA002", "IN-AP-VSP-PND", "asha_gorapalli", "Smt. K. Satyavathi", "Gorapalli Village"),
            ("ASHA003", "IN-AP-VSP-BHM", "asha_bheemili", "Smt. G. Lakshmi", "Bheemili Coastal Zone"),
            ("ASHA004", "IN-AP-VSP-GJV", "asha_gajuwaka", "Smt. P. Mary", "Gajuwaka Colony Beta"),
            ("ASHA005", "IN-AP-VSP-ANA", "asha_anakapalle", "Smt. B. Durga", "Anakapalle Rural Grid"),
            ("ASHA006", "IN-AP-VZM-GJM", "asha_gajapathinagaram", "Smt. D. Parvathi", "Gajapathinagaram Ward 4"),
            ("ASHA007", "IN-AP-VZM-CHB", "asha_cheepurupalli", "Smt. V. Ramani", "Cheepurupalli East"),
            ("ASHA008", "IN-AP-VZM-SKR", "asha_sravankota", "Smt. M. Gowri", "Sravankota Hills Node"),
            ("ASHA009", "IN-AP-SKL-RUR", "asha_srikakulam", "Smt. K. Chittemma", "Srikakulam River Block"),
            ("ASHA010", "IN-AP-SKL-PLM", "asha_palasa", "Smt. L. Savithri", "Palasa Cashew Village")
        ])

        # 💊 SEED 4: 10 Local Pharmacists mapped to Facilities
        cursor.executemany("INSERT INTO pharmacists VALUES (?, ?, ?, ?);", [
            ("PHM001", "IN-AP-VSP-PND", "pharma_person", "Sri K. Jagannadham"),
            ("PHM002", "IN-AP-VSP-BHM", "pharma_bheemili", "Sri G. Anand Kumar"),
            ("PHM003", "IN-AP-VSP-GJV", "pharma_gajuwaka", "Smt. S. Kalyani"),
            ("PHM004", "IN-AP-VSP-ANA", "pharma_anakapalle", "Sri V. Naidu"),
            ("PHM005", "IN-AP-VZM-GJM", "pharma_gajapathinagaram", "Sri R. K. Prasad"),
            ("PHM006", "IN-AP-VZM-CHB", "pharma_cheepurupalli", "Smt. T. Radha"),
            ("PHM007", "IN-AP-VZM-SKR", "pharma_sravankota", "Sri P. Simhachalam"),
            ("PHM008", "IN-AP-SKL-RUR", "pharma_srikakulam_rur", "Sri B. Krishna"),
            ("PHM009", "IN-AP-SKL-PLM", "pharma_palasa", "Sri N. Mohana Rao"),
            ("PHM010", "IN-AP-SKL-TKK", "pharma_tekkali", "Smt. V. Anuradha")
        ])
        
        # 📦 SEED 5: 10 Pharmacy Inventory Records
        cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?);", [
            ("IN-AP-VSP-PND", "Anti-Viral Medical Kits", 5, 200, 12.5),
            ("IN-AP-VSP-PND", "Paracetamol 500mg Tab", 450, 2000, 150.0),
            ("IN-AP-VSP-BHM", "Anti-Viral Medical Kits", 1800, 300, 22.0),
            ("IN-AP-VSP-BHM", "Amoxicillin 250mg Caps", 2300, 500, 45.0),
            ("IN-AP-VSP-GJV", "Basic Diagnostic Strips", 80, 500, 35.0),
            ("IN-AP-VSP-ANA", "ORS Hydration Pouches", 120, 1000, 85.0),
            ("IN-AP-VZM-GJM", "Basic Diagnostic Strips", 12, 100, 14.5),
            ("IN-AP-VZM-CHB", "Paracetamol 500mg Tab", 50, 1500, 110.0),
            ("IN-AP-SKL-RUR", "Anti-Viral Medical Kits", 450, 100, 15.0),
            ("IN-AP-SKL-PLM", "Emergency Medical Kit A", 3, 25, 2.8)
        ])
        
        # 👤 SEED 6: AUTOMATED 100-PATIENT HIGH-DENSITY TRIAGE RECORD ENGINE
        first_names = ["Ramesh", "Suresh", "Venkat", "Chiranjeevi", "Naidu", "Satish", "Anitha", "Lakshmi", "Durga", "Rama"]
        last_names = ["Pilla", "Kona", "Ganti", "Vanka", "Reddy", "Allu", "Yerra", "Boni", "Koppula", "Myla"]
        symptom_pool = ["High Fever, Continuous Dry Cough", "Acute Diarrhea, Dehydration", "Persistent Dry Cough, Sore Throat"]
        patient_records = []
        for i in range(1, 101):
            token_id = f"AP-SEED-{1000 + i}"
            selected_node = random.choice(nodes)
            p_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            aadhaar_mock = str(random.randint(100000000000, 999999999999))
            phone_mock = f"+919{random.randint(10000000, 99999999)}"
            logged_symptoms = random.choice(symptom_pool)
            patient_records.append((token_id, selected_node[0], str(hash(aadhaar_mock)), phone_mock, f"Patient: {p_name} | {logged_symptoms}", "COMPLETED"))
        cursor.executemany("INSERT INTO patient_triage_queue VALUES (?, ?, ?, ?, ?, ?);", patient_records)
        
        cursor.executemany("INSERT INTO node_operations VALUES (?, ?, ?, ?);", [
            ("IN-AP-VSP-PND", 40, 35, 0.88), ("IN-AP-VSP-BHM", 30, 5, 0.12), ("IN-AP-VSP-GJV", 25, 20, 0.35),
            ("IN-AP-VSP-ANA", 50, 42, 0.65), ("IN-AP-VZM-GJM", 15, 2, 0.42), ("IN-AP-VZM-CHB", 20, 18, 0.11),
            ("IN-AP-VZM-SKR", 10, 9, 0.73), ("IN-AP-SKL-RUR", 20, 18, 0.76), ("IN-AP-SKL-PLM", 35, 30, 0.22), ("IN-AP-SKL-TKK", 30, 12, 0.05)
        ])
    conn.commit()
    conn.close()

init_ap_pilot_db()
# ==========================================
# PRESENTATION LAYER & LOCATION CASCADE
# ==========================================
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "user_role" not in st.session_state: st.session_state.user_role = None
if "node_id" not in st.session_state: st.session_state.node_id = None
if "current_lang" not in st.session_state: st.session_state.current_lang = "en"

if not st.session_state.authenticated:
    st.sidebar.markdown("### 🗺️ Pilot Location Router")
    selected_lang_name = st.sidebar.radio("Language / భాష", list(LANGUAGE_NAME_MAP.values()), horizontal=True)
    for code, name in LANGUAGE_NAME_MAP.items():
        if name == selected_lang_name: st.session_state.current_lang = code
    ln = LOCALIZATION_DATA[st.session_state.current_lang]
    
    conn = sqlite3.connect("smart_health.db")
    
    # Extract string values safely out of the 1-element tuples from SQLite
    dist_list = [row[0] for row in conn.execute("SELECT DISTINCT district_name FROM administrative_hierarchy").fetchall()]
    chosen_district = st.sidebar.selectbox(ln["select_district"], dist_list)
    
    fac_cursor = conn.execute("SELECT node_name, node_id FROM administrative_hierarchy WHERE district_name = ?", (chosen_district,)).fetchall()
    
    if fac_cursor:
        facility_map = {name: node_id for name, node_id in fac_cursor}
    else:
        facility_map = {"No Facilities Found": "NONE"}
        
    chosen_facility_name = st.sidebar.selectbox(ln["select_facility"], list(facility_map.keys()))
    target_node_id = facility_map[chosen_facility_name]
    
    # Fetch personnel details securely and extract string elements out of single-item tuples
    doc_rows = [r[0] for r in conn.execute("SELECT doctor_name FROM doctors WHERE node_id = ?", (target_node_id,)).fetchall()]
    asha_rows = {r[0]: r[1] for r in conn.execute("SELECT username, worker_name FROM asha_workers WHERE node_id = ?", (target_node_id,)).fetchall()}
    pharma_rows = {r[0]: r[1] for r in conn.execute("SELECT username, employee_name FROM pharmacists WHERE node_id = ?", (target_node_id,)).fetchall()}
    conn.close()
    
    st.sidebar.markdown(f"**🩺 Connected On-Duty Clinicians:**")
    for d in doc_rows: st.sidebar.caption(f"• {d}")
    st.sidebar.markdown(f"**🎒 Local ASHA Workers assigned here:**")
    for u, n in asha_rows.items(): st.sidebar.caption(f"• {n} (`{u}`)")
    st.sidebar.markdown(f"**💊 Local Pharmacy Store Managers:**")
    for u, n in pharma_rows.items(): st.sidebar.caption(f"• {n} (`{u}`)")

    st.title(ln["login_title"])
    st.caption(f"{ln['login_sub']} | Routing Target: `{target_node_id}`")
    
    # Friendly labels dictionary map for selection purposes
    UI_ROLE_NAME_MAP = {
        "ap_state_admin": "State Surveillance Administrator",
        "district_officer": "District Officer",
        "chc_doctor": "CHC Medical Practitioner (Default Doctor Account)",
        "asha_worker": "ASHA Community Worker (Default ASHA Account)",
        "pharma_person": "Pharmacist Store Manager (Default Pharma Account)"
    }
    
    username_options = list(UI_ROLE_NAME_MAP.values())
    selected_ui_name = st.selectbox(ln["username"], username_options)
    
    # Corrected: Safely extract the matching string using list comprehension item extraction [0]
    user_in_list = [k for k, v in UI_ROLE_NAME_MAP.items() if v == selected_ui_name]
    user_in = user_in_list[0] if user_in_list else "unknown"
    pass_in = st.text_input(ln["password"], type="password")
    
    if st.button(ln["btn_login"]):
        is_authenticated = False
        resolved_role = ""
        
        if user_in in USER_REGISTRY and USER_REGISTRY[user_in]["password"] == pass_in:
            is_authenticated = True
            resolved_role = USER_REGISTRY[user_in]["role"]
        elif user_in == "chc_doctor" and pass_in == "MedicalDoc123":
            is_authenticated = True
            resolved_role = "CHC Medical Practitioner"
        elif user_in == "asha_worker" and pass_in == "VillageASHA456":
            is_authenticated = True
            resolved_role = "ASHA Community Worker"
        elif user_in == "pharma_person" and pass_in == "PharmaStore456":
            is_authenticated = True
            resolved_role = "Pharmacist"
            
        if is_authenticated:
            st.session_state.authenticated = True
            st.session_state.user_role = resolved_role
            st.session_state.node_id = target_node_id
            log_transaction(st.session_state.user_role, st.session_state.node_id, "LOGIN", f"User account [{user_in}] authenticated successfully.")
            st.rerun()
        else:
            st.error("Invalid Credentials / తప్పుడు పాస్‌వర్డ్")
# ==========================================
# AUTHENTICATED SYSTEM ENVIRONMENT ROUTER
# ==========================================
else:
    ln = LOCALIZATION_DATA[st.session_state.current_lang]
    role = st.session_state.user_role
    node = st.session_state.node_id
    
    st.sidebar.markdown(f"### 👤 {ln['sidebar_session']}: **{role}**")
    st.sidebar.caption(f"📍 Node Code: `{node}`")
    
    if st.sidebar.button(ln["btn_logout"]):
        log_transaction(role, node, "LOGOUT", "Session workspace cleanly terminated.")
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.node_id = None
        st.clear()
        st.rerun()

    st.title(ln["title"])

    # 🏢 ENVIRONMENT 1: MANAGEMENT DASHBOARDS (Admin Views)
    if role in ["State Surveillance", "District Officer"]:
        st.header(ln["facility_status"])
        df_inv, transfers = run_cross_tier_supply_balancing()
        
        st.subheader("🚨 Outbreak Surveillance Tracker Logs")
        conn = sqlite3.connect("smart_health.db")
        anomalies = pd.read_sql_query("SELECT h.node_name, o.active_epidemic_risk_score FROM node_operations o JOIN administrative_hierarchy h ON o.node_id = h.node_id WHERE o.active_epidemic_risk_score > 0.5", conn)
        conn.close()
        
        for _, alert in anomalies.iterrows():
            st.error(f"🔴 **CRITICAL OUTBREAK WARNING**: PHC Node `{alert['node_name']}` has triggered an epidemic warning score of **{alert['active_epidemic_risk_score']}**! Dispatch response teams.")
        
        # Matplotlib Rendering Framework Hooks
        st.markdown("---")
        st.subheader("📊 Executive Data Visualizations (Matplotlib Renderers)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(generate_stock_prediction_chart(df_inv))
        with col2:
            st.pyplot(generate_epidemic_risk_chart())
        st.markdown("---")
        
        # Dynamic Aerial Drone Management
        st.subheader(ln["redistribution"])
        if transfers:
            for t in transfers:
                st.warning(f"📦 **AI Aero Optimization**: Move **{t['quantity']} units** of `{t['item']}` from **{t['from_center']}** ➡️ **{t['to_node']}**.")
                if st.button(f"🚀 Authorize Quadcopter Flight Path", key=t['to_node']):
                    log_transaction(role, node, "DRONE_LAUNCH", f"Launched supply drone flight paths to {t['to_node']}.")
                    st.success("Logistics dispatch active.")
            st.map(map_cross_tier_drone_grid(transfers))
        else:
            st.success("All pilot health inventory assets balanced smoothly.")

        # Protected Compliance Ledger Review Screen
        st.markdown("---")
        st.header("🔒 Integrated Action Ledger (Admin-Eyes Only)")
        conn = sqlite3.connect("smart_health.db")
        st.dataframe(pd.read_sql_query("SELECT timestamp, user_role, node_id, action_type, details FROM system_audit_logs ORDER BY timestamp DESC", conn), use_container_width=True)
        conn.close()

    # 🩺 ENVIRONMENT 2: FRONTLINE CLINICAL OPERATIONS (CHC / ASHA Logs)
    elif role in ["CHC Medical Practitioner", "ASHA Community Worker"]:
        st.header("Clinical Triage Portal")
        conn = sqlite3.connect("smart_health.db")
        
        # Fetch active doctors for the select list mapping box
        docs_query = conn.execute("SELECT doctor_name FROM doctors WHERE node_id = ?", (node,)).fetchall()
        available_doctors = [d[0] for d in docs_query] if docs_query else ["General OPD Pool"]
        
        # 🎒 BRANCH 2A: UNIQUE PATH IF LOGGED IN AS ASHA WORKER (Intake Logger with Doctor Assignment)
        if role == "ASHA Community Worker":
            st.subheader("Patient Intake Logger & Doctor Assignment")
            st.caption("Register citizens and triage select routing to on-shift medical practitioners.")
            
            p_phone = st.text_input("Patient Contact Mobile Link (WhatsApp Enabled)", value="+91")
            aadhaar = st.text_input("Secure Aadhaar Entry (12 Digits)")
            
            # 🎯 RESOLVED: Interactive Dropdown allowing ASHA to assign the case directly to an available doctor
            assigned_doctor = st.selectbox("Assign Target Medical Practitioner / Doctor", available_doctors)
            symptoms = st.text_area("Log Symptoms Profile Data")
            
            if st.button("Submit Triage Logs & Assign Case"):
                if len(aadhaar) == 12 and symptoms:
                    token_id = f"AP-{datetime.datetime.now().strftime('%M%S')}"
                    
                    # Store data fields with explicit doctor routing context appended to descriptions
                    combined_symptoms_log = f"Assigned to: {assigned_doctor} | Symptoms: {symptoms}"
                    
                    conn.execute("INSERT INTO patient_triage_queue VALUES (?, ?, ?, ?, ?, 'WAITING')", 
                                 (token_id, node, str(hash(aadhaar)), p_phone, combined_symptoms_log))
                    conn.commit()
                    log_transaction(role, node, "PATIENT_INTAKE", f"ASHA created token {token_id} assigned to {assigned_doctor}")
                    st.success(f"🎉 Patient Registered Successfully! Token Issued: **{token_id}** and routed cleanly to **{assigned_doctor}**.")
                else:
                    st.error("Invalid formatting requirements. Ensure Aadhaar is exactly 12 digits.")

        # 🩺 BRANCH 2B: UNIQUE PATH IF LOGGED IN AS CHC MEDICAL PRACTITIONER (Doctor Queue Portal)
        elif role == "CHC Medical Practitioner":
            st.subheader("Personal Triage Consultation Queue")
            
            # Read only waiting patient lists from database
            queue_df = pd.read_sql_query("SELECT token_id, patient_phone, symptoms_logged FROM patient_triage_queue WHERE node_id=? AND status='WAITING'", conn, params=(node,))
            st.dataframe(queue_df)
            
            if not queue_df.empty:
                # Target first patient in the database index row
                target_patient = queue_df.iloc[0]
                whatsapp_link = build_esanjeevani_routing_gateway(target_patient['patient_phone'], "Active Assigned Duty Doctor")
                
                st.info(f"👉 **Processing Case Key**: {target_patient['token_id']} | {target_patient['symptoms_logged']}")
                st.link_button("📞 Launch Instant Telehealth Video Consultation", whatsapp_link, type="primary")
                
                if st.button("✅ Complete Session & Advance Queue"):
                    conn.execute("UPDATE patient_triage_queue SET status='COMPLETED' WHERE token_id=?", (target_patient['token_id'],))
                    conn.commit()
                    log_transaction(role, node, "TELEHEALTH_CALL", f"Completed session for {target_patient['token_id']}")
                    st.success("Session saved.")
                    st.rerun()
                    
        # Renders the high-density historical registries below forms
        st.markdown("---")
        st.subheader("📚 Historical Patient Electronic Health Records (EHR Ledger)")
        history_df = pd.read_sql_query("SELECT token_id, symptoms_logged as 'Demographics & Symptoms Profile', status as 'Care Status' FROM patient_triage_queue WHERE node_id = ? AND status = 'COMPLETED' LIMIT 100", conn, params=(node,))
        
        if not history_df.empty:
            st.dataframe(history_df, use_container_width=True)
        else:
            st.info("No historical case records found for this specific facility node context.")
        conn.close()

    # 💊 ENVIRONMENT 3: PHARMACIST WORKSPACE
    elif role == "Pharmacist":
        st.header("Pharmacy Stock Management Matrix")
        conn = sqlite3.connect("smart_health.db")
        inv_df = pd.read_sql_query("SELECT item_name, current_stock, min_required_threshold FROM inventory WHERE node_id=?", conn, params=(node,))
        st.dataframe(inv_df)
        
        if not inv_df.empty:
            med_to_dispense = st.selectbox("Select Drug Asset for Patient Distribution", inv_df['item_name'].tolist())
            if st.button("Single-Click Asset Dispense"):
                conn.execute("UPDATE inventory SET current_stock = current_stock - 1 WHERE node_id=? AND item_name=?", (node, med_to_dispense))
                conn.commit()
                log_transaction(role, node, "MEDICINE_DISPENSE", f"Dispensed 1 unit of {med_to_dispense}.")
                st.success(f"Dispersion verified for {med_to_dispense}.")
                st.rerun()
                
        st.subheader("UAV Cargo Intervention")
        low_stock_item = st.selectbox("Request Drone Backup Payload", ["Emergency Medical Kit A", "Paracetamol 500mg Tab"])
        if st.button("⚡ Request Instant Drone Resupply"):
            log_transaction(role, node, "DRONE_REQUEST", f"Requested emergency backup delivery of {low_stock_item}.")
            st.warning("Supply Chain emergency payload request queued onto District Admin telemetry rails.")
        conn.close()
