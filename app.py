# app.py
import streamlit as st
import pandas as pd
import sqlite3
import os
import src.predictive_engine as engine

# 🛠️ AUTOMATED ON-LAUNCH DATABASE CHECK ENGINE (Prevents DatabaseErrors)
if not os.path.exists("data/smart_health.db") or os.path.getsize("data/smart_health.db") == 0:
    try:
        import seed_mock_data
        seed_mock_data.execute_seeding_pipeline()
    except Exception as e:
        st.error(f"Critical Database Initialization Failure: {str(e)}")

st.set_page_config(layout="wide", page_title="Bharat Health AI Command")

# Custom AP Government Branding Styling Banner
st.markdown("""
    <div style='background-color:#003A70;padding:15px;border-radius:10px;margin-bottom:20px'>
        <h1 style='color:white;margin:0;font-family:sans-serif;'>🌐 Bharat Health AI: Multi-District Aero-Logistics Network</h1>
        <p style='color:#FFC107;margin:5px 0 0 0;'>Track 3: Smart Health Deployment Node — Andhra Pradesh Pilot</p>
    </div>
""", unsafe_allow_html=True)

# 1. District Selection Context Filter Sidebar
st.sidebar.header("📍 Regional Jurisdiction Matrix")
district_options = ["All Districts", "Visakhapatnam", "Vizianagaram", "Srikakulam"]
selected_district = st.sidebar.selectbox("Select Surveillance Scope", district_options)

# 2. Extract Data Telemetry from your schema structure
inventory_df, calculated_transfers = engine.run_cross_tier_supply_balancing()

if selected_district != "All Districts":
    inventory_df = inventory_df[inventory_df['district_name'] == selected_district]

# 3. Render Visual Analytics Side-by-Side
col1, col2 = st.columns(2)
with col1:
    if not inventory_df.empty:
        st.pyplot(engine.generate_stock_prediction_chart(inventory_df))
    else:
        st.info("No active inventory records found for this district.")

with col2:
    st.pyplot(engine.generate_epidemic_risk_chart(selected_district))

st.markdown("---")

# 4. Display Real-Time Triage Queues and Clinical Personnel Metrics
col_left, col_right = st.columns()

with col_left:
    st.subheader("📋 Active Patient Triage Logs (Aadhaar Hashed)")
    conn = sqlite3.connect("data/smart_health.db")
    triage_query = """
        SELECT t.token_id, h.node_name, t.symptoms_logged, t.status, h.district_name
        FROM patient_triage_queue t
        JOIN administrative_hierarchy h ON t.node_id = h.node_id
    """
    triage_df = pd.read_sql_query(triage_query, conn)
    conn.close()
    
    if selected_district != "All Districts":
        triage_df = triage_df[triage_df['district_name'] == selected_district]
    
    st.dataframe(triage_df[['token_id', 'node_name', 'symptoms_logged', 'status']], use_container_width=True, hide_index=True)

with col_right:
    st.subheader("👨‍⚕️ Medical Practitioner Attendance")
    conn = sqlite3.connect("data/smart_health.db")
    doc_query = """
        SELECT d.doctor_name, h.node_name, d.specialization, 
               CASE WHEN d.active_status = 1 THEN '🟢 Present' ELSE '🔴 Absent' END as Duty_Status,
               h.district_name
        FROM doctors d
        JOIN administrative_hierarchy h ON d.node_id = h.node_id
    """
    doc_df = pd.read_sql_query(doc_query, conn)
    conn.close()
    
    if selected_district != "All Districts":
        doc_df = doc_df[doc_df['district_name'] == selected_district]
        
    st.dataframe(doc_df[['doctor_name', 'node_name', 'Duty_Status']], use_container_width=True, hide_index=True)

st.markdown("---")

# 5. Secure Admin Gateway for Gemini AI Engine
st.subheader("🤖 Gemini 2.5 Flash Autonomous Intervention Planner")

typed_password = st.text_input(
    "🔑 Enter Password to Unlock AI Dispatch Engine", 
    type="password",
    placeholder="••••••••••••",
    help="Type the shared access password to activate the operational forecast module."
)

if st.button("✨ Generate AI Strategic Operational Mandate"):
    if typed_password == st.secrets["APP_ACCESS_PASSWORD"]:
        with st.spinner("Access Granted. Analyzing operational bottlenecks via Gemini..."):
            
            real_key = st.secrets["GEMINI_API_KEY"]
            ai_payload = engine.generate_district_health_forecast(real_key, inventory_df, calculated_transfers)
            
            if ai_payload:
                st.warning(f"📋 **Administrative Bulletin:** {ai_payload.get('early_warning_bulletin', 'No broadcast generated.')}")
                
                st.subheader("✈️ Autonomous Aero-Resupply Flight Log Manifest")
                manifest_list = ai_payload.get('drone_flight_manifest', [])
                if manifest_list:
                    st.dataframe(manifest_list, use_container_width=True, hide_index=True)
                    st.success("🤖 Flight logs compiled successfully. Ready to transmit coordinates.")
                else:
                    st.info("No active emergencies detected. Supply reserves are within healthy thresholds.")
    elif typed_password == "":
        st.error("Access Denied: Please input the shared access password.")
    else:
        st.error("❌ Invalid Password! This unauthorized attempt has been logged to your system audit trails.")
        engine.log_audit_breach(typed_password)
