-- Hierarchical Location Nodes Mapping Grid
CREATE TABLE IF NOT EXISTS administrative_hierarchy (
    node_id TEXT PRIMARY KEY,
    node_level TEXT,
    node_name TEXT,
    state_name TEXT,
    district_name TEXT,
    latitude REAL,
    longitude REAL
);

-- Doctor Shift Duty Rosters
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id TEXT PRIMARY KEY,
    node_id TEXT,
    doctor_name TEXT,
    specialization TEXT,
    active_status INT,
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- Active ASHA Workers Mapping
CREATE TABLE IF NOT EXISTS asha_workers (
    asha_id TEXT PRIMARY KEY,
    node_id TEXT,
    username TEXT,
    worker_name TEXT,
    assigned_village TEXT,
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- Local Pharmacist Personnel Mapping
CREATE TABLE IF NOT EXISTS pharmacists (
    pharma_id TEXT PRIMARY KEY,
    node_id TEXT,
    username TEXT,
    employee_name TEXT,
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- Dynamic Inventory Matrix
CREATE TABLE IF NOT EXISTS inventory (
    node_id TEXT,
    item_name TEXT,
    current_stock INT,
    min_required_threshold INT,
    daily_avg_consumption REAL,
    PRIMARY KEY (node_id, item_name),
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- Central Triage Queue
CREATE TABLE IF NOT EXISTS patient_triage_queue (
    token_id TEXT PRIMARY KEY,
    node_id TEXT,
    aadhaar_hash TEXT,
    patient_phone TEXT,
    symptoms_logged TEXT,
    status TEXT,
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- Operational Load Logs
CREATE TABLE IF NOT EXISTS node_operations (
    node_id TEXT PRIMARY KEY,
    total_beds INT,
    occupied_beds INT,
    active_epidemic_risk_score REAL,
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- Protected System Ledger
CREATE TABLE IF NOT EXISTS system_audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_role TEXT,
    node_id TEXT,
    action_type TEXT,
    details TEXT
);
-- Unified Digital Prescription Order Tracking Matrix
CREATE TABLE IF NOT EXISTS e_prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    token_id TEXT,
    node_id TEXT,
    doctor_name TEXT,
    medicine_name TEXT,
    dosage_instructions TEXT,
    status TEXT DEFAULT 'PENDING', -- 'PENDING', 'DISPENSED'
    FOREIGN KEY (token_id) REFERENCES patient_triage_queue(token_id)
);
