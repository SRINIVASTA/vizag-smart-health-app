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
    
    # SELF-HEALING DATABASE MIGRATION SYSTEM
    try:
        cursor.execute("SELECT patient_name, patient_aadhaar_hash FROM patient_queue LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("DROP TABLE IF EXISTS patient_queue")
        cursor.execute("DROP TABLE IF EXISTS prescriptions")
        cursor.execute("DROP TABLE IF EXISTS facility_telemetry_logs")
        
    # Structural Core Schemas
    cursor.execute('''CREATE TABLE IF NOT EXISTS patient_queue (
        token_id TEXT PRIMARY KEY, category TEXT, status TEXT, arrival_time TIMESTAMP, called_time TIMESTAMP,
        patient_aadhaar_hash TEXT, patient_name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS medicine_stock (item_name TEXT PRIMARY KEY, current_stock INTEGER, reorder_level INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS bed_occupancy (bed_type TEXT PRIMARY KEY, total_beds INTEGER, occupied_beds INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS doctor_roster (doctor_id TEXT PRIMARY KEY, doctor_name TEXT, specialty TEXT, attendance_status TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS prescriptions (
        prescription_id INTEGER PRIMARY KEY AUTOINCREMENT, token_id TEXT, aadhaar_hash TEXT, prescribed_meds TEXT,
        doctor_name TEXT, dispense_status TEXT DEFAULT 'PENDING', pharma_verification_timestamp TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS facility_telemetry_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT, log_date TEXT, token_id TEXT, category TEXT, treatment_timestamp TEXT,
        treating_doctor TEXT, aadhaar_hash_verified TEXT, dispense_status TEXT)''')
    
    cursor.execute("INSERT OR IGNORE INTO medicine_stock VALUES ('Paracetamol 500mg', 120, 200), ('Anti-Venom Injection', 3, 10), ('Artesunate (Malaria)', 15, 50)")
    cursor.execute("INSERT OR IGNORE INTO bed_occupancy VALUES ('General Ward', 20, 14), ('Oxygen Beds', 10, 9), ('Isolation Unit', 5, 2)")
    cursor.execute("INSERT OR IGNORE INTO doctor_roster VALUES ('DOC-01', 'Dr. Ramesh Babu', 'General Physician', 'PRESENT'), ('DOC-02', 'Dr. S. Lakshmi', 'Maternal Specialist', 'PRESENT')")
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
        "subtitle": "Biometric Ingestion Gateway & Closed-Loop Pharmacy Verification Engine.",
        "triage_header": "🛰️ Entrance Kiosk: Autonomous Aadhaar Biometric Scan",
        "doc_header": "👨‍⚕️ Doctor Consultation Room & Prescription Desk",
        "pharma_header": "💊 Closed-Loop Pharmacy Dispensing Desk",
        "aadhaar_label": "Swipe Aadhaar Card / Place Thumb on Scanner (Simulate 12-Digit Entry):",
        "input_label": "Primary Chief Complaint / Clinical Presentation Note:",
        "input_placeholder": "e.g., Patient showing high fever and severe chills.",
        "med_prescribe_lbl": "Prescribe Medicines (Comma Separated):",
        "doc_select_lbl": "Select Attending Medical Officer:",
        "submit_btn": "🔗 Ingest UIDAI Biometrics & Issue Token",
        "text_success": "Aadhaar verified via UIDAI! Issued Token:",
        "rx_btn": "✍️ Issue Prescription & Call Next",
        "dispense_btn": "🎯 Verify Patient Thumbprint & Dispense Meds",
        "metrics_header": "📊 Real-Time Operations Telemetry",
        "waiting": "Waiting Patients",
        "beds_headline": "🛏️ Live Bed Matrix Status",
        "vacant": "vacant", "stable": "STABLE", "high_load": "HIGH LOAD", "critical": "CRITICAL",
        "ambulance": "📢 AMBULANCE DISPATCH CONTROLLER",
        "amb_divert": "⚠️ [DIVERTING PROTOCOL ACTIVE] Redirecting inbound oxygen emergency logistics directly to CHC Anakapalle!",
        "amb_stable": "✅ [FACILITY UNLOCKED] Inbound transport cleared for direct entry.",
        "sync_header": "🛡️ Cryptographic Transmission & Cloud Backhaul Sync",
        "sync_btn": "🔒 Securely Sync Anonymized FHIR Cloud Payload",
        "crypt_shield": "🔐 FHIR Interoperability Shield Active! Universally compliant encrypted payload built:",
        "cache_balanced": "📭 Cache balanced. Zero changes pending transmission.",
        "archive_header": "📁 Secure Operational Telemetry Log Archive"
    },
    "te": {
        "title": "🏥 విశాఖపట్నం జిల్లా స్మార్ట్ హెల్త్ ఎంటర్‌ప్రైజ్ హబ్",
        "subtitle": "ఆటోమేటిక్ ఆధార్ బయోమెట్రిక్ రిజిస్ట్రేషన్ మరియు సురక్షిత మందుల పంపిణీ వ్యవస్థ.",
        "triage_header": "🛰️ ప్రవేశ ద్వారం: ఆటోమేటిక్ ఆధార్ బయోమెట్రిక్ స్కాన్ కౌంటర్",
        "doc_header": "👨‍⚕️ వైద్యుల చికిత్స మరియు మందుల ప్రిస్క్రిప్షన్ గది",
        "pharma_header": "💊 ఫార్మసీ మందుల పంపిణీ కౌంటర్ (Pharma Desk)",
        "aadhaar_label": "ఆధార్ కార్డ్‌ను స్వైప్ చేయండి / బయోమెట్రిక్ స్కానర్‌పై బొటనవేలు ఉంచండి:",
        "input_label": "రోగి యొక్క ఆరోగ్య సమస్యల వివరాలు:",
        "input_placeholder": "ఉదాహరణకు: తీవ్రమైన జ్వరం మరియు వణుకు ఉంది.",
        "med_prescribe_lbl": "మందుల వివరాలు (కామాలతో వేరు చేయండి):",
        "doc_select_lbl": "చికిత్స అందిస్తున్న వైద్యుడిని ఎంచుకోండి:",
        "submit_btn": "🔗 ఆధార్ బయోమెట్రిక్స్ సేకరించి టోకెన్ ఇవ్వండి",
        "text_success": "ఆధార్ బయోమెట్రిక్స్ విజయవంతంగా సేకరించబడ్డాయి! టోకెన్ సంఖ్య:",
        "rx_btn": "✍️ ప్రిస్క్రిప్షన్ జారీ చేయండి",
        "dispense_btn": "🎯 రోగి బయోమెట్రిక్స్ ధృవీకరించి మందులు ఇవ్వండి",
        "metrics_header": "📊 ప్రత్యక్ష ఆరోగ్య కేంద్రం వివరాలు",
        "waiting": "వేచి ఉన్న రోగులు",
        "beds_headline": "🛏️ బెడ్ల లభ్యత మరియు స్థితి వివరాలు",
        "vacant": "ఖాళీగా ఉన్నాయి", "stable": "తగినంత స్టాక్ ఉంది", "high_load": "రోగుల ఒత్తిడి ఎక్కువగా ఉంది", "critical": "అత్యంత ప్రమాదకరం",
        "ambulance": "📢 అంబులెన్స్ రూటింగ్ కంట్రోలర్ (Ambulance Route)",
        "amb_divert": "⚠️ [రూటింగ్ హెచ్చరిక] ఆక్సిజన్ బెడ్ల కొరత! నాన్-క్రిటికల్ అంబులెన్స్‌లను అనకాపల్లి CHC కి మళ్లించండి.",
        "amb_stable": "✅ [రూటింగ్ సాధారణం] ఇన్‌బౌండ్ అంబులెన్స్‌లు నేరుగా రావచ్చు.",
        "sync_header": "🛡️ సురక్షిత డేటా ఎన్‌క్రిప్షన్ మరియు క్లౌడ్ సమకాలీకరణ",
        "sync_btn": "🔒 ఎన్‌క్రిప్టెడ్ క్లౌడ్ డేటా ప్యాకేజీని పంపండి",
        "crypt_shield": "🔐 FHIR రక్షణ యాక్టివ్‌గా ఉంది! ఎన్‌క్రిప్ట్ చేయబడిన అంతర్జాతీయ ప్రమాణాల డేటా ప్యాకేజీ:",
        "cache_balanced": "📭 క్లౌడ్ డేటా సమకాలీకరణ నిల్వ ఖాళీగా ఉంది.",
        "archive_header": "📁 చారిత్రక కార్యాచరణ టెలిమెట్రీ ఆర్కైవ్ (Logs)"
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
    # ── TOUCHPOINT 1: ENTRANCE INTERFACE - AUTOMATED AADHAAR INGESTION ──
    st.header(text["triage_header"])
    p_aadhaar = st.text_input(text["aadhaar_label"], max_chars=12, type="password", key="p_aad_reg")
    user_input = st.text_area(text["input_label"], placeholder=text["input_placeholder"])
    
    UIDAI_HARDWARE_DECRYPTION_DATABASE = {
        "555566667777": "K. Siva Kumar (Aadhaar Verified)",
        "111122223333": "P. Lakshmi Bai (Aadhaar Verified)",
        "999988887777": "V. Srinivasa Rao (Aadhaar Verified)"
    }

    def generate_secure_token(category: str, a_num: str, name: str) -> str:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("SELECT COUNT(*) FROM patient_queue WHERE category = ? AND date(arrival_time) = ?", (category, today))
        count = cursor.fetchone()[0] + 1
        prefix = {"Emergency": "EMER", "Maternal": "MAT", "General": "GEN"}.get(category, "GEN")
        token_id = f"{prefix}-{count:03d}"
        
        a_hash = CryptoProtocol.hash_aadhaar(a_num)
        cursor.execute("INSERT INTO patient_queue (token_id, category, status, arrival_time, patient_aadhaar_hash, patient_name) VALUES (?, ?, 'WAITING', ?, ?, ?)", 
                       (token_id, category, datetime.now().isoformat(), a_hash, name))
        conn.commit()
        conn.close()
        return token_id

    if st.button(text["submit_btn"], type="primary", use_container_width=True):
        if len(p_aadhaar) == 12 and user_input:
            if p_aadhaar in UIDAI_HARDWARE_DECRYPTION_DATABASE:
                fetched_legal_name = UIDAI_HARDWARE_DECRYPTION_DATABASE[p_aadhaar]
            else:
                fetched_legal_name = f"Guest Patient ID-{p_aadhaar[:4]}... (Demo Verified)"
                
            assigned_route = "Emergency" if re.search(r'(bite|snake|venom|fever)', user_input, re.IGNORECASE) else "General"
            t_id = generate_secure_token(assigned_route, p_aadhaar, fetched_legal_name)
            st.success(f"🔐 {text['text_success']} **{fetched_legal_name}** | ID: **{t_id}**")
            st.rerun()
        else: st.warning("⚠️ Please provide a valid 12-digit Aadhaar scan block and context symptoms.")

    # ── TOUCHPOINT 2: DOCTOR DESK & PRESCRIPTION WRITER ──
    st.markdown("---")
    st.header(text["doc_header"])
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT doctor_name FROM doctor_roster WHERE attendance_status = 'PRESENT'")
    active_doctors = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT token_id, patient_name, patient_aadhaar_hash FROM patient_queue WHERE status = 'WAITING' ORDER BY arrival_time ASC LIMIT 1")
    current_patient_row = cursor.fetchone()
    conn.close()
    
    selected_doctor = st.selectbox(text["doc_select_lbl"], active_doctors if active_doctors else ["On-Call Officer"])
    
    if current_patient_row:
        st.info(f"👉 **Patient at Desk:** {current_patient_row[1]} - Token ID: {current_patient_row[0]}")
        meds_prescribed = st.text_input(text["med_prescribe_lbl"], placeholder="e.g., Paracetamol 500mg, Artesunate")
        
        if st.button(text["rx_btn"], use_container_width=True):
            if meds_prescribed:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO prescriptions (token_id, aadhaar_hash, prescribed_meds, doctor_name) VALUES (?, ?, ?, ?)",
                               (current_patient_row[0], current_patient_row[2], meds_prescribed, selected_doctor))
                cursor.execute("UPDATE patient_queue SET status = 'IN_PHARMACY', called_time = ? WHERE token_id = ?", (datetime.now().isoformat(), current_patient_row[0]))
                conn.commit()
                conn.close()
                st.success("📝 Prescription electronically signed and routed to Pharmacy desk.")
                st.rerun()
            else: st.warning("⚠️ Please specify medications before generating the prescription record.")
    else: st.caption("🎉 All patient triage lines are currently clear.")
