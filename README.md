# Vizag Smart Health Application (Andhra Pradesh Pilot Project)

An integrated, multi-tiered digital healthcare ecosystem tailored for the Visakhapatnam region. This application maps directly onto the Indian administrative hierarchy (State ➔ Division ➔ District ➔ Mandal ➔ Panchayat ➔ Village) to power guided telemedicine, real-time epidemic tracking, and autonomous drone logistics for hard-to-reach tribal tracts like Araku and Paderu.

---

## 🏗️ Repository Architecture

```text
vizag-smart-health-app/
│
├── .streamlit/
│   └── config.toml          # Custom theme configuration variables (AP Government UI/UX Branding)
│
├── data/
│   ├── schema.sql           # Database creation commands (Seeded for AP Pilot & ABHA IDs)
│   └── smart_health.db      # Local SQLite3 database instance for edge computing deployments
│
├── src/
│   ├── __init__.py          # Designates folder as importable package
│   ├── auth.py              # Role-Based Access Control (RBAC) logs for DMs, CHOs, and ASHA workers
│   ├── drone_logistics.py   # Coordinate generator for BVLOS payload flight paths to Agency areas
│   ├── language_pack.py     # Localized string matrix (English, Hindi, Telugu / తెలుగు)
│   ├── predictive_engine.py # Resource balancing and automated IHIP outbreak mapping algorithms
│   └── telehealth.py        # WhatsApp Business API e-Sanjeevani link builder tools
│
├── app.py                   # System core orchestrator loop & Streamlit layout dashboard
├── README.md                # Technical operational setup documentation (This file)
└── requirements.txt         # Production library dependency manifest
```

---

## ⚡ Core Functional Modules

### 1. Multi-Tier Governance & RBAC (`src/auth.py`)
Maps application views and dashboard permissions dynamically based on the administrative layer of the logged-in user:
*   **National/State Health Authority**: Macro analytics on disease outbreak tracking across Andhra Pradesh.
*   **District Collector / Chief Medical Officer (Vizag)**: Resource allocation, hospital bed forecasting, and emergency declarations.
*   **Mandal / Community Health Officer (CHO)**: Managing village e-Sanjeevani waiting rooms and digital drug inventory.
*   **ASHA Worker / Ground Surveyor**: Simplified mobile-first forms to upload localized syndromic health data.

### 2. Guided Telemedicine (`src/telehealth.py`)
Implements the e-Sanjeevani hub-and-spoke logic. It pairs high-risk patients at rural Gram Panchayats with specialists at **King George Hospital (KGH), Visakhapatnam**. It auto-generates localized, encrypted **WhatsApp consultation links** complete with pre-compiled patient vital attachments.

### 3. Epidemic Engine (`src/predictive_engine.py`)
An automated local adaptation of India’s **Integrated Health Information Platform (IHIP)**. The engine constantly evaluates syndromic reporting input from the field. It flags spatial anomaly clusters (e.g., an unusual spike in fever/waterborne illness cases within a specific Mandal) to trigger early warning notices.

### 4. Drone Delivery Logistics (`src/drone_logistics.py`)
Generates autonomous Beyond Visual Line of Sight (BVLOS) flight paths mapping from urban medical distribution hubs directly to inaccessible terrains in the **Vizag Agency areas (Ananthagiri, Paderu, Araku)** for time-critical drops of anti-venom, vaccines, and emergency drug supplies.

### 5. Multi-Language Support (`src/language_pack.py`)
Provides seamless UI toggles between **English, Hindi, and Telugu (తెలుగు)** to make it fully accessible to field staff and local health workers on the ground.

---

## 🛠️ Installation & Setup

### Prerequisites
*   Python 3.10 or higher
*   SQLite3

