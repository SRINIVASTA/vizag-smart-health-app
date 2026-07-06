import sqlite3

# Expanded Global Role Registry Mapping covering all Pilot Districts & Personnel
USER_REGISTRY = {
    # 🏢 Global Administrative Overlay Credentials
    "ap_state_admin": {"password": "AmaravatiHealth2026!", "role": "State Surveillance"},
    "district_officer": {"password": "VizagDSU99!", "role": "District Officer"},
    
    # 📍 Visakhapatnam District Specific Accounts
    "Dr. S. Srinivasa Rao": {"password": "MedicalDoc123", "role": "CHC Medical Practitioner"},
    "Dr. K. Anuradha": {"password": "MedicalDoc123", "role": "CHC Medical Practitioner"},
    "Dr. A. Lakshmi Prasanna": {"password": "MedicalDoc123", "role": "CHC Medical Practitioner"},
    "Dr. P. Venkatesh": {"password": "MedicalDoc123", "role": "CHC Medical Practitioner"},
    "Dr. G. Satyanarayana": {"password": "MedicalDoc123", "role": "CHC Medical Practitioner"},
    "pharma_person": {"password": "PharmaStore456", "role": "Pharmacist"},
    "asha_worker": {"password": "VillageASHA456", "role": "ASHA Community Worker"},
    
    # 📍 Vizianagaram District Specific Accounts
    "Dr. Ch. Koteswara Rao": {"password": "MedicalDoc123", "role": "CHC Medical Practitioner"},
    "Dr. M. Sridevi": {"password": "MedicalDoc123", "role": "CHC Medical Practitioner"},
    "Dr. J. Ramana": {"password": "MedicalDoc123", "role": "CHC Medical Practitioner"},
    "pharma_gajapathinagaram": {"password": "PharmaStore456", "role": "Pharmacist"},
    "asha_gajapathinagaram": {"password": "VillageASHA456", "role": "ASHA Community Worker"},
    
    # 📍 Srikakulam District Specific Accounts
    "Dr. K. Venkataswamy": {"password": "MedicalDoc123", "role": "CHC Medical Practitioner"},
    "Dr. Y. Appala Naidu": {"password": "MedicalDoc123", "role": "CHC Medical Practitioner"},
    "pharma_srikakulam_rur": {"password": "PharmaStore456", "role": "Pharmacist"},
    "asha_srikakulam": {"password": "VillageASHA456", "role": "ASHA Community Worker"}
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
