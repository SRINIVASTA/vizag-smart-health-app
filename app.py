# app.py — BLOCK 1: CORE INITIALIZATION & AUTOMATED SEEDER
import streamlit as st
import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt

# 🛠️ EMBEDDED AUTOMATIC DATABASE CREATION ENGINE
def build_native_database_instance():
    """Constructs the local smart_health database node from the sql schema blueprint."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/smart_health.db")
    cursor = conn.cursor()

    # Read and build raw tables from your exact schema definitions
    with open("data/schema.sql", "r", encoding="utf-8") as schema_file:
        cursor.executescript(schema_file.read())

    # Purge existing rows to avoid primary key constraints on hot-reloads
    cursor.execute("DELETE FROM system_audit_logs;")
    cursor.execute("DELETE FROM patient_prescriptions;")
    cursor.execute("DELETE FROM patient_triage_queue;")
    cursor.execute("DELETE FROM node_operations;")
    cursor.execute("DELETE FROM inventory;")
    cursor.execute("DELETE FROM pharmacists;")
    cursor.execute("DELETE FROM asha_workers;")
    cursor.execute("DELETE FROM doctors;")
    cursor.execute("DELETE FROM administrative_hierarchy;")

    # 1. Map Regional Facilities matching your official operational directory
    facilities = [
        ('IN-AP-VSP-PND', 'Tehsil', 'Pendurthi CHC Hub', 'Andhra Pradesh', 'Visakhapatnam', 17.8303, 83.1979),
        ('IN-AP-VSP-BHM', 'Tehsil', 'Bheemili Hospital Spoke', 'Andhra Pradesh', 'Visakhapatnam', 17.8894, 83.4452),
        ('IN-AP-VZM-GJN', 'Tehsil', 'Gajapathinagaram PHC', 'Andhra Pradesh', 'Vizianagaram', 18.2789, 83.3323),
        ('IN-AP-SKL-RUR', 'Tehsil', 'Srikakulam Rural Center', 'Andhra Pradesh', 'Srikakulam', 18.3164, 83.8943),
        ('IN-AP-SKL-PLS', 'Tehsil', 'Palasa Super-Spec Spoke', 'Andhra Pradesh', 'Srikakulam', 18.7725, 84.4172)
    ]
    cursor.executemany("INSERT INTO administrative_hierarchy VALUES (?, ?, ?, ?, ?, ?, ?)", facilities)

    # 2. Map Medical Duty Personnel with your credentials matrix
    doctors = [
        ('DOC-VSP-001', 'IN-AP-VSP-PND', 'Dr. S. Srinivasa Rao', 'General Medicine', 1),
        ('DOC-VSP-002', 'IN-AP-VSP-PND', 'Dr. K. Anuradha', 'Pediatrics', 1),
        ('DOC-VSP-003', 'IN-AP-VSP-BHM', 'Dr. A. Lakshmi Prasanna', 'General Medicine', 1), 
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

    # 5. Asset Stock Balances (Intentional Deficits vs Surpluses for simulation loops)
    inventory_data = [
        ('IN-AP-VSP-PND', 'Paracetamol Tabs', 450, 5000, 450.0),    
        ('IN-AP-VSP-BHM', 'Paracetamol Tabs', 18000, 4000, 180.0),  
        ('IN-AP-VZM-GJN', 'Paracetamol Tabs', 5500, 3000, 210.0),
        ('IN-AP-SKL-RUR', 'Anti-Venom Vials', 3, 40, 6.5),          
        ('IN-AP-SKL-PLS', 'Anti-Venom Vials', 150, 30, 2.0)         
    ]
    cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", inventory_data)

    # 6. Patient Flows Initial Data Seed
    triage_data = [
        ('AP-1422', 'IN-AP-VSP-PND', 'sha256_hash_xyz1', '9848022338', 'High Fever, Vomiting | BP: 135/85 mmHg | Mode: e-Sanjeevani Video Call Telehealth', 'WAITING'),
        ('AP-1423', 'IN-AP-SKL-RUR', 'sha256_hash_xyz2', '9440123456', 'Acute Snake Bite | BP: 140/90 mmHg | Mode: Physical Local OPD Desk', 'WAITING')
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

if not os.path.exists("data/smart_health.db") or os.path.getsize("data/smart_health.db") == 0:
    build_native_database_instance()

st.set_page_config(layout="wide", page_title="Bharat Health AI Command")
# app.py — BLOCK 2: ROLE-BASED ACCESS CONTROL CONTROLLER
st.markdown("""
    <div style='background-color:#003A70;padding:15px;border-radius:10px;margin-bottom:20px'>
        <h1 style='color:white;margin:0;font-family:sans-serif;'>🌐 Bharat Health AI: Multi-Role Operations Matrix</h1>
        <p style='color:#FFC107;margin:5px 0 0 0;'>Track 3: Smart Health Dashboard — End-to-End Workflow Verification</p>
    </div>
