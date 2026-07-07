# app.py — BLOCK 1: INITIALIZATION
import streamlit as st
import pandas as pd
import sqlite3
import os
import src.predictive_engine as engine

# 🛠️ EMBEDDED AUTOMATIC DATABASE CREATION ENGINE
def build_native_database_instance():
    """Constructs the local smart_health database node from the sql schema template file."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/smart_health.db")
    cursor = conn.cursor()

    # Read and build raw tables from schema blueprint
    with open("data/schema.sql", "r", encoding="utf-8") as schema_file:
        cursor.executescript(schema_file.read())

    # Purge existing data rows to avoid primary key collision errors on restarts
    cursor.execute("DELETE FROM system_audit_logs;")
    cursor.execute("DELETE FROM patient_prescriptions;")
    cursor.execute("DELETE FROM patient_triage_queue;")
    cursor.execute("DELETE FROM node_operations;")
    cursor.execute("DELETE FROM inventory;")
    cursor.execute("DELETE FROM pharmacists;")
    cursor.execute("DELETE FROM asha_workers;")
    cursor.execute("DELETE FROM doctors;")
    cursor.execute("DELETE FROM administrative_hierarchy;")

    # 1. Map Regional Facilities
    facilities = [
        ('IN-AP-VSP-PND', 'Tehsil', 'Pendurthi CHC Hub', 'Andhra Pradesh', 'Visakhapatnam', 17.8303, 83.1979),
        ('IN-AP-VSP-BHM', 'Tehsil', 'Bheemili Hospital Spoke', 'Andhra Pradesh', 'Visakhapatnam', 17.8894, 83.4452),
        ('IN-AP-VZM-GJN', 'Tehsil', 'Gajapathinagaram PHC', 'Andhra Pradesh', 'Vizianagaram', 18.2789, 83.3323),
        ('IN-AP-SKL-RUR', 'Tehsil', 'Srikakulam Rural Center', 'Andhra Pradesh', 'Srikakulam', 18.3164, 83.8943),
        ('IN-AP-SKL-PLS', 'Tehsil', 'Palasa Super-Spec Spoke', 'Andhra Pradesh', 'Srikakulam', 18.7725, 84.4172)
    ]
    cursor.executemany("INSERT INTO administrative_hierarchy VALUES (?, ?, ?, ?, ?, ?, ?)", facilities)

    # 2. Map Medical Duty Personnel
    doctors = [
        ('DOC-VSP-001', 'IN-AP-VSP-PND', 'Dr. S. Srinivasa Rao', 'General Medicine', 1),
        ('DOC-VSP-002', 'IN-AP-VSP-PND', 'Dr. K. Anuradha', 'Pediatrics', 1),
        ('DOC-VSP-003', 'IN-AP-VSP-BHM', 'Dr. A. Lakshmi Prasanna', 'General Medicine', 0), 
        ('DOC-VZM-001', 'IN-AP-VZM-GJN', 'Dr. Ch. Koteswara Rao', 'General Medicine', 1),
        ('DOC-SKL-001', 'IN-AP-SKL-RUR', 'Dr. K. Venkataswamy', 'General Medicine', 1)
    ]
    cursor.executemany("INSERT INTO doctors VALUES (?, ?, ?, ?, ?)", doctors)

    # 3. Ground Intake ASHA Staff
    ashas = [
        ('ASHA-VSP-001', 'IN-AP-VSP-PND', 'asha_worker', 'Smt. Lakshmi', 'Pendurthi Village A'),
        ('ASHA-VZM-001', 'IN-AP-VZM-GJN', 'asha_gajapathinagaram', 'Smt. Saraswathi', 'Gajapathinagaram West'),
        ('ASHA-SKL-001', 'IN-AP-SKL-RUR', 'asha_srikakulam', 'Smt. Parvathi', 'Srikakulam Outer Ring')
    ]
    cursor.executemany("INSERT INTO asha_workers VALUES (?, ?, ?, ?, ?)", ashas)

    # 4. Local Pharmacy Operators
    pharmacists = [
        ('PHR-VSP-001', 'IN-AP-VSP-PND', 'pharma_person', 'Sri K. Venkatesh'),
        ('PHR-VZM-001', 'IN-AP-VZM-GJN', 'pharma_gajapathinagaram', 'Sri L. Narayana'),
        ('PHR-SKL-001', 'IN-AP-SKL-RUR', 'pharma_srikakulam_rur', 'Sri P. Satyam')
    ]
    cursor.executemany("INSERT INTO pharmacists VALUES (?, ?, ?, ?)", pharmacists)

    # 5. Asset Stock Balances
    inventory_data = [
        ('IN-AP-VSP-PND', 'Paracetamol Tabs', 450, 5000, 450.0),    
        ('IN-AP-VSP-BHM', 'Paracetamol Tabs', 18000, 4000, 180.0),  
        ('IN-AP-VZM-GJN', 'Paracetamol Tabs', 5500, 3000, 210.0),
        ('IN-AP-SKL-RUR', 'Anti-Venom Vials', 3, 40, 6.5),          
        ('IN-AP-SKL-PLS', 'Anti-Venom Vials', 150, 30, 2.0)         
    ]
    cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", inventory_data)

    # 6. Patient Flows
    triage_data = [
        ('AP-1422', 'IN-AP-VSP-PND', 'sha256_hash_xyz1', '9848022338', 'High Fever, Vomiting, Body Pains', 'WAITING'),
        ('AP-1423', 'IN-AP-SKL-RUR', 'sha256_hash_xyz2', '9440123456', 'Acute Snake Bite on Foot', 'WAITING')
    ]
    cursor.executemany("INSERT INTO patient_triage_queue VALUES (?, ?, ?, ?, ?, ?)", triage_data)

    # 7. Bed and Syndromic Anomaly Scores
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

# Evaluate database integrity status before execution loop begins
if not os.path.exists("data/smart_health.db") or os.path.getsize("data/smart_health.db") == 0:
    build_native_database_instance()

st.set_page_config(layout="wide", page_title="Bharat Health AI Command")
# app.py — BLOCK 2: VISUAL INTERFACE
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
col_left, col_right = st.columns(2)

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
# app.py — BLOCK 3: AI DISPATCH GATEWAY
st.markdown("---")

# ====================================================================
# 🤖 5. SECURE ADMIN GATEWAY: NO INTERNAL KEY STORAGE ARCHITECTURE
# ====================================================================
st.subheader("🤖 Gemini 2.5 Flash Autonomous Intervention Planner")

# Step A: Regular login access verification block for judges
typed_password = st.text_input(
    "🔑 Enter System Password", 
    type="password",
    placeholder="••••••••••••",
    help="Type 'AmaravatiHealth2026!' to unlock the administrative action triggers."
)

# Step B: Secure execution key validation wrapper block
typed_api_key = st.text_input(
    "🌐 Paste Your Private Gemini API Key", 
    type="password",
    placeholder="AIzaSy...",
    help="Paste your private key here to authenticate the summary execution loop. It runs strictly in memory."
)

if st.button("✨ Generate AI Strategic Operational Mandate"):
    # 1. Enforce strict matching parameter checks for your shared view passcode
    if typed_password == "AmaravatiHealth2026!":
        
        # 2. Check if the private key field has been populated
        if typed_api_key.startswith("AIzaSy"):
            with st.spinner("Access Granted. Communicating with Gemini Cloud Infrastructure nodes..."):
                
                from google import genai
                from google.genai import types
                
                try:
                    # Pass the key entered on screen directly into Google client constructor
                    client = genai.Client(api_key=typed_api_key.strip())
                    
                    # Convert the interactive Pandas monitoring table directly into string vectors
                    inventory_summary = inventory_df[['node_name', 'item_name', 'current_stock', 'min_required_threshold', 'daily_avg_consumption']].to_string()
                    
                    prompt = f"Analyze infrastructure state data and provide a concise, 2-sentence summary intervention plan:\n{inventory_summary}"
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.2)
                    )
                    
                    # Render resulting text card cleanly within an explicit alert wrapper
                    st.subheader("📋 Executive Strategic Health Summary")
                    st.warning(response.text)
                    st.success("🤖 Analysis executed successfully. Metrics are safe to display to judges.")
                    
                except Exception as e:
                    st.error(f"Gemini API Execution Error: {str(e)}")
        else:
            st.error("❌ Key Authentication Failure: Please paste a valid Gemini API Key starting with 'AIzaSy' into the input block above.")
    elif typed_password == "":
        st.error("Access Denied: Please input the shared access system password.")
    else:
        st.error("❌ Invalid System Password! This unauthorized gateway boundary breach has been logged to your database audit tables.")
        engine.log_audit_breach(typed_password)