### 1. Clone and Navigate to the Repository
```bash
git clone https://github.com
cd vizag-smart-health-app
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Production Dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed the Database
Initialize your local database using the seed schema mapped for the Visakhapatnam administrative zones:
```bash
sqlite3 data/smart_health.db < data/schema.sql
```

### 5. Execute the Core Orchestrator
Launch the main application interface locally using Streamlit:
```bash
streamlit run app.py
```

---

# Bharat Health AI: Decentralized Multi-District Care & Aero-Logistics Network

An enterprise-grade, offline-first health management platform designed for public health infrastructure. This application operates on a specialized **Cascading Location Matrix and State Audit Model**, bridging the gap between frontline village healthcare, district-level coordinators, and state surveillance administrators across Andhra Pradesh.

---

## 🔑 Complete Operational Credentials Matrix

To evaluate different organizational tiers within the platform, select your target **District** and **Facility Node** in the sidebar navigation matrix, then pick the corresponding authorized profile name from the **Username** selectbox dropdown list:

### 🏢 Cross-District Administrative Clearances

| District Selector Context | Username Selection Option | Required Password | Authorized View & clearance Level |
| :--- | :--- | :--- | :--- |
| **Any District** | `ap_state_admin` | `AmaravatiHealth2026!` | State Surveillance (Unrestricted monitoring access to all 3 districts concurrently) |
| **Visakhapatnam** | `vsp_district_officer` | `VizagDSU99!` | District Officer (Isolated analytics scope locked to Visakhapatnam) |
| **Vizianagaram** | `vzm_district_officer` | `VizagDSU99!` | District Officer (Isolated analytics scope locked to Vizianagaram) |
| **Srikakulam** | `skl_district_officer` | `VizagDSU99!` | District Officer (Isolated analytics scope locked to Srikakulam) |

### 📍 District 1: Visakhapatnam Node Accounts

| Targeted Facility Dropdown | Username Selection Option | Required Password | Authorized Frontline Role View |
| :--- | :--- | :--- | :--- |
| **Pendurthi CHC Hub** | `Dr. S. Srinivasa Rao` | `MedicalDoc123` | CHC Medical Practitioner (Clinical Queue Portal) |
| **Pendurthi CHC Hub** | `Dr. K. Anuradha` | `MedicalDoc123` | CHC Medical Practitioner (Clinical Queue Portal) |
| **Pendurthi CHC Hub** | `asha_worker` | `VillageASHA456` | ASHA Community Worker (Patient Intake Logger) |
| **Pendurthi CHC Hub** | `pharma_person` | `PharmaStore456` | Pharmacist Store Manager (Fulfillment Desk) |
| **Bheemili Hospital Spoke** | `Dr. A. Lakshmi Prasanna` | `MedicalDoc123` | CHC Medical Practitioner (Clinical Queue Portal) |
| **Gajuwaka Industrial PHC** | `Dr. P. Venkatesh` | `MedicalDoc123` | CHC Medical Practitioner (Clinical Queue Portal) |
| **Anakapalle Referral CHC** | `Dr. G. Satyanarayana` | `MedicalDoc123` | CHC Medical Practitioner (Clinical Queue Portal) |

### 📍 District 2: Vizianagaram Node Accounts

| Targeted Facility Dropdown | Username Selection Option | Required Password | Authorized Frontline Role View |
| :--- | :--- | :--- | :--- |
| **Gajapathinagaram PHC** | `Dr. Ch. Koteswara Rao` | `MedicalDoc123` | CHC Medical Practitioner (Clinical Queue Portal) |
| **Gajapathinagaram PHC** | `asha_gajapathinagaram` | `VillageASHA456` | ASHA Community Worker (Patient Intake Logger) |
| **Gajapathinagaram PHC** | `pharma_gajapathinagaram`| `PharmaStore456` | Pharmacist Store Manager (Fulfillment Desk) |
| **Cheepurupalli Spoke CHC**| `Dr. M. Sridevi` | `MedicalDoc123` | CHC Medical Practitioner (Clinical Queue Portal) |
| **Sravankota Rural PHC** | `Dr. J. Ramana` | `MedicalDoc123` | CHC Medical Practitioner (Clinical Queue Portal) |

### 📍 District 3: Srikakulam Node Accounts

| Targeted Facility Dropdown | Username Selection Option | Required Password | Authorized Frontline Role View |
| :--- | :--- | :--- | :--- |
| **Srikakulam Rural Center**| `Dr. K. Venkataswamy` | `MedicalDoc123` | CHC Medical Practitioner (Clinical Queue Portal) |
| **Srikakulam Rural Center**| `asha_srikakulam` | `VillageASHA456` | ASHA Community Worker (Patient Intake Logger) |
| **Srikakulam Rural Center**| `pharma_srikakulam_rur` | `PharmaStore456` | Pharmacist Store Manager (Fulfillment Desk) |
| **Palasa Super-Spec Spoke**| `Dr. Y. Appala Naidu` | `MedicalDoc123` | CHC Medical Practitioner (Clinical Queue Portal) |

---

## 🧪 Comprehensive Cross-tier Validation Walkthrough

Follow these exact operational walkthroughs to demonstrate your end-to-end architecture workflows to the grading panel:

### Walkthrough A: Closed-Loop Digital Prescription Routing
1. Set the sidebar location matrix to **Srikakulam** ➡️ **Srikakulam Rural Health Center**.
2. Select **asha_srikakulam** from the username selector dropdown and input password: `VillageASHA456`.
3. Fill out the *Patient Intake Logger* with test details (e.g., 12-digit Aadhaar), assign the case directly to **Dr. K. Venkataswamy**, and submit.
4. Log out, maintain the location context, and log back in under **Dr. K. Venkataswamy** using password: `MedicalDoc123`.
5. Locate the newly logged triage case. Toggle the consulting mode to *e-Sanjeevani Video Call Telehealth* to review video gates. Move to the *Formulate Digital Medical Prescription* panel, choose a medicine, type dosage instructions, and click **Issue Prescription to Pharmacy**.
6. Log out and log back into the same center as **pharma_srikakulam_rur** (password: `PharmaStore456`). Toggle the active distribution mode to *Drone-Routed Aero Resupply*. You will see the doctor's prescription securely routed to the fulfillment queue. Click **Authorize Autonomous Drone Resupply Delivery** to fire the UAV simulation.

### Walkthrough B: Cross-District Secure Data Protection Block
1. Choose **Dr. S. Srinivasa Rao** from the username dropdown. This practitioner belongs to **Visakhapatnam**.
2. Intentionally change the sidebar location selector to a different territory context: **Srikakulam** ➡️ **Palasa Super-Specialty Spoke**.
3. Input the password: `MedicalDoc123` and click Login.
4. The system immediately detects the district boundary violation, flags a clear warning message block, hides all triage fields and active medical prescription form sheets, and switches into **Read-Only View Mode**, restricting the user solely to looking up the *Historical Patient Electronic Health Records (EHR Ledger)*.

### Walkthrough C: Administrative Jurisdiction Separation
1. Log in under **vzm_district_officer** using password: `VizagDSU99!`. Access the administrative view panels to observe how the **Matplotlib asset charts** and drone logistics telemetry logs isolate data strictly to the **Vizianagaram** district lines.
2. Log out and log in under **ap_state_admin** (password: `AmaravatiHealth2026!`). The layout expands instantly into unrestricted mode, compiling data from **Visakhapatnam, Vizianagaram, and Srikakulam** concurrently onto unified District Infection and Stock Exhaustion timelines.
