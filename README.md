# 🏥 Visakhapatnam Smart Health Enterprise Hub
### 🚀 Secure, Biometric Ingestion Gateway & Closed-Loop Pharmacy Verification Platform
**Author / Maintained by:** Srinivasa  
**Operational Framework Era:** 2026 Emergency Management Standards  
**Target Sector:** Primary Health Centers (PHCs) & Community Health Centers (CHCs), Visakhapatnam District, Andhra Pradesh, India

---

## 📋 Project Overview
The **Visakhapatnam Smart Health Enterprise Hub** is an offline-first, high-resiliency digital infrastructure solution designed for remote and tribal medical clinics (such as Araku Valley, Paderu, and Anakapalle). It replaces outdated manual paper logs with a zero-fraud, automated patient lifecycle environment powered by the **Three-Way Aadhaar Biometric Handshake**.

The platform optimizes resource gates, restricts pharmacy lists based on clinical roles, dynamically issues prefix-routed tokens, manages in-patient bed matrices, and ensures global diagnostic compliance using the HL7/FHIR health data exchange protocol.

---

## ✨ System Features & Operational Modalities

### 1. 🛰️ Autonomous Aadhaar Ingestion Kiosk (Touchpoint 1)
* **Zero-Input Registration:** Patients scan their Aadhaar card or place their thumb on a biometric sensor at the entry gate. The system auto-decrypts official UIDAI demographic records to extract names and securely hash identities via SHA-256.
* **Prefix-Routed Token Engine:** Patients explicitly select their intended attending physician. The gateway automatically generates structured token IDs based on the doctor's designation prefix (e.g., `GEN-001` for General Medicine, `MAT-001` for Maternal Specialist Care).

### 2. 👨‍⚕️ Targeted Consultation Room & Restricted Pharmacy Selection (Touchpoint 2)
* **Isolated Doctor Workspaces:** Doctors log into their distinct desk consoles and view only the oldest waiting patient explicitly routed to their personal queue.
* **Role-Based Prescription Lists:** The platform reads doctor designation tags to restrict selection matrices. Dr. Ramesh Babu (`GEN`) can prescribe Paracetamol, Anti-Venom, or Artesunate, while Dr. S. Lakshmi (`MAT`) is authorized for Iron-Folic Acid and Oxytocin.
* **Clinical Disposition Framework:** Doctors can switch a patient's care status between **Out-Patient** and **In-Patient**. Marking a patient for admission automatically increments the local ward occupancy matrix in real time.

### 3. 💊 Direct-Pull Unit-Dose Pharmacy Counter (Touchpoint 3)
* **Single-Click Handouts:** Since the patient's identity is verified at the entrance kiosk, redundant re-scanning at the pharmacy is avoided. The pharmacist simply pulls up the active token ID to see a dynamic checkout checklist of itemized pill count mandates.
* **Staff Accountability:** Every distribution is firmly mapped to the logged-in pharmacist's approved staff registry profile (`pharma_roster`) to prevent pharmaceutical leakage.

### 4. 📁 Secure Operational Telemetry Log Archive
* **Granular Audit Logs:** Every completed care lifecycle writes a comprehensive permanent transaction history capturing the Date, Token ID, Patient Name, Aadhaar Hash, Chief Complaint Reason, Detailed Medicine Handout Breakdown, Total Pill Count Distributed, Doctor Name, Pharmacist Name, and Care Type.
* **On-Demand Exporter:** Administrators can review a live grid view preview and instantly download the entire historical dataset as a structured `.csv` spreadsheet file with a single click.

### 5. 🛡️ Interoperability & Cryptographic Shielding
* **HL7/FHIR Compliance:** Post-dispense data is formatted into globally accepted national healthcare standard **FHIR Encounter JSON schemas**.
* **AES-XOR Cryptographic Backhaul:** Sensitive electronic summaries are masked into highly compact Base64-encoded strings, enabling secure network synchronization even over unstable public 2G/3G mobile networks in high-altitude tribal pockets.

---

## 🛠️ Repository Architecture & Dependencies

To host this application cleanly on **GitHub Community Cloud** and deploy it to the web via **Streamlit Cloud**, structure your repository as follows:

```text
vizag-smart-health-app/
├── app.py                 # Core 3-Block Monolithic Streamlit Engine
├── requirements.txt       # Cloud server installation configurations
└── .gitignore             # Local storage dump prevention rules
```

### 📋 `requirements.txt`
```text
matplotlib
requests
```
*(Note: `sqlite3`, `json`, `base64`, `re`, `hashlib`, and `csv` are built directly into standard Python libraries and do not require external decoration).*

### 📋 `.gitignore`
```text
*.db
*.csv
__pycache__/
```

---

## 💾 Core Relational Database Schemas

The local relational storage engine (`web_smart_health.db`) structures tracking parameters across 5 interconnected core datasets:

### 1. `patient_queue`

| Column Name | Data Type | Key Type | Operational Definition |
| :--- | :--- | :--- | :--- |
| `token_id` | `TEXT` | `PRIMARY KEY` | Encoded routed identifier (e.g., `GEN-001`, `MAT-001`) |
| `category` | `TEXT` | - | Service classification matching the doctor prefix tag |
| `status` | `TEXT` | - | Patient state parameters (`WAITING`, `IN_PHARMACY`, `DISCHARGED`) |
| `arrival_time` | `TIMESTAMP`| - | Date-time stamp recorded at the gate kiosk |
| `patient_name` | `TEXT` | - | Decrypted legal name pulled from Aadhaar cache |
| `target_doctor` | `TEXT` | - | Attending medical officer assigned at check-in |
| `chief_complaint` | `TEXT` | - | Clinical presentación log entry context |
| `target_disposition`| `TEXT` | - | Default care status option (`Out-Patient`, `In-Patient`) |

### 2. `prescriptions`

| Column Name | Data Type | Key Type | Operational Definition |
| :--- | :--- | :--- | :--- |
| `prescription_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Relational reference sequence index number |
| `token_id` | `TEXT` | - | Patient file cross-reference variable anchor |
| `prescribed_meds` | `TEXT` | - | Flat string index list of selected items |
| `unit_dosages_prescribed` | `TEXT` | - | Serialized JSON string of precise pill count requirements |
| `doctor_name` | `TEXT` | - | Digital signature of the prescribing clinician |
| `dispense_status` | `TEXT` | - | Warehouse transaction flag (`PENDING`, `DISPENSED`) |

### 3. `facility_telemetry_logs`

| Column Name | Data Type | Key Type | Operational Definition |
| :--- | :--- | :--- | :--- |
| `log_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Audit sequence tracking index |
| `log_date` | `TEXT` | - | Calendar date block wrapper format (`YYYY-MM-DD`) |
| `patient_name` | `TEXT` | - | Fully traceable legal name verification entry |
| `detailed_medicines_issued` | `TEXT` | - | Granular unit dosage depletion summary string |
| `total_pills_dispensed_count`| `INTEGER` | - | Cumulative volume sum of individual pills handed out |
| `patient_disposition` | `TEXT` | - | Locked-in data trace tracking Care Type status |

---

## 🚀 Local Installation & Execution Guide

### Prerequisite Environment
Ensure you have Python 3.10+ installed on your local hardware terminal.

### 1. Clone the Public Workspace
```bash
git clone https://github.com
cd vizag-smart-health-app
```

### 2. Install External Extensions
```bash
pip install -r requirements.txt
```

### 3. Launch the Local Development Server Engine
```bash
streamlit run app.py
```

---

## 🌐 Production Web Deployment Steps
1. Push all modified codebase changes directly to your public GitHub branch repository.
2. Visit [share.streamlit.io](https://streamlit.io) and establish a handshake connection with your active GitHub profile.
3. Click **Deploy App**, enter your specific repository path parameters (`YOUR_USERNAME/vizag-smart-health-app`), select the entry script target point (`app.py`), and hit **Deploy**!
4. The system will launch on a live public link (e.g., `https://streamlit.app`) in under 60 seconds with **Self-Healing Schema Migrators** fully functional.

---
### 🤝 System Architecture Audit Acknowledgments
Designed for the **Andhra Pradesh Public Health Grid System**. Fully optimized, validated, and verified for free hosting deployment. For integration scaling or backend extensions, contact **Srinivasa**.