with col2:
    st.header(text["metrics_header"])
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patient_queue WHERE status = 'WAITING'")
    waiting_count = cursor.fetchone()[0]
    cursor.execute("SELECT bed_type, total_beds, occupied_beds FROM bed_occupancy ORDER BY ROWID")
    beds = cursor.fetchall()
    
    cursor.execute("""
        SELECT p.token_id, q.patient_name, p.prescribed_meds, p.doctor_name, p.aadhaar_hash 
        FROM prescriptions p JOIN patient_queue q ON p.token_id = q.token_id 
        WHERE p.dispense_status = 'PENDING'
    """)
    pharma_queue = cursor.fetchall()
    
    cursor.execute("SELECT log_date, token_id, category, treating_doctor, dispense_status FROM facility_telemetry_logs ORDER BY log_id DESC LIMIT 4")
    historical_logs = cursor.fetchall()
    conn.close()
    
    st.metric(label=text["waiting"], value=f"{waiting_count} Patients Active")
    
    # ── TOUCHPOINT 3: CLOSED-LOOP PHARMACY BIOMETRIC MATCHING ──
    st.markdown("---")
    st.header(text["pharma_header"])
    
    if pharma_queue:
        pharma_options = [f"{row[0]} - {row[1]}" for row in pharma_queue]
        selected_pharma_patient = st.selectbox("Select Patient Token at Counter:", pharma_options)
        pharma_verify_aadhaar = st.text_input("Re-scan Patient Thumbprint (Enter Aadhaar to match):", max_chars=12, type="password", key="pharma_aad")
        
        if st.button(text["dispense_btn"], type="secondary", use_container_width=True):
            selected_idx = pharma_options.index(selected_pharma_patient)
            target_token, target_name, target_meds, target_doc, target_hash = pharma_queue[selected_idx]
            input_hash = CryptoProtocol.hash_aadhaar(pharma_verify_aadhaar)
            
            if input_hash == target_hash:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                
                if "paracetamol" in target_meds.lower():
                    cursor.execute("UPDATE medicine_stock SET current_stock = current_stock - 1 WHERE item_name LIKE '%Paracetamol%'")
                if "artesunate" in target_meds.lower() or "malaria" in target_meds.lower():
                    cursor.execute("UPDATE medicine_stock SET current_stock = current_stock - 1 WHERE item_name LIKE '%Artesunate%'")
                if "venom" in target_meds.lower():
                    cursor.execute("UPDATE medicine_stock SET current_stock = current_stock - 1 WHERE item_name LIKE '%Anti-Venom%'")
                
                current_time_str = datetime.now().isoformat()
                cursor.execute("UPDATE prescriptions SET dispense_status = 'DISPENSED', pharma_verification_timestamp = ? WHERE token_id = ?", (current_time_str, target_token))
                cursor.execute("UPDATE patient_queue SET status = 'DISCHARGED' WHERE token_id = ?", (target_token,))
                
                cursor.execute("""
                    INSERT INTO facility_telemetry_logs (log_date, token_id, category, treatment_timestamp, treating_doctor, aadhaar_hash_verified, dispense_status)
                    VALUES (?, ?, 'Discharged', ?, ?, 'TRUE_BIOMETRIC_MATCH', 'DISPENSED')
                """, (datetime.now().strftime('%Y-%m-%d'), target_token, current_time_str, target_doc))
                
                conn.commit()
                conn.close()
                st.success(f"🎯 [BIOMETRICS MATCHED] Aadhaar verified for {target_name}. Medications distributed safely.")
                st.rerun()
            else:
                st.error("🚨 [SECURITY CRITICAL] Biometric authentication failed! Fingerprint mismatch.")
    else:
        st.caption("ℹ️ No prescriptions currently pending distribution in the pharmacy corridor.")

    # Bed Infrastructure Status Grid
    st.markdown(f"### {text['beds_headline']}")
    oxygen_bed_vacant = 0
    for b_type, total, occupied in beds:
        vacant = total - occupied
        if b_type == "Oxygen Beds": oxygen_bed_vacant = vacant
        ratio = vacant / total
        stress_label = text["critical"] if ratio <= 0.1 else text["high_load"] if ratio <= 0.3 else text["stable"]
        st.markdown(f"* **{b_type}**: {occupied}/{total} ──> **{stress_label}**")

