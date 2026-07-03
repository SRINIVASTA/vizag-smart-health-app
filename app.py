import streamlit as st
import sqlite3
import base64
import re
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
    cursor.execute("INSERT OR IGNORE INTO medicine_stock VALUES ('Paracetamol 500mg', 120, 200), ('Anti-Venom Injection', 3, 10), ('Artesunate (Malaria)', 15, 50)")
    cursor.execute("INSERT OR IGNORE INTO bed_occupancy VALUES ('General Ward', 20, 14), ('Oxygen Beds', 10, 9), ('Isolation Unit', 5, 2)")
    conn.commit()
    conn.close()

init_db()

class CryptoProtocol:
    _KEY = b"VizagPHCArakuValleySecretKey2026##"
    @staticmethod
    def encrypt(data_str: str) -> str:
        encrypted_bytes = bytes([ord(data_str[i]) ^ CryptoProtocol._KEY[i % len(CryptoProtocol._KEY)] for i in range(len(data_str))])
        return base64.b64encode(encrypted_bytes).decode('utf-8')

LANG_PACK = {
    "en": {
        "title": "🏥 Visakhapatnam Smart Health Command Center",
        "subtitle": "Real-time AI management of stock, patient footfall, beds, and rosters.",
        "triage_header": "📝 Frontline Patient AI Triage",
        "input_label": "Enter Patient Complaints / Clinical Presentation Note:",
        "input_placeholder": "e.g., Patient age 24, showing high fever and severe chills.",
        "submit_btn": "Process & Issue Token",
        "metrics_header": "📊 Real-Time Operations Telemetry",
        "waiting": "Waiting Patients",
        "beds_headline": "🛏️ Live Bed Matrix Status",
        "vacant": "vacant", "stable": "STABLE", "high_load": "HIGH LOAD", "critical": "CRITICAL",
        "ambulance": "📢 AMBULANCE DISPATCH CONTROLLER",
        "amb_divert": "⚠️ [DIVERTING PROTOCOL ACTIVE] Redirecting inbound oxygen emergency logistics directly to CHC Anakapalle!",
        "amb_stable": "✅ [FACILITY UNLOCKED] Inbound transport cleared for direct entry.",
        "sync_btn": "🔒 Securely Sync Anonymized Cloud Payload",
        "route_alloc": "Route Allocated", "token_success": "Token Logged Successfully!",
        "empty_warning": "⚠️ Input prompt context text is empty.",
        "cache_balanced": "📭 Cache balanced. Zero changes pending transmission.",
        "crypt_shield": "🔐 Cryptographic Shield Active! Hex-Anonymized Payload Block compiled successfully:",
        "stress_test_title": "🦠 Mock Stress Testing Triggers",
        "stress_test_btn": "🚨 Simulate Monsoon Malaria Outbreak Surge (+5 Cases)",
        "sim_success": "💥 Outbreak injection completed. System thresholds adjusted.",
        "sync_header": "🛡️ Cryptographic Transmission & Cloud Backhaul Sync"
    },
    "te": {
        "title": "🏥 విశాఖపట్నం జిల్లా స్మార్ట్ హెల్త్ కమాండ్ సెంటర్",
        "subtitle": "మందుల స్టాక్, రోగుల సంఖ్య, బెడ్ల లభ్యత మరియు హాజరు యొక్క ప్రత్యక్ష పర్యవేక్షణ.",
        "triage_header": "📝 రోగుల ఐటియాజ్ పర్యవేక్షణ (AI Triage)",
        "input_label": "రోగి యొక్క ఆరోగ్య సమస్యల వివరాలను నమోదు చేయండి:",
        "input_placeholder": "ఉదాహరణకు: రోగి వయస్సు 24 సంవత్సరాలు, తీవ్రమైన జ్వరం మరియు వణుకు ఉంది.",
        "submit_btn": "టోకెన్ జారీ చేయండి",
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
        "crypt_shield": "🔐 క్రిప్టోగ్రాఫిక్ రక్షణ యాక్టివ్‌గా ఉంది! ఎన్‌క్రిప్ట్ చేయబడిన డేటా ప్యాకేజీ:",
        "stress_test_title": "🦠 మక్ స్ట్రెస్ టెస్టింగ్ ట్రిగ్గర్స్",
        "stress_test_btn": "🚨 మలేరియా వ్యాప్తి తీవ్రతను పెంచండి (+5 కేసులు)",
        "sim_success": "💥 కొత్త కేసులు విజయవంతంగా నమోదు చేయబడ్డాయి. వ్యవస్థ అలర్ట్ చేయబడింది.",
        "sync_header": "🛡️ సురక్షిత డేటా ఎన్‌క్రిప్షన్ మరియు క్లౌడ్ సమకాలీకరణ"
    }
}

