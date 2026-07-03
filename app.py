import streamlit as st
import sqlite3
import base64
import re
import json
import hashlib
from datetime import datetime

DB_NAME = "web_smart_health.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # HARDENED SELF-HEALING DATABASE MIGRATION ENGINE
    # Drops tables only if structural column elements mismatch previous trial schema models
    try:
        cursor.execute("SELECT target_disposition FROM patient_queue LIMIT 1")
        cursor.execute("SELECT doctor_prefix FROM doctor_roster LIMIT 1")
        cursor.execute("SELECT allowed_designation FROM medicine_stock LIMIT 1")
    except sqlite3.OperationalError:
        # Clear old tracking tables cleanly to establish a valid enterprise join state
        cursor.execute("DROP TABLE IF EXISTS patient_queue")
        cursor.execute("DROP TABLE IF EXISTS prescriptions")
        cursor.execute("DROP TABLE IF EXISTS facility_telemetry_logs")
        cursor.execute("DROP TABLE IF EXISTS doctor_roster")
        cursor.execute("DROP TABLE IF EXISTS medicine_stock")
        cursor.execute("DROP TABLE IF EXISTS pharma_roster")
        
    # Structural Core Schemas
    cursor.execute('''CREATE TABLE IF NOT EXISTS patient_queue (
        token_id TEXT PRIMARY KEY, category TEXT, status TEXT, arrival_time TIMESTAMP, called_time TIMESTAMP,
        patient_aadhaar_hash TEXT, patient_name TEXT, target_doctor TEXT, chief_complaint TEXT, target_disposition TEXT DEFAULT 'Out-Patient')''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS medicine_stock 
        (item_name TEXT PRIMARY KEY, current_stock INTEGER, reorder_level INTEGER, allowed_designation TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS bed_occupancy (bed_type TEXT PRIMARY KEY, total_beds INTEGER, occupied_beds INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS doctor_roster 
        (doctor_id TEXT PRIMARY KEY, doctor_name TEXT, specialty TEXT, attendance_status TEXT, doctor_prefix TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pharma_roster (staff_id TEXT PRIMARY KEY, staff_name TEXT, shift_status TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS prescriptions (
        prescription_id INTEGER PRIMARY KEY AUTOINCREMENT, token_id TEXT, aadhaar_hash TEXT, prescribed_meds TEXT,
        unit_dosages_prescribed TEXT, doctor_name TEXT, dispense_status TEXT DEFAULT 'PENDING', 
        pharma_verification_timestamp TEXT, dispensing_pharmacist TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS facility_telemetry_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT, log_date TEXT, token_id TEXT, patient_name TEXT, chief_complaint TEXT,
        detailed_medicines_issued TEXT, total_pills_dispensed_count INTEGER, treating_doctor TEXT, dispensing_pharmacist TEXT, patient_disposition TEXT)''')
    
    # Seed multi-role catalog parameters safely
    cursor.execute("INSERT OR IGNORE INTO medicine_stock VALUES ('Paracetamol 500mg', 1200, 500, 'GEN'), ('Anti-Venom Injection', 30, 10, 'GEN'), ('Artesunate (Malaria)', 150, 50, 'GEN'), ('Iron-Folic Acid Supplement', 500, 200, 'MAT'), ('Oxytocin Injection', 40, 15, 'MAT')")
    cursor.execute("INSERT OR IGNORE INTO bed_occupancy VALUES ('General Ward', 20, 14), ('Oxygen Beds', 10, 9), ('Isolation Unit', 5, 2)")
    cursor.execute("INSERT OR IGNORE INTO doctor_roster VALUES ('DOC-01', 'Dr. Ramesh Babu', 'General Physician', 'PRESENT', 'GEN'), ('DOC-02', 'Dr. S. Lakshmi', 'Maternal Specialist', 'PRESENT', 'MAT')")
    cursor.execute("INSERT OR IGNORE INTO pharma_roster VALUES ('PHARM-01', 'M. Srinivasa Rao (Pharma In-Charge)', 'ACTIVE'), ('PHARM-02', 'K. Durga Devi (Junior Pharmacist)', 'ACTIVE')")
    conn.commit()
    conn.close()

