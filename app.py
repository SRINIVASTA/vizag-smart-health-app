import streamlit as st
import pandas as pd
import sqlite3
import datetime

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
    cursor.execute("CREATE TABLE IF NOT EXISTS inventory (node_id TEXT, item_name TEXT, current_stock INT, min_required_threshold INT, daily_avg_consumption REAL, PRIMARY KEY (node_id, item_name));")
    cursor.execute("CREATE TABLE IF NOT EXISTS patient_triage_queue (token_id TEXT PRIMARY KEY, node_id TEXT, aadhaar_hash TEXT, patient_phone TEXT, symptoms_logged TEXT, status TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS node_operations (node_id TEXT PRIMARY KEY, total_beds INT, occupied_beds INT, active_epidemic_risk_score REAL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS system_audit_logs (log_id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, user_role TEXT, node_id TEXT, action_type TEXT, details TEXT);")
    
    cursor.execute("SELECT COUNT(*) FROM administrative_hierarchy;")
    if cursor.fetchone() == 0:
        cursor.executemany("INSERT INTO administrative_hierarchy VALUES (?, ?, ?, ?, ?, ?, ?);", [
            ("IN-AP-VSP-PND", "Tehsil", "Pendurthi CHC Hub", "Andhra Pradesh", "Visakhapatnam", 17.8344, 83.2014),
            ("IN-AP-VSP-BHM", "Tehsil", "Bheemili Hospital Spoke", "Andhra Pradesh", "Visakhapatnam", 17.8903, 83.4447),
            ("IN-AP-VZM-GJM", "Tehsil", "Gajapathinagaram PHC", "Andhra Pradesh", "Vizianagaram", 18.2750, 83.3314),
            ("IN-AP-SKL-RUR", "Tehsil", "Srikakulam Rural Health Center", "Andhra Pradesh", "Srikakulam", 18.2949, 83.8938)
        ])
        cursor.executemany("INSERT INTO doctors VALUES (?, ?, ?, ?, ?);", [
            ("DOC001", "IN-AP-VSP-PND", "Dr. S. Srinivasa Rao", "General Medicine", 1),
            ("DOC002", "IN-AP-VSP-BHM", "Dr. A. Lakshmi Prasanna", "Pediatrics", 1),
            ("DOC003", "IN-AP-VZM-GJM", "Dr. Ch. Koteswara Rao", "Family Physician", 1),
            ("DOC004", "IN-AP-SKL-RUR", "Dr. K. Venkataswamy", "Epidemiology Specialist", 1)
        ])
        cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?);", [
            ("IN-AP-VSP-PND", "Anti-Viral Medical Kits", 5, 200, 12.5),
            ("IN-AP-VSP-BHM", "Anti-Viral Medical Kits", 1800, 300, 22.0),
            ("IN-AP-VZM-GJM", "Basic Diagnostic Strips", 12, 100, 14.5),
            ("IN-AP-SKL-RUR", "Anti-Viral Medical Kits", 450, 100, 15.0)
        ])
        cursor.executemany("INSERT INTO node_operations VALUES (?, ?, ?, ?);", [
            ("IN-AP-VSP-PND", 40, 35, 0.88),
            ("IN-AP-VSP-BHM", 30, 5, 0.12),
            ("IN-AP-VZM-GJM", 15, 2, 0.42),
            ("IN-AP-SKL-RUR", 20, 18, 0.76)
        ])
    conn.commit()
    conn.close()

init_ap_pilot_db()

# State memory management initial patterns
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "user_role" not in st.session_state: st.session_state.user_role = None
if "node_id" not in st.session_state: st.session_state.node_id = None
if "current_lang" not in st.session_state: st.session_state.current_lang = "en"

