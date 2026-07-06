import sqlite3

# Plain text tracking roles mapping for unified test authorization footprints
USER_REGISTRY = {
    "ap_state_admin": {"password": "AmaravatiHealth2026!", "role": "State Surveillance"},
    "district_officer": {"password": "VizagDSU99!", "role": "District Officer"},
    "asha_worker": {"password": "VillageASHA456", "role": "ASHA Community Worker"},
    "chc_doctor": {"password": "MedicalDoc123", "role": "CHC Medical Practitioner"},
    "pharma_person": {"password": "PharmaStore456", "role": "Pharmacist"}
}

def log_transaction(user_role, node_id, action_type, details):
    """Secure background system footprint logger. Visible exclusively to Admins."""
    conn = sqlite3.connect("smart_health.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO system_audit_logs (user_role, node_id, action_type, details)
        VALUES (?, ?, ?, ?);
    """, (user_role, node_id, action_type, details))
    conn.commit()
    conn.close()