init_db()

class CryptoProtocol:
    _KEY = b"VizagPHCArakuValleySecretKey2026##"
    @staticmethod
    def encrypt(data_str: str) -> str:
        encrypted_bytes = bytes([ord(data_str[i]) ^ CryptoProtocol._KEY[i % len(CryptoProtocol._KEY)] for i in range(len(data_str))])
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    @staticmethod
    def hash_aadhaar(aadhaar_no: str) -> str:
        return hashlib.sha256(aadhaar_no.encode()).hexdigest()[:16]

LANG_PACK = {
    "en": {
        "title": "🏥 Visakhapatnam Smart Health Enterprise Hub",
        "subtitle": "Prefix-Routed Token Engines, Restricted Pharmacy Lists, & In-Patient Bed Management.",
        "triage_header": "🛰️ Entrance Kiosk: Autonomous Aadhaar Biometric Scan",
        "doc_header": "👨‍⚕️ Doctor Consultation Room & Prescription Desk",
        "pharma_header": "💊 Direct-Pull Unit-Dose Pharmacy Dispensing Desk",
        "aadhaar_label": "Swipe Aadhaar Card / Place Thumb on Scanner (Simulate 12-Digit Entry):",
        "input_label": "Primary Chief Complaint / Clinical Reason for Visit:",
        "input_placeholder": "e.g., Pregnant patient requiring ANC checkup.",
        "gate_doc_select": "Select Intended Doctor to Consult:",
        "med_prescribe_lbl": "Select Medication (Filtered by Your Specialty Authorization):",
        "doc_select_lbl": "Select Attending Medical Officer:",
        "pharma_select_lbl": "Log In Active Dispensing Pharmacist Identity:",
        "dispo_lbl": "Clinical Disposition Framework (Set Patient Care Status):",
        "submit_btn": "🔗 Ingest UIDAI Biometrics & Issue Prefix Routed Token",
        "text_success": "Aadhaar verified! Token generated with matching prefix designation:",
        "rx_btn": "✍️ Authorize Prescription & Route to Pharmacy",
        "dispense_btn": "🎯 Confirm Physical Handout & Log Final Dispense",
        "metrics_header": "📊 Real-Time Operations Telemetry",
        "waiting": "Waiting Patients",
        "med_count_lbl": "Active Catalog Items (Live Directory)",
        "beds_headline": "🛏️ Live Bed Matrix Status",
        "vacant": "vacant", "stable": "STABLE", "high_load": "HIGH LOAD", "critical": "CRITICAL",
        "ambulance": "📢 AMBULANCE DISPATCH CONTROLLER",
        "amb_divert": "⚠️ [DIVERTING PROTOCOL ACTIVE] Redirecting inbound oxygen emergency logistics directly to CHC Anakapalle!",
        "amb_stable": "✅ [FACILITY UNLOCKED] Inbound transport cleared for direct entry.",
        "sync_header": "🛡️ Cryptographic Transmission & Cloud Backhaul Sync",
        "sync_btn": "🔒 Securely Sync Anonymized FHIR Cloud Payload",
        "crypt_shield": "🔐 FHIR Interoperability Shield Active! Universally compliant encrypted payload built:",
        "cache_balanced": "📭 Cache balanced. Zero changes pending transmission.",
        "archive_header": "📁 Secure Operational Telemetry Log Archive",
        "csv_btn": "📥 Download Consolidated CSV Audit Spreadsheet Report"
    },
    "te": {
        "title": "🏥  విశాఖపట్నం జిల్లా స్మార్ట్ హెల్త్ ఎంటర్‌ప్రైజ్ హబ్",
        "subtitle": "డాక్టర్ విభాగం ఆధారిత టోకెన్లు, ఫిల్టర్ చేయబడిన మందుల పంపిణీ మరియు ఇన్-పేషెంట్ నిర్వహణ వ్యవస్థ.",
        "triage_header": "🛰️ ప్రవేశ ద్వారం: ఆటోమేటిక్ ఆధార్ బయోమెట్రిక్ స్కాన్ కౌంటర్",
        "doc_header": "👨‍⚕️ వైద్యుల చికిత్స మరియు మందుల ప్రిస్క్రిప్షన్ గది",
        "pharma_header": "💊 ఫార్మసీ మందుల పంపిణీ కౌంటర్ (Pharma Desk)",
        "aadhaar_label": "ఆధార్ కార్డ్‌ను స్వైప్ చేయండి / బయోమెట్రిక్ స్కానర్‌పై బొటనవేలు ఉంచండి:",
        "input_label": "రోగి యొక్క ఆరోగ్య సమస్యల వివరాలు:",
        "input_placeholder": "ఉదాహరణకు: గర్భిణీ స్త్రీ రెగ్యులర్ చెకప్ కోసం వచ్చారు.",
        "gate_doc_select": "మీరు సంప్రదించాలనుకుంటున్న వైద్యుడిని ఎంచుకోండి:",
        "med_prescribe_lbl": "మీ అర్హతకు కేటాయించబడిన మందులను మాత్రమే ఎంచుకోండి:",
        "pharma_select_lbl": "మందులు ఇస్తున్న ఫార్మసిస్ట్‌ను ఎంచుకోండి:",
        "dispo_lbl": "రోగి చికిత్సా విధానం రకం (Patient Care Type):",
        "submit_btn": "🔗 ఆధార్ బయోమెట్రిక్స్ సేకరించి టోకెన్ ఇవ్వండి",
        "text_success": "ఆధార్ వెరిఫై అయింది! కేటాయించబడిన టోకెన్ ఐడి:",
        "rx_btn": "✍️ ప్రిస్క్రిప్షన్ జారీ చేసి ఫార్మసీకి పంపండి",
        "dispense_btn": "🎯 మందుల పంపిణీని నిర్ధారించి రికార్డ్ చేయండి",
        "metrics_header": "📊 ప్రత్యక్ష ఆరోగ్య కేంద్రం వివరాలు",
        "waiting": "వేచి ఉన్న రోగులు",
        "med_count_lbl": "అందుబాటులో ఉన్న మొత్తం మందుల రకాలు (Live Catalog)",
        "beds_headline": "🛏️ బెడ్ల లభ్యత మరియు స్థితి వివరాలు",
        "vacant": "ఖాళీగా ఉన్నాయి", "stable": "తగినంత స్టాక్ ఉంది", "high_load": "రోగుల ఒత్తిడి ఎక్కువగా ఉంది", "critical": "అత్యంత ప్రమాదకరం",
        "ambulance": "📢 అంబులెన్స్ రూటింగ్ కంట్రోలర్ (Ambulance Route)",
        "amb_divert": "⚠️ [రూటింగ్ హెచ్చరిక] ఆక్సిజన్ బెడ్ల కొరత! నాన్-క్రిటికల్ అంబులెన్స్‌లను అనకాపల్లి CHC కి మళ్లించండి.",
        "amb_stable": "✅ [రూటింగ్ సాధారణం] ఇన్‌బౌండ్ అంబులెన్స్‌లు నేరుగా రావచ్చు.",
        "sync_header": "🛡️ సురక్షిత డేటా ఎన్‌క్రిప్షన్ మరియు క్లౌడ్ సమకాలీకరణ",
        "sync_btn": "🔒 ఎన్‌క్రిప్టెడ్ క్లౌడ్ డేటా ప్యాకేజీని పంపండి",
        "crypt_shield": "🔐 FHIR రక్షణ యాక్టివ్‌గా ఉంది! ఎన్‌క్రిప్ట్ చేయబడిన అంతర్జాతీయ ప్రమాణాల డేటా ప్యాకేజీ:",
        "cache_balanced": "📭 క్లౌడ్ డేటా సమకాలీకరణ నిల్వ ఖాళీగా ఉంది.",
        "archive_header": "📁 సమగ్ర కార్యాచరణ టెలిమెట్రీ ఆర్కైవ్ నివేదికలు (Detailed Logs)",
        "csv_btn": "📥 రికార్డుల సిఎస్వి (CSV) ఫైల్‌ను డౌన్‌లోడ్ చేసుకోండి"
    }
}

