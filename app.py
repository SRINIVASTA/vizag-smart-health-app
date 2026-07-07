# app.py — BLOCK 1: INITIALIZATION
import streamlit as st
import pandas as pd
import sqlite3
import os
import src.predictive_engine as engine

# 🛠️ EMBEDDED AUTOMATIC DATABASE CREATION ENGINE
def build_native_database_instance():
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

    # 6. Bed and Syndromic Anomaly Scores
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
# app.py — BLOCK 2: DYNAMIC SECURITY LAYER & USER DIRECTORY
st.markdown("""
    <div style='background-color:#003A70;padding:15px;border-radius:10px;margin-bottom:20px'>
        <h1 style='color:white;margin:0;font-family:sans-serif;'>🌐 Bharat Health AI: Decentralized Administrative Portal</h1>
        <p style='color:#FFC107;margin:5px 0 0 0;'>Track 3: Multi-Tier Governance & Live Workflow Verification Node</p>
    </div>
""", unsafe_allow_html=True)

# 1. Setup Password Login Gate inside Sidebar for Authorization Verification
st.sidebar.header("🔐 Command Clearance Desk")
access_password = st.sidebar.text_input("Enter Clearance Password", type="password", placeholder="••••••••••••")

# Map password strings to target regional scopes
current_scope = "DENIED"
selected_district = "All Districts"

if access_password == "AmaravatiHealth2026!":
    current_scope = "STATE"
    st.sidebar.success("🟢 Authenticated: AP State Admin View unlocked.")
    # Allow state admin to switch between districts manually via a dropdown box
    selected_district = st.sidebar.selectbox("Select Target District Scope", ["All Districts", "Visakhapatnam", "Vizianagaram", "Srikakulam"])
elif access_password == "VizagDSU99!":
    current_scope = "DISTRICT"
    selected_district = "Visakhapatnam"
    st.sidebar.success("🟢 Authenticated: Visakhapatnam District Scope locked.")
elif access_password == "Vizianagaram99!":
    current_scope = "DISTRICT"
    selected_district = "Vizianagaram"
    st.sidebar.success("🟢 Authenticated: Vizianagaram District Scope locked.")
elif access_password == "Srikakulam99!":
    current_scope = "DISTRICT"
    selected_district = "Srikakulam"
    st.sidebar.success("🟢 Authenticated: Srikakulam District Scope locked.")
elif access_password != "":
    st.sidebar.error("❌ Access Denied: Invalid Authentication Token.")

# Run initial stock balancing calculations
inventory_df, calculated_transfers = engine.run_cross_tier_supply_balancing()

if current_scope != "DENIED":
    # Apply location filters to analytical dataframes
    if selected_district != "All Districts":
        inventory_df = inventory_df[inventory_df['district_name'] == selected_district]

    # Render Charts Matrix
    c1, c2 = st.columns(2)
    with c1: st.pyplot(engine.generate_stock_prediction_chart(inventory_df))
    with c2: st.pyplot(engine.generate_epidemic_risk_chart(selected_district))

    st.markdown("---")
    st.subheader(f"👥 Human Resource Directory: {selected_district} Jurisdiction")
    
    # Extract staff listings dynamically using relational joins
    conn = sqlite3.connect("data/smart_health.db")
    
    doc_df = pd.read_sql_query("SELECT d.doctor_name as Name, h.node_name as Facility, d.specialization as Detail, h.district_name FROM doctors d JOIN administrative_hierarchy h ON d.node_id = h.node_id", conn)
    asha_df = pd.read_sql_query("SELECT a.worker_name as Name, h.node_name as Facility, a.assigned_village as Detail, h.district_name FROM asha_workers a JOIN administrative_hierarchy h ON a.node_id = h.node_id", conn)
    phr_df = pd.read_sql_query("SELECT p.employee_name as Name, h.node_name as Facility, 'Pharmacy Manager' as Detail, h.district_name FROM pharmacists p JOIN administrative_hierarchy h ON p.node_id = h.node_id", conn)
    conn.close()

    if selected_district != "All Districts":
        doc_df = doc_df[doc_df['district_name'] == selected_district]
        asha_df = asha_df[asha_df['district_name'] == selected_district]
        phr_df = phr_df[phr_df['district_name'] == selected_district]

    # Display Personnel categories side by side
    col_d, col_a, col_p = st.columns(3)
    with col_d:
        st.markdown("🩺 **Medical Practitioners**")
        st.dataframe(doc_df[['Name', 'Facility']], use_container_width=True, hide_index=True)
    with col_a:
        st.markdown("🌾 **ASHA Ground Field Workers**")
        st.dataframe(asha_df[['Name', 'Detail']], use_container_width=True, hide_index=True)
    with col_p:
        st.markdown("💊 **Accredited Pharmacists**")
        st.dataframe(phr_df[['Name', 'Facility']], use_container_width=True, hide_index=True)