# Location Router & Language Resolution Interface
if not st.session_state.authenticated:
    st.sidebar.markdown("### 🗺️ Pilot Location Router")
    st.sidebar.info("📍 Active State Layer: **Andhra Pradesh**")
    
    selected_lang_name = st.sidebar.radio("Language / భాష", list(LANGUAGE_NAME_MAP.values()), horizontal=True)
    for code, name in LANGUAGE_NAME_MAP.items():
        if name == selected_lang_name: st.session_state.current_lang = code
            
    ln = LOCALIZATION_DATA[st.session_state.current_lang]
    
    conn = sqlite3.connect("smart_health.db")
    dist_list = [row[0] for row in conn.execute("SELECT DISTINCT district_name FROM administrative_hierarchy").fetchall()]
    chosen_district = st.sidebar.selectbox(ln["select_district"], dist_list)
    
    fac_cursor = conn.execute("SELECT node_name, node_id FROM administrative_hierarchy WHERE district_name = ?", (chosen_district,)).fetchall()
    # FIX: Explicitly unpack the query row tuple into string keys and values
    facility_map = {row[0]: row[1] for row in fac_cursor}
    
    chosen_facility_name = st.sidebar.selectbox(ln["select_facility"], list(facility_map.keys()))
    target_node_id = facility_map[chosen_facility_name]
    
    doc_rows = conn.execute("SELECT doctor_name, specialization FROM doctors WHERE node_id = ? AND active_status = 1", (target_node_id,)).fetchall()
    conn.close()
    
    st.sidebar.markdown(f"**🩺 {ln['avail_docs']}:**")
    for d in doc_rows: st.sidebar.caption(f"• {d[0]} ({d[1]})")

    st.title(ln["login_title"])
    st.caption(f"{ln['login_sub']} | Routing Target: `{target_node_id}`")
    user_in = st.text_input(ln["username"])
    pass_in = st.text_input(ln["password"], type="password")
    
    if st.button(ln["btn_login"]):
        if user_in in USER_REGISTRY and USER_REGISTRY[user_in]["password"] == pass_in:
            st.session_state.authenticated = True
            st.session_state.user_role = USER_REGISTRY[user_in]["role"]
            st.session_state.node_id = target_node_id
            log_transaction(st.session_state.user_role, st.session_state.node_id, "LOGIN", "Logged into Andhra Pradesh pilot matrix.")
            st.rerun()
        else:
            st.error("Invalid Credentials / తప్పుడు వివరాలు")
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
        st.rerun()

    st.title(ln["title"])

    # 🏢 ENVIRONMENT 1: MANAGEMENT DASHBOARDS (State / District Controls)
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
            stock_fig = generate_stock_prediction_chart(df_inv)
            st.pyplot(stock_fig)
        with col2:
            risk_fig = generate_epidemic_risk_chart()
            st.pyplot(risk_fig)
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
        
        docs_df = pd.read_sql_query("SELECT doctor_name, specialization, active_status FROM doctors WHERE node_id = ?", conn, params=(node,))
        st.dataframe(docs_df)
        
        st.subheader("Patient Intake Logger")
        p_phone = st.text_input("Patient Contact Mobile Link", value="+91")
        aadhaar = st.text_input("Secure Aadhaar Entry")
        symptoms = st.text_area("Log Symptoms Profile Data")
        
        if st.button("Submit Triage Logs & Open Session"):
            if len(aadhaar) == 12 and symptoms:
                token_id = f"AP-{datetime.datetime.now().strftime('%M%S')}"
                conn.execute("INSERT INTO patient_triage_queue VALUES (?, ?, ?, ?, ?, 'WAITING')", (token_id, node, hash(aadhaar), p_phone, symptoms))
                conn.commit()
                log_transaction(role, node, "PATIENT_INTAKE", f"Logged triage token {token_id}")
                
                if not docs_df.empty:
                    whatsapp_link = build_esanjeevani_routing_gateway(p_phone, docs_df.iloc['doctor_name'])
                    st.success(f"Patient Added! Token Issued: **{token_id}**")
                    st.link_button("📞 Launch Instant Telehealth Session", whatsapp_link, type="primary")
            else:
                st.error("Invalid formatting requirements.")
        conn.close()