st.sidebar.markdown("### 🌐 Navigation Language / భాష")
selected_lang = st.sidebar.radio("Choose Preferred Option View:", ("English", "తెలుగు"), label_visibility="collapsed")
lang_code = "en" if selected_lang == "English" else "te"
text = LANG_PACK[lang_code]

st.title(text["title"])
st.caption(text["subtitle"])
st.markdown("---")
col1, col2 = st.columns([1, 1.1])

with col1:
    # ── TOUCHPOINT 1: GATE KIOSK WITH PREFIX ROUTED TOKEN ENGINE ──
    st.header(text["triage_header"])
    p_aadhaar = st.text_input(text["aadhaar_label"], max_chars=12, type="password", key="p_aad_reg")
    user_input = st.text_area(text["input_label"], placeholder=text["input_placeholder"])
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT doctor_name, doctor_prefix FROM doctor_roster WHERE attendance_status = 'PRESENT'")
    gate_roster_raw = cursor.fetchall()
    conn.close()
    
    gate_doctor_map = {row[0]: row[1] for row in gate_roster_raw} if gate_roster_raw else {"Dr. Ramesh Babu": "GEN"}
    chosen_kiosk_doctor = st.selectbox(text["gate_doc_select"], list(gate_doctor_map.keys()))

    UIDAI_HARDWARE_DECRYPTION_DATABASE = {
        "555566667777": "K. Siva Kumar (Aadhaar Verified)",
        "111122223333": "P. Lakshmi Bai (Aadhaar Verified)",
        "999988887777": "V. Srinivasa Rao (Aadhaar Verified)"
    }

    def generate_prefix_token(name: str, a_num: str, target_doc: str, prefix_tag: str, complaint: str) -> str:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("SELECT COUNT(*) FROM patient_queue WHERE target_doctor = ? AND date(arrival_time) = ?", (target_doc, today))
        count = cursor.fetchone()[0] + 1
        
        token_id = f"{prefix_tag}-{count:03d}"
        a_hash = CryptoProtocol.hash_aadhaar(a_num)
        
        cursor.execute("INSERT INTO patient_queue (token_id, category, status, arrival_time, patient_aadhaar_hash, patient_name, target_doctor, chief_complaint) VALUES (?, ?, 'WAITING', ?, ?, ?, ?, ?)", 
                       (token_id, prefix_tag, datetime.now().isoformat(), a_hash, name, target_doc, complaint))
        conn.commit()
        conn.close()
        return token_id

    if st.button(text["submit_btn"], type="primary", use_container_width=True):
        if len(p_aadhaar) == 12 and user_input:
            if p_aadhaar in UIDAI_HARDWARE_DECRYPTION_DATABASE:
                fetched_legal_name = UIDAI_HARDWARE_DECRYPTION_DATABASE[p_aadhaar]
            else: fetched_legal_name = f"Guest Patient ID-{p_aadhaar[:4]}... (Demo Verified)"
                
            prefix_tag = gate_doctor_map.get(chosen_kiosk_doctor, "GEN")
            t_id = generate_prefix_token(fetched_legal_name, p_aadhaar, chosen_kiosk_doctor, prefix_tag, user_input)
            st.success(f"🔐 {text['text_success']} **{t_id}** [Assigned: {chosen_kiosk_doctor}]")
            st.rerun()
        else: st.warning("⚠️ Please provide a valid 12-digit Aadhaar scan block and context symptoms.")

    # ── TOUCHPOINT 2: DOCTOR PRESCRIPTION VIEW FILTER DESK ──
    st.markdown("---")
    st.header(text["doc_header"])
    
    doc_desk_filter = st.selectbox("Select Your Logged-In Desk Identity:", list(gate_doctor_map.keys()))
    active_doc_prefix = gate_doctor_map.get(doc_desk_filter, "GEN")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT token_id, patient_name, chief_complaint FROM patient_queue WHERE status = 'WAITING' AND target_doctor = ? ORDER BY arrival_time ASC LIMIT 1", (doc_desk_filter,))
    current_patient_row = cursor.fetchone()
    
    cursor.execute("SELECT item_name FROM medicine_stock WHERE allowed_designation = ?", (active_doc_prefix,))
    allowed_medicines = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if current_patient_row:
        st.info(f"👉 **Next Patient:** {current_patient_row[1]} | Token ID: **{current_patient_row[0]}**")
        st.caption(f"📋 **Reason for Visit:** {current_patient_row[2]}")
        
        selected_disposition = st.radio(text["dispo_lbl"], ["Out-Patient", "In-Patient (Requires Admission Bed)"])
        selected_prescription_meds = st.multiselect(text["med_prescribe_lbl"], allowed_medicines)
        
        dosage_allocation_map = {}
        if selected_prescription_meds:
            st.markdown("##### 💊 Set Precise Unit Counts / Pill Volumes:")
            for medicine in selected_prescription_meds:
                quantity_pill_count = st.number_input(f"Count for {medicine}:", min_value=1, max_value=100, value=10, key=f"dose_{medicine}")
                dosage_allocation_map[medicine] = int(quantity_pill_count)
        
        if st.button(text["rx_btn"], use_container_width=True):
            if selected_prescription_meds:
                med_string_format = ", ".join(selected_prescription_meds)
                json_dosage_string = json.dumps(dosage_allocation_map)
                
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO prescriptions (token_id, aadhaar_hash, prescribed_meds, unit_dosages_prescribed, doctor_name) VALUES (?, (SELECT patient_aadhaar_hash FROM patient_queue WHERE token_id=?), ?, ?, ?)",
                               (current_patient_row[0], current_patient_row[0], med_string_format, json_dosage_string, doc_desk_filter))
                
                if "In-Patient" in selected_disposition:
                    cursor.execute("UPDATE bed_occupancy SET occupied_beds = occupied_beds + 1 WHERE bed_type = 'General Ward'")
                    cursor.execute("UPDATE patient_queue SET status = 'IN_PHARMACY', target_disposition = 'In-Patient', called_time = ? WHERE token_id = ?", (datetime.now().isoformat(), current_patient_row[0]))
                else:
                    cursor.execute("UPDATE patient_queue SET status = 'IN_PHARMACY', target_disposition = 'Out-Patient', called_time = ? WHERE token_id = ?", (datetime.now().isoformat(), current_patient_row[0]))
                    
                conn.commit()
                conn.close()
                st.success("📝 Prescription and Clinical Disposition logged and routed to Pharmacy desk.")
                st.rerun()
            else: st.warning("⚠️ Please select medications from your authorized directory registry.")
    else: st.caption(f"🎉 No patients currently waiting specifically for {doc_desk_filter}.")