""", unsafe_allow_html=True)

# 🛠️ NATIVE STOCK CHART CONTROLLERS
def local_stock_chart(df):
    fig, ax = plt.subplots(figsize=(7, 3.2))
    df_sorted = df.sort_values(by='current_stock')
    colors = ['#DC3545' if x <= r['min_required_threshold'] else '#28A745' for x, r in zip(df_sorted['current_stock'], df_sorted.to_dict('records'))]
    bars = ax.barh(df_sorted['node_name'], df_sorted['current_stock'], color=colors, height=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('Current Inventory Balances', fontsize=9, fontweight='bold')
    ax.set_title('AI Supply Depletion & Stock Grid Monitor', fontsize=10, fontweight='bold')
    plt.tight_layout()
    return fig

def local_risk_chart(scope_district):
    conn = sqlite3.connect("data/smart_health.db")
    query = "SELECT h.node_name, o.active_epidemic_risk_score, h.district_name FROM node_operations o JOIN administrative_hierarchy h ON o.node_id = h.node_id"
    df = pd.read_sql_query(query, conn)
    conn.close()
    if scope_district != "All Districts":
        df = df[df['district_name'] == scope_district]
    fig, ax = plt.subplots(figsize=(7, 3.2))
    bars = ax.bar(df['node_name'], df['active_epidemic_risk_score'], color='#007BFF', alpha=0.85, width=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylabel('Outbreak Risk Multiplier', fontsize=9, fontweight='bold')
    ax.set_ylim(0, 1.0)
    plt.xticks(rotation=10, ha='right', fontsize=8)
    plt.tight_layout()
    return fig

# 🔐 SIDEBAR AUTHENTICATION ENGINE
st.sidebar.header("🔐 Role Clearance Desk")
selected_role = st.sidebar.selectbox("Select Your System Role", ["Choose Role", "State Administrator", "District Officer", "ASHA Worker", "Medical Doctor", "Pharmacist"])
password_input = st.sidebar.text_input("Enter Clearance Password", type="password", placeholder="••••••••••••")

# Access verification routing logic parameters
authenticated = False
assigned_district = "All Districts"
assigned_facility = "ALL"

# Explicit role mapping cross-checks matching your exact credentials
if selected_role == "State Administrator" and password_input == "AmaravatiHealth2026!":
    authenticated = True
    assigned_district = st.sidebar.selectbox("Filter Global Jurisdiction", ["All Districts", "Visakhapatnam", "Vizianagaram", "Srikakulam"])
elif selected_role == "District Officer" and password_input == "VizagDSU99!":
    authenticated = True
    assigned_district = st.sidebar.selectbox("Select Monitored Area", ["Visakhapatnam", "Vizianagaram", "Srikakulam"])
elif selected_role == "ASHA Worker" and password_input == "VillageASHA456":
    authenticated = True
    user_node = st.sidebar.selectbox("Select Your Operational Village Base", ["Pendurthi Hub", "Gajapathinagaram PHC", "Srikakulam Rural"])
    assigned_facility = "IN-AP-VSP-PND" if "Pendurthi" in user_node else "IN-AP-VZM-GJN" if "Gajapathinagaram" in user_node else "IN-AP-SKL-RUR"
elif selected_role == "Medical Doctor" and password_input == "MedicalDoc123":
    authenticated = True
    user_doc = st.sidebar.selectbox("Select Your Registry Name", ["Dr. S. Srinivasa Rao", "Dr. Ch. Koteswara Rao", "Dr. K. Venkataswamy"])
    assigned_facility = "IN-AP-VSP-PND" if "Srinivasa" in user_doc else "IN-AP-VZM-GJN" if "Koteswara" in user_doc else "IN-AP-SKL-RUR"
elif selected_role == "Pharmacist" and password_input == "PharmaStore456":
    authenticated = True
    user_phr = st.sidebar.selectbox("Select Pharmacy Unit", ["Sri K. Venkatesh (Pendurthi)", "Sri L. Narayana (Gajapathinagaram)", "Sri P. Satyam (Srikakulam)"])
    assigned_facility = "IN-AP-VSP-PND" if "Pendurthi" in user_phr else "IN-AP-VZM-GJN" if "Gajapathinagaram" in user_phr else "IN-AP-SKL-RUR"
elif password_input != "":
    st.sidebar.error("❌ Invalid clearance password credentials for the selected role.")

# RENDER MAIN INTERACTIVE DATA GRID WORKSPACES
if authenticated:
    conn = sqlite3.connect("data/smart_health.db")
    inventory_df = pd.read_sql_query("SELECT i.*, h.node_name, h.district_name, h.latitude, h.longitude FROM inventory i JOIN administrative_hierarchy h ON i.node_id = h.node_id", conn)
    conn.close()

    if assigned_district != "All Districts":
        inventory_df = inventory_df[inventory_df['district_name'] == assigned_district]

    # Display Macro Metrics for Administrative ranks (State Admin and District Officers)
    if selected_role in ["State Administrator", "District Officer"]:
        st.subheader(f"📊 Surveillance Operations Panel: Scope [{assigned_district}]")
        col_g1, col_g2 = st.columns(2)
        with col_g1: st.pyplot(local_stock_chart(inventory_df))
        with col_g2: st.pyplot(local_risk_chart(assigned_district))
# app.py — BLOCK 3: HEALTH WORKFLOW SIMULATION & GEMINI INTERFACE
    st.markdown("---")
    st.subheader("🔄 Multi-Tier Operational Workflow Execution Engine")
    
    # -------------------------------------------------------------
    # ROLE WORKFLOW VIEW 1: ASHA PATIENT TRIAGE COUNTER
    # -------------------------------------------------------------
    if selected_role == "ASHA Worker":
        st.info(f"🌾 Connected Mode: Frontline Intake Logger (Facility Terminal: {assigned_facility})")
        with st.form("asha_entry_form"):
            pt_phone = st.text_input("Patient Contact Mobile Number", "9848022338")
            symptoms = st.text_input("Logged Symptoms Description", "High Fever, Chills, Dehydration, Vomiting")
            sys_bp = st.number_input("Vitals: Systolic Blood Pressure (mmHg)", 80, 200, 130)
            dia_bp = st.number_input("Vitals: Diastolic Blood Pressure (mmHg)", 50, 120, 85)
            consult_mode = st.radio("Requested Consultation Mode", ["e-Sanjeevani Video Call Telehealth", "Physical Local OPD Desk"])
            
            if st.form_submit_button("📥 Push Triage Metrics to Clinical Queue"):
                conn = sqlite3.connect("data/smart_health.db")
                cursor = conn.cursor()
                token = f"AP-{cursor.execute('SELECT COUNT(*) FROM patient_triage_queue').fetchone() + 1001}"
                vitals_summary = f"{symptoms} | BP: {sys_bp}/{dia_bp} mmHg | Mode: {consult_mode}"
                cursor.execute("INSERT INTO patient_triage_queue VALUES (?, ?, ?, ?, ?, 'WAITING')", (token, assigned_facility, "sha256_hash", pt_phone, vitals_summary))
                conn.commit()
                conn.close()
                st.success(f"🎉 Patient registration logged! Assigned Token ID: **{token}**. Forwarded to Clinical Pool.")

    # -------------------------------------------------------------
    # ROLE WORKFLOW VIEW 2: DOCTOR EVALUATION pool
    # -------------------------------------------------------------
    elif selected_role == "Medical Doctor":
        st.info(f"🩺 Connected Mode: Clinical Practitioner (Facility Terminal: {assigned_facility})")
        conn = sqlite3.connect("data/smart_health.db")
        waiting_df = pd.read_sql_query("SELECT * FROM patient_triage_queue WHERE node_id = ? AND status = 'WAITING'", conn, params=(assigned_facility,))
        conn.close()
        
        if not waiting_df.empty:
            st.dataframe(waiting_df[['token_id', 'symptoms_logged']], use_container_width=True, hide_index=True)
            with st.form("doc_prescription_form"):
                target_token = st.selectbox("Select Active Patient Token to Treat", waiting_df['token_id'].tolist())
                rx_med = st.selectbox("Prescribe Necessary Medical Formulation", ["Paracetamol Tabs", "Anti-Venom Vials", "Amoxicillin Caps"])
                rx_dose = st.text_input("Dosage Regulation Instructions", "1 tablet after meals twice daily for 5 days")
                
                if st.form_submit_button("✍️ Authorize and Sign Digital Prescription"):
                    conn = sqlite3.connect("data/smart_health.db")
                    cursor = conn.cursor()
                    vitals_txt = cursor.execute("SELECT symptoms_logged FROM patient_triage_queue WHERE token_id = ?", (target_token,)).fetchone()[0]
                    mode = "e-Sanjeevani Video Call Telehealth" if "Video" in vitals_txt else "Physical Local OPD Desk"
                    cursor.execute("INSERT INTO patient_prescriptions (token_id, node_id, doctor_name, medication_name, dosage_instructions, consult_mode, status) VALUES (?, ?, ?, ?, ?, ?, 'PENDING')",
                                   (target_token, assigned_facility, "Attending Doctor", rx_med, rx_dose, mode))
                    cursor.execute("UPDATE patient_triage_queue SET status = 'COMPLETED' WHERE token_id = ?", (target_token,))
                    conn.commit()
                    conn.close()
                    st.success(f"🏥 Prescription for case **{target_token}** signed and transmitted to Pharmacy Counter for fulfillment routing.")
                    st.rerun()
        else:
            st.success("🟢 All patient consultation triage slots for this facility node are currently clear.")

    # -------------------------------------------------------------
    # ROLE WORKFLOW VIEW 3: PHARMACIST DELIVERY DESK
    # -------------------------------------------------------------
    elif selected_role == "Pharmacist":
        st.info(f"💊 Connected Mode: Dispensation & Logistics Desk (Facility Terminal: {assigned_facility})")
        conn = sqlite3.connect("data/smart_health.db")
        orders_df = pd.read_sql_query("SELECT * FROM patient_prescriptions WHERE node_id = ? AND status = 'PENDING'", conn, params=(assigned_facility,))
        conn.close()
        
        if not orders_df.empty:
            st.dataframe(orders_df[['prescription_id', 'token_id', 'medication_name', 'consult_mode']], use_container_width=True, hide_index=True)
            with st.form("pharma_fulfillment_form"):
                target_rx = st.selectbox("Select Prescription ID to Dispense", orders_df['prescription_id'].tolist())
                delivery_method = st.radio("Fulfillment Logistics Path", ["📦 Standard Over-the-Counter Physical Handout", "✈️ Autonomous BVLOS Drone Resupply Flight Path"])
                
                if st.form_submit_button("🚀 Finalize Dispensation Order"):
                    conn = sqlite3.connect("data/smart_health.db")
                    cursor = conn.cursor()
                    rx_item = cursor.execute("SELECT medication_name FROM patient_prescriptions WHERE prescription_id = ?", (target_rx,)).fetchone()[0]
                    cursor.execute("UPDATE inventory SET current_stock = current_stock - 1 WHERE node_id = ? AND item_name = ?", (assigned_facility, rx_item))
                    cursor.execute("UPDATE patient_prescriptions SET status = 'FULFILLED' WHERE prescription_id = ?", (target_rx,))
                    conn.commit()
                    conn.close()
                    
                    st.success(f"✅ Dispensation Order #{target_rx} completed successfully! Inventory balance decremented.")
                    if "Drone" in delivery_method:
                        st.warning(f"✈️ BVLOS Drone Launcher Primed! Transporting payload formulation ({rx_item}) directly to field coordinates mapped via src/drone_logistics.py.")
                    st.rerun()
        else:
            st.success("🟢 No pending digital prescriptions require dispensation at this counter block.")

    # Display General Logs for Administrative roles
    elif selected_role in ["State Administrator", "District Officer"]:
        conn = sqlite3.connect("data/smart_health.db")
        global_triage = pd.read_sql_query("SELECT t.token_id, h.node_name, t.symptoms_logged, t.status FROM patient_triage_queue t JOIN administrative_hierarchy h ON t.node_id = h.node_id", conn)
        conn.close()
        st.subheader("📋 Unified System Triage Records Ledger")
        st.dataframe(global_triage, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------
    # 🤖 UNIFIED GEMINI 2.5 FLASH SURVEILLANCE GENERATOR
    # -------------------------------------------------------------
    if selected_role in ["State Administrator", "District Officer"]:
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
                        summary_txt = inventory_df[['node_name', 'item_name', 'current_stock', 'min_required_threshold', 'daily_avg_consumption']].to_string()
                        prompt = f"Analyze infrastructure state data and provide a concise, 2-sentence summary intervention plan:\n{summary_txt}"
                        
                        response = client.models.generate_content(model='generamin-2.5-flash', contents=prompt, config=types.GenerateContentConfig(temperature=0.2))
                        st.subheader("📋 Executive Strategic Health Summary")
                        st.warning(response.text)
                    except Exception as e:
                        st.error(f"Gemini API Execution Error: {str(e)}")
            else:
                st.error("Please insert a valid developer API Key to unlock this module.")
else:
    st.info("🔒 Please select a valid role and enter its clearance password in the left sidebar to unlock records.")