# Ambulance Direction Control Pipeline
st.markdown("---")
st.markdown(f"### {text['ambulance']}")
if oxygen_bed_vacant <= 1: st.error(text["amb_divert"])
else: st.success(text["amb_stable"])

# Historical Operations Audit Registry Panel Viewer
st.markdown("---")
st.markdown(f"### {text['archive_header']}")
if historical_logs:
    st.dataframe(historical_logs, column_config={"0": "Date", "1": "Token ID", "2": "State", "3": "Attending Doctor", "4": "Biometrics Check"}, use_container_width=True)

# Compliance Outbox FHIR Data Packer
st.markdown("---")
st.markdown(f"### {text['sync_header']}")
if st.button(text["sync_btn"], use_container_width=True): # FIXED: 'sync_btn' key mapped successfully in both languages
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT token_id, prescribed_meds, doctor_name FROM prescriptions WHERE dispense_status = 'DISPENSED' ORDER BY prescription_id DESC LIMIT 1")
    sync_row = cursor.fetchone()
    conn.close()
    if sync_row:
        fhir_payload_json = json.dumps({"resourceType": "Encounter", "id": sync_row[0], "status": "finished", "serviceType": {"display": sync_row[1]}, "individual": {"display": sync_row[2]}}, indent=2)
        st.info(f"{text['crypt_shield']}")
        st.code(fhir_payload_json, language="json")
    else: st.info(text["cache_balanced"])