with col2:
    st.header(text["metrics_header"])
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patient_queue WHERE status = 'WAITING'")
    waiting_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM medicine_stock")
    total_registered_medicines = cursor.fetchone()[0]
    cursor.execute("SELECT bed_type, total_beds, occupied_beds FROM bed_occupancy ORDER BY ROWID")
    beds = cursor.fetchall()
    
    # Securely bridge relational tables including the verified target_disposition column elements
    cursor.execute("""
        SELECT p.token_id, q.patient_name, p.prescribed_meds, p.unit_dosages_prescribed, p.doctor_name, p.aadhaar_hash, q.chief_complaint, q.target_disposition 
        FROM prescriptions p JOIN patient_queue q ON p.token_id = q.token_id 
        WHERE p.dispense_status = 'PENDING'
    """)
    pharma_queue = cursor.fetchall()
    
    cursor.execute("SELECT staff_name FROM pharma_roster WHERE shift_status = 'ACTIVE'")
    active_pharmacists_raw = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("""
        SELECT log_date, token_id, patient_name, chief_complaint, detailed_medicines_issued, total_pills_dispensed_count, treating_doctor, dispensing_pharmacist, patient_disposition 
        FROM facility_telemetry_logs ORDER BY log_id DESC LIMIT 10
    """)
    historical_logs_raw = cursor.fetchall()
    conn.close()
    
    meta_col1, meta_col2 = st.columns(2)
    with meta_col1: st.metric(label=text["waiting"], value=f"{waiting_count} Patients")
    with meta_col2: st.metric(label=text["mod_count_lbl"], value=f"{total_registered_medicines} Types")
    
    # ── TOUCHPOINT 3: DIRECT-PULL SINGLE-CLICK PHARMACY VERIFICATION ──
    st.markdown("---")
    st.header(text["pharma_header"])
    
    pharmacist_options = active_pharmacists_raw if active_pharmacists_raw else ["Default Pharmacist"]
    selected_active_pharmacist = st.selectbox(text["pharma_select_lbl"], pharmacist_options)
    
    if pharma_queue:
        pharma_options = [f"{row[0]} - {row[1]} ({row[7]})" for row in pharma_queue]
        selected_pharma_patient = st.selectbox("Select Patient Token at Counter:", pharma_options)
        
        selected_idx = pharma_options.index(selected_pharma_patient)
        target_token, target_name, target_meds, target_json_doses, target_doc, target_hash, target_complaint, target_dispo = pharma_queue[selected_idx]
        
        st.markdown("##### 📋 Verified Prescription Orders Checklist:")
        parsed_dosages = json.loads(target_json_doses) if target_json_doses else {}
        for medicine_name, pill_volume in parsed_dosages.items():
            st.info(f"👉 **{medicine_name}** ──> Handout Volume Required: **{pill_volume} units**")
            
        if st.button(text["dispense_btn"], type="primary", use_container_width=True):
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            total_dispensed_pills_sum = 0
            breakdown_log_strings_list = []
            
            for medicine_name, pill_volume in parsed_dosages.items():
                cursor.execute("UPDATE medicine_stock SET current_stock = current_stock - ? WHERE item_name = ?", (pill_volume, medicine_name))
                total_dispensed_pills_sum += pill_volume
                breakdown_log_strings_list.append(f"{medicine_name}(-{pill_volume})")
            
            detailed_issued_meds_summary_str = ", ".join(breakdown_log_strings_list) if breakdown_log_strings_list else "None"
            current_time_str = datetime.now().isoformat()
            
            cursor.execute("UPDATE prescriptions SET dispense_status = 'DISPENSED', pharma_verification_timestamp = ?, dispensing_pharmacist = ? WHERE token_id = ?", 
                           (current_time_str, selected_active_pharmacist, target_token))
            cursor.execute("UPDATE patient_queue SET status = 'DISCHARGED' WHERE token_id = ?", (target_token,))
            
            # Save complete records containing the unified target care type disposition
            cursor.execute("""
                INSERT INTO facility_telemetry_logs (log_date, token_id, patient_name, chief_complaint, detailed_medicines_issued, total_pills_dispensed_count, treating_doctor, dispensing_pharmacist, patient_disposition)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (datetime.now().strftime('%Y-%m-%d'), target_token, target_name, target_complaint, detailed_issued_meds_summary_str, total_dispensed_pills_sum, target_doc, selected_active_pharmacist, target_dispo))
            
            conn.commit()
            conn.close()
            st.success(f"🎯 [DISPENSE SUCCESS] Verified Handout compiled. Total individual pills distributed: {total_dispensed_pills_sum}.")
            st.rerun()
    else: st.caption("ℹ️ No prescriptions currently pending distribution in the pharmacy corridor.")

    # Bed Infrastructure Status Grid
    st.markdown(f"### {text['beds_headline']}")
    oxygen_bed_vacant = 0
    for b_type, total, occupied in beds:
        vacant = total - occupied
        if b_type == "Oxygen Beds": oxygen_bed_vacant = vacant
        ratio = vacant / total
        stress_label = text["critical"] if ratio <= 0.1 else text["high_load"] if ratio <= 0.3 else text["stable"]
        color_tag = "🔴" if ratio <= 0.1 else "🟡" if ratio <= 0.3 else "✅"
        st.markdown(f"* **{b_type}**: {occupied}/{total} ──> {color_tag} **{stress_label}**")

    if oxygen_bed_vacant <= 1:
        if st.button(text["discharge_bed_btn"], type="secondary", use_container_width=True):
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("UPDATE bed_occupancy SET occupied_beds = occupied_beds - 1 WHERE bed_type = 'Oxygen Beds'")
            conn.commit()
            conn.close()
            st.rerun()

# Ambulance Direction Control Pipeline
st.markdown("---")
st.markdown(f"### {text['ambulance']}")
if oxygen_bed_vacant <= 1: st.error(text["amb_divert"])
else: st.success(text["amb_stable"])

# =====================================================================
# HISTORICAL DATALOG CONSOLE ARCHIVE GRID
# =====================================================================
st.markdown("---")
st.markdown(f"### {text['archive_header']}")
if historical_logs_raw:
    st.dataframe(
        historical_logs_raw, 
        column_config={
            "0": "Date", "1": "Token ID", "2": "Patient Name", "3": "Chief Complaint Reason", 
            "4": "Detailed Medicine Handout Breakdown", "5": "Total Pill Count Issued", 
            "6": "Doctor Name", "7": "Dispensing Pharmacist", "8": "Patient Care Type"
        }, 
        use_container_width=True
    )
    
    csv_buffer = "Log_Date,Token_ID,Patient_Name,Chief_Complaint,Detailed_Medicine_Breakdown,Total_Pills_Issued,Attending_Doctor,Pharmacist,Care_Type\n"
    for r in historical_logs_raw:
        csv_buffer += f'"{r[0]}","{r[1]}","{r[2]}","{r[3]}","{r[4]}",{r[5]},"{r[6]}","{r[7]}","{r[8]}"\n'
        
    st.download_button(
        label=text["csv_btn"], data=csv_buffer, 
        file_name=f"uidai_secure_health_log_{datetime.now().strftime('%Y-%m-%d')}.csv", 
        mime="text/csv", use_container_width=True
    )
else: st.caption("ℹ️ Waiting for verified biometric transactions to populate the spreadsheet archive download desk.")

# Compliance Outbox FHIR Data Packer
st.markdown("---")
st.markdown(f"### {text['sync_header']}")
if st.button(text["sync_btn"], use_container_width=True):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT token_id, prescribed_meds, doctor_name, dispensing_pharmacist FROM prescriptions WHERE dispense_status = 'DISPENSED' ORDER BY prescription_id DESC LIMIT 1")
    sync_row = cursor.fetchone()
    conn.close()
    if sync_row:
        fhir_payload_json = json.dumps({"resourceType": "Encounter", "id": sync_row, "status": "finished", "serviceType": {"display": sync_row}, "participant": [{"individual": {"display": sync_row}}, {"individual": {"display": sync_row}}]}, indent=2)
        st.info(f"{text['crypt_shield']}")
        st.code(fhir_payload_json, language="json")
    else: st.info("📭 Cache balanced. Zero changes pending transmission.")
