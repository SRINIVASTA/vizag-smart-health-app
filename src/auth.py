import sqlite3

USER_REGISTRY = {
    "ap_state_admin": {"password": "AmaravatiHealth2026!", "role": "State Surveillance"},
    "district_officer": {"password": "VizagDSU99!", "role": "District Officer"},
    "chc_doctor": {"password": "MedicalDoc123", "role": "CHC Medical Practitioner"},
    "asha_worker": {"password": "VillageASHA456", "role": "ASHA Community Worker"}
}

def log_transaction(user_role, node_id, action_type, details):
    conn = sqlite3.connect("smart_health.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO system_audit_logs (user_role, node_id, action_type, details)
        VALUES (?, ?, ?, ?);
    """, (user_role, node_id, action_type, details))
    conn.commit()
    conn.close()
