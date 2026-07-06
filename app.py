import streamlit as st
import pandas as pd
import sqlite3
import datetime
import random
import os

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
    db_file = "smart_health.db"
    
    # Check database status dynamically on startup to clear any legacy 1-district file blocks safely
    if os.path.exists(db_file):
        try:
            conn_test = sqlite3.connect(db_file)
            cursor_test = conn_test.cursor()
            cursor_test.execute("SELECT COUNT(DISTINCT district_name) FROM administrative_hierarchy;")
            count = cursor_test.fetchone()[0]
            conn_test.close()
            if count < 3:
                os.remove(db_file)
        except Exception:
            pass

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS administrative_hierarchy (node_id TEXT PRIMARY KEY, node_level TEXT, node_name TEXT, state_name TEXT, district_name TEXT, latitude REAL, longitude REAL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS doctors (doctor_id TEXT PRIMARY KEY, node_id TEXT, doctor_name TEXT, specialization TEXT, active_status INT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS asha_workers (asha_id TEXT PRIMARY KEY, node_id TEXT, username TEXT, worker_name TEXT, assigned_village TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS pharmacists (pharma_id TEXT PRIMARY KEY, node_id TEXT, username TEXT, employee_name TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS inventory (node_id TEXT, item_name TEXT, current_stock INT, min_required_threshold INT, daily_avg_consumption REAL, PRIMARY KEY (node_id, item_name));")
    cursor.execute("CREATE TABLE IF NOT EXISTS patient_triage_queue (token_id TEXT PRIMARY KEY, node_id TEXT, aadhaar_hash TEXT, patient_phone TEXT, symptoms_logged TEXT, status TEXT);")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patient_prescriptions (
        prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
        token_id TEXT, node_id TEXT, doctor_name TEXT, medication_name TEXT, dosage_instructions TEXT, consult_mode TEXT, status TEXT DEFAULT 'PENDING'
    );""")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS node_operations (node_id TEXT PRIMARY KEY, total_beds INT, occupied_beds INT, active_epidemic_risk_score REAL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS system_audit_logs (log_id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, user_role TEXT, node_id TEXT, action_type TEXT, details TEXT);")
    
    cursor.execute("SELECT COUNT(*) FROM administrative_hierarchy;")
    if cursor.fetchone()[0] == 0:
        # Seeding 10 health facilities across Visakhapatnam, Vizianagaram, and Srikakulam districts
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
        
        cursor.executemany("INSERT INTO asha_workers VALUES (?, ?, ?, ?, ?);", [
            ("ASHA001", "IN-AP-VSP-PND", "asha_worker", "Smt. T. Appalanamma", "Pendurthi Sector 1"),
            ("ASHA002", "IN-AP-VZM-GJM", "asha_gajapathinagaram", "Smt. D. Parvathi", "Gajapathinagaram Ward 4"),
            ("ASHA003", "IN-AP-SKL-RUR", "asha_srikakulam", "Smt. K. Chittemma", "Srikakulam River Block")
        ])

        cursor.executemany("INSERT INTO pharmacists VALUES (?, ?, ?, ?);", [
            ("PHM001", "IN-AP-VSP-PND", "pharma_person", "Sri K. Jagannadham"),
            ("PHM002", "IN-AP-VZM-GJM", "pharma_gajapathinagaram", "Sri R. K. Prasad"),
            ("PHM003", "IN-AP-SKL-RUR", "pharma_srikakulam_rur", "Sri B. Krishna")
        ])
        
        cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?);", [
            ("IN-AP-VSP-PND", "Anti-Viral Medical Kits", 5, 200, 12.5),
            ("IN-AP-VSP-PND", "Paracetamol 500mg Tab", 450, 2000, 150.0),
            ("IN-AP-VSP-BHM", "Anti-Viral Medical Kits", 1800, 300, 22.0),
            ("IN-AP-VZM-GJM", "Basic Diagnostic Strips", 12, 100, 14.5),
            ("IN-AP-VZM-CHB", "Paracetamol 500mg Tab", 50, 1500, 110.0),
            ("IN-AP-SKL-RUR", "Anti-Viral Medical Kits", 450, 100, 15.0),
            ("IN-AP-SKL-PLM", "Emergency Medical Kit A", 3, 25, 2.8)
        ])
        
        patient_records = []
        for i in range(1, 101):
            token_id = f"AP-SEED-{1000 + i}"
            selected_node = random.choice(nodes)[0] # Extract text string ID cleanly
            p_name = f"{random.choice(['Ramesh', 'Suresh', 'Venkat', 'Chiranjeevi', 'Anitha', 'Lakshmi'])} {random.choice(['Pilla', 'Kona', 'Ganti', 'Reddy', 'Allu'])}"
            aadhaar_mock = str(random.randint(100000000000, 999999999999))
            phone_mock = f"+919{random.randint(10000000, 99999999)}"
            logged_symptoms = random.choice(["High Fever, Continuous Dry Cough", "Acute Diarrhea, Dehydration", "Persistent Dry Cough, Sore Throat"])
            patient_records.append((token_id, selected_node, str(hash(aadhaar_mock)), phone_mock, f"Patient: {p_name} | {logged_symptoms}", "COMPLETED"))
        cursor.executemany("INSERT INTO patient_triage_queue VALUES (?, ?, ?, ?, ?, ?);", patient_records)
        
        cursor.executemany("INSERT INTO node_operations VALUES (?, ?, ?, ?);", [
            ("IN-AP-VSP-PND", 40, 35, 0.88), ("IN-AP-VSP-BHM", 30, 5, 0.12), ("IN-AP-VSP-GJV", 25, 20, 0.35), ("IN-AP-VSP-ANA", 50, 42, 0.65), 
            ("IN-AP-VZM-GJM", 15, 2, 0.42), ("IN-AP-VZM-CHB", 20, 18, 0.11), ("IN-AP-VZM-SKR", 10, 9, 0.73), 
            ("IN-AP-SKL-RUR", 20, 18, 0.76), ("IN-AP-SKL-PLM", 35, 30, 0.22), ("IN-AP-SKL-TKK", 30, 12, 0.05)
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
if "user_home_district" not in st.session_state: st.session_state.user_home_district = None
if "selected_district" not in st.session_state: st.session_state.selected_district = None

if not st.session_state.authenticated:
    st.sidebar.markdown("### 🗺️ Pilot Location Router")
    selected_lang_name = st.sidebar.radio("Language / భాష", list(LANGUAGE_NAME_MAP.values()), horizontal=True)
    for code, name in LANGUAGE_NAME_MAP.items():
        if name == selected_lang_name: st.session_state.current_lang = code
    ln = LOCALIZATION_DATA[st.session_state.current_lang]
    
    conn = sqlite3.connect("smart_health.db")
    dist_list = [row for row in conn.execute("SELECT DISTINCT district_name FROM administrative_hierarchy").fetchall()]
    chosen_district = st.sidebar.selectbox(ln["select_district"], dist_list)
    st.session_state.selected_district = chosen_district
    
    fac_cursor = conn.execute("SELECT node_name, node_id FROM administrative_hierarchy WHERE district_name = ?", (chosen_district,)).fetchall()
    facility_map = {node_name: node_id for node_name, node_id in fac_cursor}
    chosen_facility_name = st.sidebar.selectbox(ln["select_facility"], list(facility_map.keys()))
    target_node_id = facility_map[chosen_facility_name]
    
    # Fetch personnel details securely and extract string elements safely
    doc_rows = [r for r in conn.execute("SELECT doctor_name FROM doctors WHERE node_id = ?", (target_node_id,)).fetchall()]
    asha_rows = {r: r for r in conn.execute("SELECT username, worker_name FROM asha_workers WHERE node_id = ?", (target_node_id,)).fetchall()}
    pharma_rows = {r: r for r in conn.execute("SELECT username, employee_name FROM pharmacists WHERE node_id = ?", (target_node_id,)).fetchall()}
    conn.close()
    
    st.sidebar.markdown(f"**🩺 Connected On-Duty Clinicians:**")
    for d in doc_rows: st.sidebar.caption(f"• {d}")
    st.sidebar.markdown(f"**🎒 Local ASHA Workers assigned here:**")
    for u, n in asha_rows.items(): st.sidebar.caption(f"• {n} (`{u}`)")
    st.sidebar.markdown(f"**💊 Local Pharmacy Store Managers:**")
    for u, n in pharma_rows.items(): st.sidebar.caption(f"• {n} (`{u}`)")

    st.title(ln["login_title"])
    st.caption(f"{ln['login_sub']} | Routing Target: `{target_node_id}`")
    
    # Render visible, human-readable display list inside select box mapping accounts cleanly
    username_options = list(USER_REGISTRY.keys())
    user_in = st.selectbox(ln["username"], username_options)
    pass_in = st.text_input(ln["password"], type="password")
    
    if st.button(ln["btn_login"]):
        if user_in in USER_REGISTRY and USER_REGISTRY[user_in]["password"] == pass_in:
            st.session_state.authenticated = True
            st.session_state.user_role = USER_REGISTRY[user_in]["role"]
            st.session_state.node_id = target_node_id
            st.session_state.user_home_district = USER_REGISTRY[user_in]["home_district"]
            
            log_transaction(st.session_state.user_role, st.session_state.node_id, "LOGIN", f"User {user_in} logged into district context.")
            st.rerun()
        else:
            st.error("Invalid Credentials / తప్పుడు పాస్‌వర్డ్")
# ==========================================
# ADMINISTRATIVE TIERS HUB VIEW
# ==========================================
else:
    ln = LOCALIZATION_DATA[st.session_state.current_lang]
    role = st.session_state.user_role
    node = st.session_state.node_id
    home_dist = st.session_state.user_home_district
    curr_dist = st.session_state.selected_district

    if st.sidebar.button(ln["btn_logout"]):
        log_transaction(role, node, "LOGOUT", "Session workspace cleanly terminated.")
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.node_id = None
        st.session_state.clear()
        st.rerun()

    st.title(ln["title"])

    if role in ["State Surveillance", "District Officer"]:
        st.header(ln["facility_status"])
        df_inv, transfers = run_cross_tier_supply_balancing()
        
        # 🎯 SCOPE ENFORCEMENT MATRIX FOR NEW DISTRICT ACCOUNTS:
        # If the logged-in user is a specialized District Officer, filter down data outputs strictly to their domain match pattern.
        if role == "District Officer":
            st.warning(f"📋 **District Officer Monitoring Active. Domain Scope Restriction**: `{home_dist}`")
            df_inv = df_inv[df_inv['district_name'] == home_dist]
            transfers = [t for t in transfers if t['to_node'].startswith(node)]
        else:
            st.success("👑 **State Surveillance Admin Mode Active: Tracking All District Matrices (Visakhapatnam, Vizianagaram, Srikakulam)**")
            
        st.subheader("🚨 Outbreak Surveillance Tracker Logs")
        conn = sqlite3.connect("smart_health.db")
        
        if role == "District Officer":
            anomalies = pd.read_sql_query("""
                SELECT h.node_name, o.active_epidemic_risk_score 
                FROM node_operations o 
                JOIN administrative_hierarchy h ON o.node_id = h.node_id 
                WHERE o.active_epidemic_risk_score > 0.5 AND h.district_name = ?
            """, conn, params=(home_dist,))
        else:
            anomalies = pd.read_sql_query("""
                SELECT h.node_name, o.active_epidemic_risk_score 
                FROM node_operations o 
                JOIN administrative_hierarchy h ON o.node_id = h.node_id 
                WHERE o.active_epidemic_risk_score > 0.5
            """, conn)
        conn.close()
        
        if not anomalies.empty:
            for _, alert in anomalies.iterrows():
                st.error(f"🔴 **CRITICAL OUTBREAK WARNING**: PHC Node `{alert['node_name']}` has triggered an epidemic warning score of **{alert['active_epidemic_risk_score']}**!")
        else:
            st.success("No critical syndromic outbreak alerts reported within your jurisdiction scope.")
        
        # Matplotlib Rendering Framework Hooks
        st.markdown("---")
        st.subheader("📊 Executive Data Visualizations (Matplotlib Renderers)")
        col1, col2 = st.columns(2)
        with col1:
            if not df_inv.empty:
                st.pyplot(generate_stock_prediction_chart(df_inv))
            else:
                st.info("No stock data available for the targeted filtering parameters.")
        with col2:
            st.pyplot(generate_epidemic_risk_chart())
        st.markdown("---")
        
        st.subheader(ln["redistribution"])
        if transfers:
            for t in transfers:
                st.warning(f"📦 **AI Aero Optimization**: Move **{t['quantity']} units** of `{t['item']}` from **{t['from_center']}** ➡️ **{t['to_node']}**.")
                if st.button(f"🚀 Authorize Quadcopter Flight Path", key=t['to_node']):
                    log_transaction(role, node, "DRONE_LAUNCH", f"Launched supply drone flight paths to {t['to_node']}.")
                    st.success("Logistics dispatch active.")
            st.map(map_cross_tier_drone_grid(transfers))
        else:
            st.success("All local area health inventory assets balanced smoothly.")

        # Protected Compliance Ledger Review Screen
        st.markdown("---")
        st.header("🔒 Integrated Action Ledger (Admin-Eyes Only)")
        conn = sqlite3.connect("smart_health.db")
        if role == "District Officer":
            st.dataframe(pd.read_sql_query("SELECT timestamp, user_role, node_id, action_type, details FROM system_audit_logs WHERE node_id LIKE ? ORDER BY timestamp DESC", conn, params=(f"%{home_dist[:3].upper()}%",)), use_container_width=True)
        else:
            st.dataframe(pd.read_sql_query("SELECT timestamp, user_role, node_id, action_type, details FROM system_audit_logs ORDER BY timestamp DESC", conn), use_container_width=True)
        conn.close()

    # Pharmacy Fulfillment Deck
    elif role == "Pharmacist":
        st.header("Pharmacy Stock & Fulfillment Desk")
        pharma_mode = st.radio("Select Active Inventory Distribution Mode", ["Local Counter Dispensation", "Drone-Routed Aero Resupply Operations"], horizontal=True)
        
        st.subheader("📥 Inbound Doctor Prescriptions Ledger")
        conn = sqlite3.connect("smart_health.db")
        rx_df = pd.read_sql_query("SELECT prescription_id, token_id, doctor_name, medication_name, dosage_instructions, consult_mode FROM patient_prescriptions WHERE node_id=? AND status='PENDING'", conn, params=(node,))
        st.dataframe(rx_df)
        
        if not rx_df.empty:
            target_rx = rx_df.iloc[0]
            st.markdown(f"### 🎯 Active Target Order: **Prescription ID {target_rx['prescription_id']}**")
            st.info(f"Patient Token: **{target_rx['token_id']}** | Medication: **{target_rx['medication_name']}** | Channel: **{target_rx['consult_mode']}**")
            
            if pharma_mode == "Local Counter Dispensation":
                if st.button("💊 Process Single-Click Local Counter Dispense"):
                    conn.execute("UPDATE inventory SET current_stock = current_stock - 1 WHERE node_id=? AND item_name=?", (node, target_rx['medication_name']))
                    conn.execute("UPDATE patient_prescriptions SET status='DISPENSED' WHERE prescription_id=?", (int(target_rx['prescription_id']),))
                    conn.commit()
                    log_transaction(role, node, "MEDICINE_DISPENSE", f"Dispensed prescription ID {target_rx['prescription_id']} locally.")
                    st.success("Prescription fulfilled over the counter successfully!")
                    st.rerun()
            else:
                st.warning(f"Aero Deployment Active: Patient consulted via **{target_rx['consult_mode']}**.")
                if st.button("🚀 Authorize Autonomous Drone Resupply Delivery"):
                    conn.execute("UPDATE inventory SET current_stock = current_stock - 1 WHERE node_id=? AND item_name=?", (node, target_rx['medication_name']))
                    conn.execute("UPDATE patient_prescriptions SET status='DRONE_DISPATCHED' WHERE prescription_id=?", (int(target_rx['prescription_id']),))
                    conn.commit()
                    log_transaction(role, node, "DRONE_DISPATCH", f"Dispatched prescription ID {target_rx['prescription_id']} via quadcopter drone.")
                    st.success("UAV Flight path calculated. Supply drone dispatched successfully to target destination!")
                    st.rerun()
        else:
            st.success("All clinical orders processed. No pending prescriptions.")
        conn.close()
