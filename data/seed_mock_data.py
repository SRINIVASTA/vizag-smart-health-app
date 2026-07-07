# seed_mock_data.py
import sqlite3
import os

def execute_seeding_pipeline():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/smart_health.db")
    cursor = conn.cursor()

    with open("data/schema.sql", "r", encoding="utf-8") as schema_file:
        cursor.executescript(schema_file.read())

    # Purge existing data to avoid conflict errors
    cursor.execute("DELETE FROM system_audit_logs;")
    cursor.execute("DELETE FROM patient_prescriptions;")
    cursor.execute("DELETE FROM patient_triage_queue;")
    cursor.execute("DELETE FROM node_operations;")
    cursor.execute("DELETE FROM inventory;")
    cursor.execute("DELETE FROM pharmacists;")
    cursor.execute("DELETE FROM asha_workers;")
    cursor.execute("DELETE FROM doctors;")
    cursor.execute("DELETE FROM administrative_hierarchy;")

    # 1. Spatial Clinic Coordinates
    facilities = [
        ('IN-AP-VSP-PND', 'Tehsil', 'Pendurthi CHC Hub', 'Andhra Pradesh', 'Visakhapatnam', 17.8303, 83.1979),
        ('IN-AP-VSP-BHM', 'Tehsil', 'Bheemili Hospital Spoke', 'Andhra Pradesh', 'Visakhapatnam', 17.8894, 83.4452),
        ('IN-AP-VZM-GJN', 'Tehsil', 'Gajapathinagaram PHC', 'Andhra Pradesh', 'Vizianagaram', 18.2789, 83.3323),
        ('IN-AP-SKL-RUR', 'Tehsil', 'Srikakulam Rural Center', 'Andhra Pradesh', 'Srikakulam', 18.3164, 83.8943),
        ('IN-AP-SKL-PLS', 'Tehsil', 'Palasa Super-Spec Spoke', 'Andhra Pradesh', 'Srikakulam', 18.7725, 84.4172)
    ]
    cursor.executemany("INSERT INTO administrative_hierarchy VALUES (?, ?, ?, ?, ?, ?, ?)", facilities)

    # 2. Medical Staff Logs
    doctors = [
        ('DOC-VSP-001', 'IN-AP-VSP-PND', 'Dr. S. Srinivasa Rao', 'General Medicine', 1),
        ('DOC-VSP-002', 'IN-AP-VSP-PND', 'Dr. K. Anuradha', 'Pediatrics', 1),
        ('DOC-VSP-003', 'IN-AP-VSP-BHM', 'Dr. A. Lakshmi Prasanna', 'General Medicine', 0), 
        ('DOC-VZM-001', 'IN-AP-VZM-GJN', 'Dr. Ch. Koteswara Rao', 'General Medicine', 1),
        ('DOC-SKL-001', 'IN-AP-SKL-RUR', 'Dr. K. Venkataswamy', 'General Medicine', 1)
    ]
    cursor.executemany("INSERT INTO doctors VALUES (?, ?, ?, ?, ?)", doctors)

    # 3. Grassroots Registries
    ashas = [
        ('ASHA-VSP-001', 'IN-AP-VSP-PND', 'asha_worker', 'Smt. Lakshmi', 'Pendurthi Village A'),
        ('ASHA-VZM-001', 'IN-AP-VZM-GJN', 'asha_gajapathinagaram', 'Smt. Saraswathi', 'Gajapathinagaram West'),
        ('ASHA-SKL-001', 'IN-AP-SKL-RUR', 'asha_srikakulam', 'Smt. Parvathi', 'Srikakulam Outer Ring')
    ]
    cursor.executemany("INSERT INTO asha_workers VALUES (?, ?, ?, ?, ?)", ashas)

    # 4. Pharma Managers
    pharmacists = [
        ('PHR-VSP-001', 'IN-AP-VSP-PND', 'pharma_person', 'Sri K. Venkatesh'),
        ('PHR-VZM-001', 'IN-AP-VZM-GJN', 'pharma_gajapathinagaram', 'Sri L. Narayana'),
        ('PHR-SKL-001', 'IN-AP-SKL-RUR', 'pharma_srikakulam_rur', 'Sri P. Satyam')
    ]
    cursor.executemany("INSERT INTO pharmacists VALUES (?, ?, ?, ?)", pharmacists)

    # 5. Inventory Matrix (Shortages vs Surpluses)
    inventory_data = [
        ('IN-AP-VSP-PND', 'Paracetamol Tabs', 450, 5000, 450.0),    
        ('IN-AP-VSP-BHM', 'Paracetamol Tabs', 18000, 4000, 180.0),  
        ('IN-AP-VZM-GJN', 'Paracetamol Tabs', 5500, 3000, 210.0),
        ('IN-AP-SKL-RUR', 'Anti-Venom Vials', 3, 40, 6.5),          
        ('IN-AP-SKL-PLS', 'Anti-Venom Vials', 150, 30, 2.0)         
    ]
    cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", inventory_data)

    # 6. Patient Queues
    triage_data = [
        ('AP-1422', 'IN-AP-VSP-PND', 'sha256_hash_xyz1', '9848022338', 'High Fever, Vomiting, Body Pains', 'WAITING'),
        ('AP-1423', 'IN-AP-SKL-RUR', 'sha256_hash_xyz2', '9440123456', 'Acute Snake Bite on Foot', 'WAITING')
    ]
    cursor.executemany("INSERT INTO patient_triage_queue VALUES (?, ?, ?, ?, ?, ?)", triage_data)

    # 7. Bed Counts & Epidemic Multiplication Ratios
    node_ops = [
        ('IN-AP-VSP-PND', 50, 44, 0.88),  
        ('IN-AP-VSP-BHM', 30, 10, 0.12),
        ('IN-AP-VZM-GJN', 20, 12, 0.38),
        ('IN-AP-SKL-RUR', 25, 22, 0.79),  
        ('IN-AP-SKL-PLS', 40, 15, 0.21)
    ]
    cursor.executemany("INSERT INTO node_operations VALUES (?, ?, ?, ?)", node_ops)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    execute_seeding_pipeline()
    print("🎉 System Database Instantiated!")
