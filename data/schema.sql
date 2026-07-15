-- BLOCK 5: DATABASE SCHEMA DEFINITION BLUEPRINT
CREATE TABLE IF NOT EXISTS administrative_hierarchy (
    node_id TEXT PRIMARY KEY,
    layer_type TEXT,
    node_name TEXT,
    state_name TEXT,
    district_name TEXT,
    latitude REAL,
    longitude REAL
);

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id TEXT PRIMARY KEY,
    node_id TEXT,
    doctor_name TEXT,
    specialization TEXT,
    is_active INTEGER,
    FOREIGN KEY(node_id) REFERENCES administrative_hierarchy(node_id)
);

CREATE TABLE IF NOT EXISTS asha_workers (
    asha_id TEXT PRIMARY KEY,
    node_id TEXT,
    username TEXT,
    worker_name TEXT,
    assigned_area TEXT,
    FOREIGN KEY(node_id) REFERENCES administrative_hierarchy(node_id)
);

CREATE TABLE IF NOT EXISTS pharmacists (
    pharmacist_id TEXT PRIMARY KEY,
    node_id TEXT,
    username TEXT,
    pharmacist_name TEXT,
    FOREIGN KEY(node_id) REFERENCES administrative_hierarchy(node_id)
);

CREATE TABLE IF NOT EXISTS inventory (
    node_id TEXT,
    item_name TEXT,
    current_stock INTEGER,
    min_required_threshold INTEGER,
    daily_avg_consumption REAL,
    PRIMARY KEY(node_id, item_name),
    FOREIGN KEY(node_id) REFERENCES administrative_hierarchy(node_id)
);

CREATE TABLE IF NOT EXISTS patient_triage_queue (
    token_id TEXT PRIMARY KEY,
    node_id TEXT,
    patient_hash TEXT,
    contact_phone TEXT,
    symptoms_logged TEXT,
    status TEXT,
    FOREIGN KEY(node_id) REFERENCES administrative_hierarchy(node_id)
);

CREATE TABLE IF NOT EXISTS patient_prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id TEXT,
    node_id TEXT,
    doctor_name TEXT,
    medication_name TEXT,
    dosage_instructions TEXT,
    consult_mode TEXT,
    status TEXT,
    FOREIGN KEY(token_id) REFERENCES patient_triage_queue(token_id),
    FOREIGN KEY(node_id) REFERENCES administrative_hierarchy(node_id)
);

CREATE TABLE IF NOT EXISTS node_operations (
    node_id TEXT PRIMARY KEY,
    total_beds INTEGER,
    occupied_beds INTEGER,
    active_epidemic_risk_score REAL,
    FOREIGN KEY(node_id) REFERENCES administrative_hierarchy(node_id)
);

CREATE TABLE IF NOT EXISTS system_audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_role TEXT,
    action_details TEXT
);