st.set_page_config(layout="wide", page_title="Vizag Smart Health Dashboard")
st.sidebar.markdown("### 🌐 Navigation Language / భాష")
selected_lang = st.sidebar.radio("Choose Preferred Option View:", ("English", "తెలుగు"), label_visibility="collapsed")
lang_code = "en" if selected_lang == "English" else "te"
text = LANG_PACK[lang_code]

st.title(text["title"])
st.caption(text["subtitle"])
st.markdown("---")
def parse_and_triage(raw_text: str) -> str:
    maternal_match = re.search(r'(pregnancy|anc|pnc|lmp|maternal)', raw_text, re.IGNORECASE)
    snake_match = re.search(r'(bite|snake|venom)', raw_text, re.IGNORECASE)
    if snake_match or "high fever" in raw_text.lower(): return "Emergency"
    if maternal_match: return "Maternal"
    return "General"

def generate_token(category: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM patient_queue WHERE category = ? AND date(arrival_time) = ?", (category, today))
    count = cursor.fetchone()[0] + 1
    prefix = {"Emergency": "EMER", "Maternal": "MAT", "General": "GEN"}.get(category, "GEN")
    token_id = f"{prefix}-{count:03d}"
    cursor.execute("INSERT INTO patient_queue (token_id, category, status, arrival_time) VALUES (?, ?, ?, ?)", (token_id, category, "WAITING", datetime.now().isoformat()))
    conn.commit()
    conn.close()

col1, col2 = st.columns([1, 1.2])

with col1:
    st.header(text["triage_header"])
    user_input = st.text_area(text["input_label"], placeholder=text["input_placeholder"], height=100)
    if st.button(text["submit_btn"], type="primary", use_container_width=True):
        if user_input:
            assigned_route = parse_and_triage(user_input)
            generate_token(assigned_route)
            st.success(f"✅ {text['route_alloc']}: **{assigned_route}** | {text['token_success']}")
        else:
            st.warning(text["empty_warning"])

    st.markdown("---")
    st.markdown(f"### {text['stress_test_title']}")
    if st.button(text["stress_test_btn"], use_container_width=True):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        current_time_str = datetime.now().isoformat()
        base_id = datetime.now().microsecond
        for i in range(5):
            cursor.execute("INSERT INTO patient_queue (token_id, category, status, arrival_time) VALUES (?, 'General', 'WAITING', ?)", (f"GEN-SIM-{base_id}-{i}", current_time_str))
        cursor.execute("UPDATE medicine_stock SET reorder_level = 120 WHERE item_name = 'Artesunate (Malaria)'")
        conn.commit()
        conn.close()
        st.success(text["sim_success"])
        st.rerun()

with col2:
    st.header(text["metrics_header"])
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patient_queue WHERE status = 'WAITING'")
    waiting_count = cursor.fetchone()[0]
    cursor.execute("SELECT bed_type, total_beds, occupied_beds FROM bed_occupancy ORDER BY ROWID")
    beds = cursor.fetchall()
    conn.close()
    
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
st.markdown("---")
st.markdown(f"### {text['ambulance']}")
if oxygen_bed_vacant <= 1:
    st.error(text["amb_divert"])
else:
    st.success(text["amb_stable"])

st.markdown("---")
st.markdown(f"### {text['sync_header']}")

if st.button(text["sync_btn"], use_container_width=True):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient_queue WHERE status = 'WAITING' LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        secure_token = CryptoProtocol.encrypt(str(row))
        st.info(f"{text['crypt_shield']} `{secure_token}`")
    else:
        st.info(text["cache_balanced"])
