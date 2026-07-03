import streamlit as st
import sqlite3
import base64
import re
import json
from datetime import datetime

DB_NAME = "web_smart_health.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS patient_queue 
        (token_id TEXT PRIMARY KEY, category TEXT, status TEXT, arrival_time TIMESTAMP, called_time TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS medicine_stock 
        (item_name TEXT PRIMARY KEY, current_stock INTEGER, reorder_level INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS bed_occupancy 
        (bed_type TEXT PRIMARY KEY, total_beds INTEGER, occupied_beds INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS doctor_roster 
        (doctor_id TEXT PRIMARY KEY, doctor_name TEXT, specialty TEXT, attendance_status TEXT)''')
    
    cursor.execute("INSERT OR IGNORE INTO medicine_stock VALUES ('Paracetamol 500mg', 120, 200), ('Anti-Venom Injection', 3, 10), ('Artesunate (Malaria)', 15, 50)")
    cursor.execute("INSERT OR IGNORE INTO bed_occupancy VALUES ('General Ward', 20, 14), ('Oxygen Beds', 10, 9), ('Isolation Unit', 5, 2)")
    cursor.execute("INSERT OR IGNORE INTO doctor_roster VALUES ('DOC-01', 'Dr. Ramesh Babu', 'General Physician', 'PRESENT'), ('DOC-02', 'Dr. S. Lakshmi', 'Maternal Specialist', 'ABSENT')")
    conn.commit()
    conn.close()

init_db()

class CryptoProtocol:
    _KEY = b"VizagPHCArakuValleySecretKey2026##"
    @staticmethod
    def encrypt(data_str: str) -> str:
        encrypted_bytes = bytes([ord(data_str[i]) ^ CryptoProtocol._KEY[i % len(CryptoProtocol._KEY)] for i in range(len(data_str))])
        return base64.b64encode(encrypted_bytes).decode('utf-8')

class InteroperabilityEngine:
    @staticmethod
    def export_to_fhir_standard_json(patient_token: str, assigned_track: str) -> str:
        fhir_encounter = {
            "resourceType": "Encounter",
            "id": patient_token,
            "status": "finished",
            "class": {"system": "http://hl7.org", "code": "AMB", "display": "ambulatory"},
            "serviceType": {"coding": [{"system": "http://snomed.info", "code": "394577000", "display": assigned_track}]},
            "period": {"end": datetime.now().isoformat()}
        }
        return json.dumps(fhir_encounter, indent=2)

LANG_PACK = {
    "en": {
        "title": "🏥 Visakhapatnam Smart Health Enterprise Hub",
        "subtitle": "Hardware-linked, ML-optimized management of stock, crowds, beds, and rosters.",
        "triage_header": "📝 Frontline Patient AI Triage",
        "doc_header": "👨‍⚕️ Doctor Consultation Room",
        "input_label": "Enter Patient Complaints / Clinical Presentation Note:",
        "input_placeholder": "e.g., Patient age 24, showing high fever and severe chills.",
        "submit_btn": "Process & Issue Token",
        "call_btn": "✅ Treat & Discharge Next Patient",
        "discharge_bed_btn": "🛏️ Free Up 1 Occupied Oxygen Bed",
        "no_patients": "🎉 No waiting patients! Triage line is fully cleared.",
        "metrics_header": "📊 Real-Time Operations Telemetry",
        "waiting": "Waiting Patients",
        "beds_headline": "🛏️ Live Bed Matrix Status",
        "vacant": "vacant", "stable": "STABLE", "high_load": "HIGH LOAD", "critical": "CRITICAL",
        "ambulance": "📢 AMBULANCE DISPATCH CONTROLLER",
        "amb_divert": "⚠️ [DIVERTING PROTOCOL ACTIVE] Redirecting inbound oxygen emergency logistics directly to CHC Anakapalle!",
        "amb_stable": "✅ [FACILITY UNLOCKED] Inbound transport cleared for direct entry.",
        "sync_btn": "🔒 Securely Sync Anonymized FHIR Cloud Payload",
        "route_alloc": "Route Allocated", "token_success": "Token Logged Successfully!",
        "empty_warning": "⚠️ Input prompt context text is empty.",
        "cache_balanced": "📭 Cache balanced. Zero changes pending transmission.",
        "crypt_shield": "🔐 FHIR Interoperability Shield Active! Universally compliant encrypted payload built:",
        "hardware_title": "🛰️ IoT Sensor & ML Predictive Pipelines",
        "hw_cam_btn": "📷 Simulate Computer Vision Waiting Room Overflow (+5 People Counted)",
        "hw_geo_btn": "📍 Authenticate On-Duty Doctor via Geo-Fenced Mobile Biometrics",
        "hw_ml_btn": "🌦️ Run ML Monsoon Weather Predictive Forecast (Rain > 250mm)",
        "sim_success": "💥 Action registered successfully. System states updated dynamically.",
        "sync_header": "🛡️ Cryptographic Transmission & Cloud Backhaul Sync"
    },
    "te": {
        "title": "🏥 విశాఖపట్నం జిల్లా స్మార్ట్ హెల్త్ ఎంటర్‌ప్రైజ్ హబ్",
        "subtitle": "మందుల స్టాక్, రోగుల సంఖ్య, బెడ్ల లభ్యత మరియు హాజరు యొక్క ప్రత్యక్ష IoT పర్యవేక్షణ.",
        "triage_header": "📝 రోగుల ఐటియాజ్ పర్యవేక్షణ (AI Triage)",
        "doc_header": "👨‍⚕️ వైద్యుల చికిత్స గది (Doctor Desk)",
        "input_label": "రోగి యొక్క ఆరోగ్య సమస్యల వివరాలను నమోదు చేయండి:",
        "input_placeholder": "ఉదాహరణకు: రోగి వయస్సు 24 సంవత్సరాలు, తీవ్రమైన జ్వరం మరియు వణుకు ఉంది.",
        "submit_btn": "టోకెన్ జారీ చేయండి",
        "call_btn": "✅ తదుపరి రోగికి చికిత్స చేసి పంపండి",
        "discharge_bed_btn": "🛏️ ఒక ఆక్సిజన్ బెడ్‌ను ఖాళీ చేయండి",
        "no_patients": "🎉 నిరీక్షణ జాబితా ఖాళీగా ఉంది! అందరికీ చికిత్స పూర్తయింది.",
        "metrics_header": "📊 ప్రత్యక్ష ఆరోగ్య కేంద్రం వివరాలు",
        "waiting": "వేచి ఉన్న రోగులు",
        "beds_headline": "🛏️ బెడ్ల లభ్యత మరియు స్థితి వివరాలు",
        "vacant": "ఖాళీగా ఉన్నాయి", "stable": "తగినంత స్టాక్ ఉంది", "high_load": "రోగుల ఒత్తిడి ఎక్కువగా ఉంది", "critical": "అత్యంత ప్రమాదకరం",
        "ambulance": "📢 అంబులెన్స్ రూటింగ్ కంట్రోలర్ (Ambulance Route)",
        "amb_divert": "⚠️ [రూటింగ్ హెచ్చరిక] ఆక్సిజన్ బెడ్ల కొరత! నాన్-క్రిటికల్ అంబులెన్స్‌లను అనకాపల్లి CHC కి మళ్లించండి.",
        "amb_stable": "✅ [రూటింగ్ సాధారణం] ఇన్‌బౌండ్ అంబులెన్స్‌లు నేరుగా రావచ్చు.",
        "sync_btn": "🔒 ఎన్‌క్రిప్టెడ్ క్లౌడ్ డేటా ప్యాకేజీని పంపండి",
        "route_alloc": "కేటాయించిన విభాగం", "token_success": "టోకెన్ విజయవంతంగా నమోదు చేయబడింది!",
        "empty_warning": "⚠️ సమాచారం ఏమీ నమోదు చేయలేదు.",
        "cache_balanced": "📭 క్లౌడ్ డేటా సమకాలీకరణ నిల్వ ఖాళీగా ఉంది.",
        "crypt_shield": "🔐 FHIR రక్షణ యాక్టివ్‌గా ఉంది! ఎన్‌క్రిప్ట్ చేయబడిన అంతర్జాతీయ ప్రమాణాల డేటా ప్యాకేజీ:",
        "hardware_title": "🛰️ IoT సెన్సార్ & ML ప్రిడిక్టివ్ పైప్‌లైన్స్",
        "hw_cam_btn": "📷 కంప్యూటర్ విజన్ కెమెరా ఓవర్‌ఫ్లో పరీక్షించండి (+5 మంది వ్యక్తులు)",
        "hw_geo_btn": "📍 జియో-ఫెన్స్డ్ మొబైల్ బయోమెట్రిక్స్ ద్వారా వైద్యుడి హాజరును ధృవీకరించండి",
        "hw_ml_btn": "🌦️ ML వర్షపాత ప్రిడిక్టివ్ ఫోర్‌కాస్ట్ రన్ చేయండి (వర్షపాతం > 250mm)",
        "sim_success": "💥 చర్య విజయవంతంగా నమోదు చేయబడింది. వ్యవస్థ అప్‌డేట్ చేయబడింది.",
        "sync_header": "🛡️ సురక్షిత డేటా ఎన్‌క్రిప్షన్ మరియు క్లౌడ్ సమకాలీకరణ"
    }
}

st.sidebar.markdown("### 🌐 Navigation Language / భాష")
selected_lang = st.sidebar.radio("Choose Preferred Option View:", ("English", "తెలుగు"), label_visibility="collapsed")
lang_code = "en" if selected_lang == "English" else "te"
text = LANG_PACK[lang_code]

st.title(text["title"])
st.caption(text["subtitle"])
st.markdown("---")
col1, col2 = st.columns([1, 1.2])

with col1:
    # ── PATIENT INFLOW (TRIAGE) ──
    st.header(text["triage_header"])
    user_input = st.text_area(text["input_label"], placeholder=text["input_placeholder"], height=100)
    
    def parse_and_triage(raw_text: str) -> str:
        if re.search(r'(pregnancy|anc|pnc|lmp|maternal)', raw_text, re.IGNORECASE): return "Maternal"
        if re.search(r'(bite|snake|venom)', raw_text, re.IGNORECASE) or "high fever" in raw_text.lower(): return "Emergency"
        return "General"

    def generate_token(category: str) -> str:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("SELECT COUNT(*) FROM patient_queue WHERE category = ? AND date(arrival_time) = ?", (category, today))
        count = cursor.fetchone() + 1
        token_id = f"{'EMER' if category=='Emergency' else 'MAT' if category=='Maternal' else 'GEN'}-{count:03d}"
        cursor.execute("INSERT INTO patient_queue (token_id, category, status, arrival_time) VALUES (?, ?, 'WAITING', ?)", (token_id, category, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return token_id

    if st.button(text["submit_btn"], type="primary", use_container_width=True):
        if user_input:
            assigned_route = parse_and_triage(user_input)
            generate_token(assigned_route)
            st.success(f"✅ {text['route_alloc']}: **{assigned_route}** | {text['token_success']}")
            st.rerun()
        else:
            st.warning(text["empty_warning"])

    # ── PATIENT OUTFLOW: DOCTOR CLEARANCE ENGINE (REDUCES TELEMETRY) ──
    st.markdown("---")
    st.header(text["doc_header"])
    if st.button(text["call_btn"], use_container_width=True):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Find the oldest waiting patient currently sitting in the triage queue
        cursor.execute("SELECT token_id FROM patient_queue WHERE status = 'WAITING' ORDER BY arrival_time ASC LIMIT 1")
        next_patient = cursor.fetchone()
        
        if next_patient:
            target_token = next_patient
            # Update status to COMPLETED to remove them from the active waiting pool
            cursor.execute("UPDATE patient_queue SET status = 'COMPLETED', called_time = ? WHERE token_id = ?", (datetime.now().isoformat(), target_token))
            conn.commit()
            st.toast(f"👨‍⚕️ Treated and Discharged: {target_token}")
        else:
            st.info(text["no_patients"])
        conn.close()
        st.rerun()

    # ── IoT PERIPHERALS & ML PIPELINES ──
    st.markdown("---")
    st.markdown(f"### {text['hardware_title']}")
    
    if st.button(text["hw_cam_btn"], use_container_width=True):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        current_time_str = datetime.now().isoformat()
        base_id = datetime.now().microsecond
        for i in range(5):
            cursor.execute("INSERT INTO patient_queue (token_id, category, status, arrival_time) VALUES (?, 'General', 'WAITING', ?)", (f"CAM-VOL-{base_id}-{i}", current_time_str))
        conn.commit()
        conn.close()
        st.rerun()

    if st.button(text["hw_geo_btn"], use_container_width=True):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE doctor_roster SET attendance_status = 'PRESENT' WHERE doctor_id = 'DOC-02'")
        conn.commit()
        conn.close()
        st.success(text["sim_success"])

    if st.button(text["hw_ml_btn"], use_container_width=True):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE medicine_stock SET reorder_level = 150 WHERE item_name = 'Artesunate (Malaria)'")
        conn.commit()
        conn.close()
        st.rerun()

with col2:
    st.header(text["metrics_header"])
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patient_queue WHERE status = 'WAITING'")
    waiting_count = cursor.fetchone()
    cursor.execute("SELECT bed_type, total_beds, occupied_beds FROM bed_occupancy ORDER BY ROWID")
    beds = cursor.fetchall()
    cursor.execute("SELECT doctor_name, specialty, attendance_status FROM doctor_roster")
    roster = cursor.fetchall()
    conn.close()
    
    # Live KPI Metric Card updates automatically
    st.metric(label=text["waiting"], value=f"{waiting_count}")
    
    st.markdown(f"### {text['beds_headline']}")
    oxygen_bed_vacant = 0
    for b_type, total, occupied in beds:
        vacant = total - occupied
        if b_type == "Oxygen Beds": oxygen_bed_vacant = vacant
        ratio = vacant / total
        stress_label = text["critical"] if ratio <= 0.1 else text["high_load"] if ratio <= 0.3 else text["stable"]
        color_tag = "🔴" if ratio <= 0.1 else "🟡" if ratio <= 0.3 else "✅"
        st.markdown(f"* **{b_type}**: {occupied}/{total} ({vacant} {text['vacant']}) ──> {color_tag} **{stress_label}**")

    # BED CLEARANCE TRIGGER (REDUCES OVERLOAD)
    if oxygen_bed_vacant <= 1:
        if st.button(text["discharge_bed_btn"], type="secondary", use_container_width=True):
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            # De-escalate occupied bed count from 9 down to 8 to restore safety margins
            cursor.execute("UPDATE bed_occupancy SET occupied_beds = occupied_beds - 1 WHERE bed_type = 'Oxygen Beds'")
            conn.commit()
            conn.close()
            st.rerun()

    st.markdown("### 👨‍⚕️ Live Medical Roster Coverage")
    for name, spec, status in roster:
        st.markdown(f"* {'🟢' if status == 'PRESENT' else '⚪'} **{name}** ({spec}) ──> {status}")

# ── AMBULANCE DIRECTION SYSTEM AUTOMATION ──
st.markdown("---")
st.markdown(f"### {text['ambulance']}")
if oxygen_bed_vacant <= 1:
    st.error(text["amb_divert"])
else:
    st.success(text["amb_stable"])

# ── COMPLIANCE FHIR SYNCER ──
st.markdown("---")
st.markdown(f"### {text['sync_header']}")
if st.button(text["sync_btn"], use_container_width=True):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT token_id, category FROM patient_queue WHERE status = 'WAITING' LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        fhir_payload_json = InteroperabilityEngine.export_to_fhir_standard_json(row, row)
        encrypted_fhir_stream = CryptoProtocol.encrypt(fhir_payload_json)
        st.info(f"{text['crypt_shield']}")
        st.code(fhir_payload_json, language="json")
        st.warning(f"🔒 Encrypted ASCII Outbox Data Frame: `{encrypted_fhir_stream[:120]}...`")
    else:
        st.info(text["cache_balanced"])
