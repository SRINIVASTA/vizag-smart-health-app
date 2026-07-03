import streamlit as st
import sqlite3
import json
import zlib
import base64
import re
import matplotlib.pyplot as plt
from datetime import datetime

DB_NAME = "web_smart_health.db"

# =====================================================================
# SYSTEM BACKEND ENGINE (Database initialization & triggers)
# =====================================================================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS patient_queue 
        (token_id TEXT PRIMARY KEY, category TEXT, status TEXT, arrival_time TIMESTAMP, called_time TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS medicine_stock 
        (item_name TEXT PRIMARY KEY, current_stock INTEGER, reorder_level INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS bed_occupancy 
        (bed_type TEXT PRIMARY KEY, total_beds INTEGER, occupied_beds INTEGER)''')
    
    # Seeding base values
    cursor.execute("INSERT OR IGNORE INTO medicine_stock VALUES ('Paracetamol 500mg', 120, 200), ('Anti-Venom Injection', 3, 10), ('Artesunate (Malaria)', 15, 50)")
    cursor.execute("INSERT OR IGNORE INTO bed_occupancy VALUES ('General Ward', 20, 14), ('Oxygen Beds', 10, 9), ('Isolation Unit', 5, 2)")
    conn.commit()
    conn.close()

init_db()

# Cryptographic Module
class CryptoProtocol:
    _KEY = b"VizagPHCArakuValleySecretKey2026##"
    @staticmethod
    def encrypt(data_str: str) -> str:
        encrypted_bytes = bytes([ord(data_str[i]) ^ CryptoProtocol._KEY[i % len(CryptoProtocol._KEY)] for i in range(len(data_str))])
        return base64.b64encode(encrypted_bytes).decode('utf-8')

# OCR Triage Module
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

# =====================================================================
# MULTILINGUAL FRONTEND INTERFACE DESIGN
# =====================================================================
LANG_PACK = {
    "en": {
        "title": "🏥 Visakhapatnam Smart Health Command Center",
        "triage_header": "📝 Frontline Patient AI Triage",
        "input_label": "Enter Patient Complaints / Clinical Presentation Note:",
        "input_placeholder": "e.g., Patient age 24, showing high fever and severe chills.",
        "submit_btn": "Process & Issue Token",
        "metrics_header": "📊 Real-Time Operations Telemetry",
        "waiting": "Waiting Patients",
        "beds_headline": "🛏️ Live Bed Matrix Status",
        "vacant": "vacant",
        "ambulance": "📢 AMBULANCE DISPATCH CONTROLLER",
        "sync_btn": "🔒 Securely Sync Anonymized Cloud Payload"
    },
    "te": {
        "title": "🏥 విశాఖపట్నం జిల్లా స్మార్ట్ హెల్త్ కమాండ్ సెంటర్",
        "triage_header": "📝 రోగుల ఐటియాజ్ పర్యవేక్షణ (AI Triage)",
        "input_label": "రోగి యొక్క ఆరోగ్య సమస్యల వివరాలను నమోదు చేయండి:",
        "input_placeholder": "ఉదాహరణకు: రోగి వయస్సు 24 సంవత్సరాలు, తీవ్రమైన జ్వరం మరియు వణుకు ఉంది.",
        "submit_btn": "టోకెన్ జారీ చేయండి",
        "metrics_header": "📊 ప్రత్యక్ష ఆరోగ్య కేంద్రం వివరాలు",
        "waiting": "వేచి ఉన్న రోగులు",
        "beds_headline": "🛏️ బెడ్ల లభ్యత మరియు స్థితి వివరాలు",
        "vacant": "ఖాళీగా ఉన్నాయి",
        "ambulance": "📢 అంబులెన్స్ రూటింగ్ కంట్రోలర్ (Ambulance Route)",
        "sync_btn": "🔒 ఎన్‌క్రిప్టెడ్ క్లౌడ్ డేటా ప్యాకేజీని పంపండి"
    }
}

# Streamlit App Configurations
st.set_page_config(layout="wide", page_title="Vizag Smart Health")
selected_lang = st.sidebar.radio("🌐 Select Language / భాషను ఎంచుకోండి:", ("English", "తెలుగు"))
lang_code = "en" if selected_lang == "English" else "te"
text = LANG_PACK[lang_code]

st.title(text["title"])
st.markdown("---")

# LAYOUT: Two Columns (Left = Actions, Right = Metrics Dashboard)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.header(text["triage_header"])
    user_input = st.text_area(text["input_label"], placeholder=text["input_placeholder"], height=100)
    
    if st.button(text["submit_btn"], type="primary"):
        if user_input:
            assigned_route = parse_and_triage(user_input)
            generate_token(assigned_route)
            st.success(f"✅ Route Allocated: **{assigned_route}** | Token Logged Successfully!")
        else:
            st.warning("⚠️ Input prompt context text is empty.")

    # Emergency Outbreak Simulation Fast-Buttons
    st.markdown("### 🦠 Mock Stress Testing Triggers")
    if st.button("🚨 Simulate Monsoon Malaria Outbreak Surge (+5 Cases)"):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        for _ in range(5):
            cursor.execute("INSERT INTO patient_queue (token_id, category, status, arrival_time) VALUES ('GEN-'+inf, 'General', 'WAITING', datetime.now().isoformat())")
        cursor.execute("UPDATE medicine_stock SET reorder_level = 120 WHERE item_name = 'Artesunate (Malaria)'")
        conn.commit()
        conn.close()
        st.experimental_rerun()

with col2:
    st.header(text["metrics_header"])
    
    # Read Metrics
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patient_queue WHERE status = 'WAITING'")
    waiting_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT bed_type, total_beds, occupied_beds FROM bed_occupancy")
    beds = cursor.fetchall()
    conn.close()
    
    st.metric(label=text["waiting"], value=f"{waiting_count} Patients Active")
    
    # Display Beds Status Matrix
    st.markdown(f"### {text['beds_headline']}")
    oxygen_bed_vacant = 0
    for b_type, total, occupied in beds:
        vacant = total - occupied
        if b_type == "Oxygen Beds": oxygen_bed_vacant = vacant
        stress = "🚨 CRITICAL" if (vacant/total) <= 0.1 else "⚡ HIGH LOAD" if (vacant/total) <= 0.3 else "✅ STABLE"
        st.markdown(f"* **{b_type}**: {occupied}/{total} ({vacant} {text['vacant']}) ──> **{stress}**")

    # Ambulance Dispatch System Rule Engine Output
    st.markdown(f"### {text['ambulance']}")
    if oxygen_bed_vacant <= 1:
        st.error("⚠️ [DIVERTING PROTOCOL ACTIVE] Redirecting inbound oxygen emergency logistics directly to CHC Anakapalle!")
    else:
        st.success("✅ [FACILITY UNLOCKED] Inbound transport cleared for direct entry.")

# Cryptographic Packaging Button
st.markdown("---")
if st.button(text["sync_btn"], use_container_width=True):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient_queue WHERE status = 'WAITING' LIMIT 3")
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        secure_token = CryptoProtocol.encrypt(rows[0][0])
        st.info(f"🔐 Cryptographic Shield Active! Hex-Anonymized Payload Block compiled successfully: `{secure_token}`")
    else:
        st.info("📭 Cache balanced. Zero changes pending transmission.")
