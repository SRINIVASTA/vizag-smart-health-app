-- ====================================================================
-- BHARAT HEALTH AI: PRODUCTION PILOT SCHEMA BLUEPRINT (ANDHRA PRADESH)
-- ====================================================================

-- 1. Hierarchical District & Facility Location Nodes Matrix
CREATE TABLE IF NOT EXISTS administrative_hierarchy (
    node_id TEXT PRIMARY KEY,       -- E.g., 'IN-AP-VSP-PND'
    node_level TEXT NOT NULL,       -- 'Tehsil', 'District', 'State'
    node_name TEXT NOT NULL,        -- E.g., 'Pendurthi CHC Hub'
    state_name TEXT NOT NULL,       -- 'Andhra Pradesh'
    district_name TEXT NOT NULL,    -- E.g., 'Visakhapatnam'
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

-- 2. Doctor Shift Duty Rosters
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id TEXT PRIMARY KEY,
    node_id TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    active_status INT NOT NULL DEFAULT 1,
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- 3. ASHA Community Ground-Level Worker Directory
CREATE TABLE IF NOT EXISTS asha_workers (
    asha_id TEXT PRIMARY KEY,
    node_id TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,  -- E.g., 'asha_worker'
    worker_name TEXT NOT NULL,
    assigned_village TEXT NOT NULL,
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- 4. Local Pharmacy Store Managers Directory
CREATE TABLE IF NOT EXISTS pharmacists (
    pharma_id TEXT PRIMARY KEY,
    node_id TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,  -- E.g., 'pharma_person'
    employee_name TEXT NOT NULL,
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- 5. Real-Time Dynamic Inventory Matrix
CREATE TABLE IF NOT EXISTS inventory (
    node_id TEXT NOT NULL,
    item_name TEXT NOT NULL,
    current_stock INT NOT NULL DEFAULT 0,
    min_required_threshold INT NOT NULL DEFAULT 10,
    daily_avg_consumption REAL NOT NULL DEFAULT 1.0,
    PRIMARY KEY (node_id, item_name),
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- 6. Unified Patient Flow Triage Queue 
CREATE TABLE IF NOT EXISTS patient_triage_queue (
    token_id TEXT PRIMARY KEY,      -- E.g., 'AP-1422'
    node_id TEXT NOT NULL,
    aadhaar_hash TEXT NOT NULL,
    patient_phone TEXT NOT NULL,
    symptoms_logged TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'WAITING', -- 'WAITING', 'COMPLETED'
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- 7. 🎯 NEW: CLOSED-LOOP PATIENT PRESCRIPTION ROUTING LEDGER
CREATE TABLE IF NOT EXISTS patient_prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id TEXT NOT NULL,         -- Links back to the patient record
    node_id TEXT NOT NULL,          -- Facility indicator
    doctor_name TEXT NOT NULL,
    medication_name TEXT NOT NULL,
    dosage_instructions TEXT NOT NULL,
    consult_mode TEXT NOT NULL,    -- 'Physical Local OPD Desk' or 'e-Sanjeevani Video Call Telehealth'
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'PENDING', -- 'PENDING' or 'FULFILLED'
    FOREIGN KEY (token_id) REFERENCES patient_triage_queue(token_id),
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- 8. Cross-Tier Bed Infrastructure & Epidemic Anomaly Tracker Metrics
CREATE TABLE IF NOT EXISTS node_operations (
    node_id TEXT PRIMARY KEY,
    total_beds INT NOT NULL DEFAULT 0,
    occupied_beds INT NOT NULL DEFAULT 0,
    active_epidemic_risk_score REAL NOT NULL DEFAULT 0.0,
    FOREIGN KEY (node_id) REFERENCES administrative_hierarchy(node_id)
);

-- 9. Immutable Background Compliance Audit Log Trail
CREATE TABLE IF NOT EXISTS system_audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_role TEXT NOT NULL,
    node_id TEXT NOT NULL,
    action_type TEXT NOT NULL,     -- 'LOGIN', 'PATIENT_INTAKE', 'PRESCRIPTION_ISSUE', 'MEDICINE_DISPENSE'
    details TEXT NOT NULL
);