else:
    st.info("🔒 Please enter a valid administrative password in the left sidebar to unlock regional healthcare records.")
# app.py — BLOCK 3: LIVE OPERATIONAL HEALTH WORKFLOW ENGINE
if current_scope != "DENIED":
    st.markdown("---")
    st.header("🔄 Live Closed-Loop Care Workflow Simulation")
    
    tab1, tab2, tab3 = st.tabs(["1️⃣ ASHA Ground Intake Desk", "2️⃣ Doctor Evaluation Portal", "3️⃣ Pharmacist Fulfillment & Drone Desk"])

    # -------------------------------------------------------------
    # STEP 1: ASHA INTAKE LOGGING DESK
    # -------------------------------------------------------------
    with tab1:
        st.subheader("🌾 Frontline Patient Intake Registration Matrix")
        with st.form("asha_intake_form"):
            patient_phone = st.text_input("Patient Contact Number (Phone)", "9848022338")
            symptoms = st.text_area("Logged Symptoms Description", "Acute High Fever, Severe Headaches, Body Dehydration")
            bp_sys = st.number_input("Blood Pressure - Systolic (mmHg)", 120, 200, 130)
            bp_dia = st.number_input("Blood Pressure - Diastolic (mmHg)", 70, 120, 85)
            consult_type = st.selectbox("Requested Mode of Consultation", ["e-Sanjeevani Video Call Telehealth", "Physical Local OPD Desk"])
            target_node = st.selectbox("Intake Facility Target Destination Node", ["IN-AP-VSP-PND", "IN-AP-VZM-GJN", "IN-AP-SKL-RUR"])
            
            if st.form_submit_button("📥 Push Triage Metrics to Clinical Queue"):
                conn = sqlite3.connect("data/smart_health.db")
                cursor = conn.cursor()
                token_id = f"AP-{cursor.execute('SELECT COUNT(*) FROM patient_triage_queue').fetchone()[0] + 1001}"
                vitals_payload = f"{symptoms} | BP: {bp_sys}/{bp_dia} mmHg | Mode: {consult_type}"
                
                cursor.execute("INSERT INTO patient_triage_queue (token_id, node_id, aadhaar_hash, patient_phone, symptoms_logged, status) VALUES (?, ?, ?, ?, ?, ?)",
                               (token_id, target_node, "sha256_hashed_identity_token", patient_phone, vitals_payload, 'WAITING'))
                conn.commit()
                conn.close()
                st.success(f"🎉 Patient case generated successfully! Token ID assigned: **{token_id}**. Routed to Medical Doctor's evaluation pool.")

    # -------------------------------------------------------------
    # STEP 2: DOCTOR CLINICAL PRESCRIPTION PORTAL
    # -------------------------------------------------------------
    with tab2:
        st.subheader("🩺 Medical Practitioner Evaluation Pool")
        conn = sqlite3.connect("data/smart_health.db")
        waiting_patients = pd.read_sql_query("SELECT * FROM patient_triage_queue WHERE status = 'WAITING'", conn)
        conn.close()
        
        if not waiting_patients.empty:
            st.dataframe(waiting_patients[['token_id', 'node_id', 'symptoms_logged']], use_container_width=True, hide_index=True)
            with st.form("doctor_prescription_form"):
                selected_token = st.selectbox("Select Patient Token to Treat", waiting_patients['token_id'].tolist())
                medication = st.selectbox("Prescribe Required Medical Formulation", ["Paracetamol Tabs", "Anti-Venom Vials", "Amoxicillin Caps"])
                dosage = st.text_input("Dosage Instructions Matrix", "500mg - 1 tablet after meals twice daily for 5 days")
                doc_name = st.text_input("Attending Practitioner Signature", "Dr. S. Srinivasa Rao")
                
                if st.form_submit_button("✍️ Authorize and Sign Digital Prescription"):
                    conn = sqlite3.connect("data/smart_health.db")
                    cursor = conn.cursor()
                    # Extract facility node index link safely
                    node_id = cursor.execute("SELECT node_id FROM patient_triage_queue WHERE token_id = ?", (selected_token,)).fetchone()[0]
                    consult_mode = cursor.execute("SELECT symptoms_logged FROM patient_triage_queue WHERE token_id = ?", (selected_token,)).fetchone()[0].split(" | ")[-1].replace("Mode: ", "")
                    
                    cursor.execute("INSERT INTO patient_prescriptions (token_id, node_id, doctor_name, medication_name, dosage_instructions, consult_mode, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                   (selected_token, node_id, doc_name, medication, dosage, consult_mode, 'PENDING'))
                    cursor.execute("UPDATE patient_triage_queue SET status = 'COMPLETED' WHERE token_id = ?", (selected_token,))
                    conn.commit()
                    conn.close()
                    st.success(f"🏥 Prescription for case **{selected_token}** signed and transmitted to Pharmacy Counter for fulfillment routing.")
        else:
            st.info("🟢 Clinical Queue Clear: No patients are currently waiting in the consultation tier.")

    # -------------------------------------------------------------
    # STEP 3: PHARMACIST FULFILLMENT & DRONE LOGISTICS DESK
    # -------------------------------------------------------------
    with tab3:
        st.subheader("💊 Pharmacy Dispensation Desk & Aero-Logistics Network")
        conn = sqlite3.connect("data/smart_health.db")
        pending_orders = pd.read_sql_query("SELECT p.*, h.node_name FROM patient_prescriptions p JOIN administrative_hierarchy h ON p.node_id = h.node_id WHERE p.status = 'PENDING'", conn)
        conn.close()
        
        if not pending_orders.empty:
            st.dataframe(pending_orders[['prescription_id', 'token_id', 'node_name', 'medication_name', 'consult_mode']], use_container_width=True, hide_index=True)
            with st.form("pharmacy_fulfillment_form"):
                selected_order = st.selectbox("Select Prescription ID to Dispense", pending_orders['prescription_id'].tolist())
                
                # Dynamic Routing Option
                delivery_method = st.radio("Fulfillment Logistics Path", ["📦 Standard Over-the-Counter Physical Handout", "✈️ Autonomous BVLOS Drone Resupply Flight Path"])
                
                if st.form_submit_button("🚀 Finalize Dispensation Order"):
                    conn = sqlite3.connect("data/smart_health.db")
                    cursor = conn.cursor()
                    
                    # Fetch details for delivery mapping
                    order_info = cursor.execute("SELECT node_id, medication_name FROM patient_prescriptions WHERE prescription_id = ?", (selected_order,)).fetchone()
                    target_node, rx_item = order_info[0], order_info[1]
                    
                    # Update inventory balances
                    cursor.execute("UPDATE inventory SET current_stock = current_stock - 1 WHERE node_id = ? AND item_name = ?", (target_node, rx_item))
                    cursor.execute("UPDATE patient_prescriptions SET status = 'FULFILLED' WHERE prescription_id = ?", (selected_order,))
                    conn.commit()
                    conn.close()
                    
                    st.success(f"✅ Order #{selected_order} dispatched successfully!")
                    if "Drone" in delivery_method:
                        st.warning(f"✈️ BVLOS Autonomous Payload Locked: Drone launching to deliver {rx_item} to regional facility node ({target_node}). Coordinates mapped via src/drone_logistics.py.")
        else:
            st.info("🟢 All digital prescriptions have been successfully dispensed across nodes.")

    # -------------------------------------------------------------
    # AI FORECAST REPORTING LAYER (From your successful Colab test)
    # -------------------------------------------------------------
    st.markdown("---")
    st.subheader("🤖 Gemini 2.5 Flash Autonomous Intervention Planner")
    typed_api_key = st.text_input("🌐 Paste Your Private Gemini API Key to run Anomaly Analysis", type="password", placeholder="AIza...")
    
    if st.button("✨ Run AI Demand Analytics"):
        if typed_api_key.strip().startswith("AIza") and len(typed_api_key.strip()) > 10:
            with st.spinner("Connecting to Gemini Model..."):
                try:
                    from google import genai
                    from google.genai import types
                    client = genai.Client(api_key=typed_api_key.strip())
                    inventory_summary = inventory_df[['node_name', 'item_name', 'current_stock', 'min_required_threshold', 'daily_avg_consumption']].to_string()
                    prompt = f"Analyze infrastructure state data and provide a concise, 2-sentence summary intervention plan:\n{inventory_summary}"
                    
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt, config=types.GenerateContentConfig(temperature=0.2))
                    st.subheader("📋 Executive Strategic Health Summary")
                    st.warning(response.text)
                except Exception as e:
                    st.error(f"Gemini API Execution Error: {str(e)}")
        else:
            st.error("Please insert a valid developer API Key to unlock this module.")
