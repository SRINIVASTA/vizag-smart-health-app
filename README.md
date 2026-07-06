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

## 🔑 Multi-District Secure Authentication Matrix

The platform implements a **Geospatial Role-Based Access Control (RBAC)** architecture. Select your target **District** and **Facility Node** in the sidebar navigation matrix, then pick the corresponding authorized profile name from the **Username** selectbox dropdown list to test specific localized care workflows:

### 🌐 Global / Cross-District Administrative Clearances

| District Selector | Username Selection Option | Required Password | Authorized View & Clearance Level |
| :--- | :--- | :--- | :--- |
| **Any District** | `State Surveillance Admin` | `AmaravatiHealth2026!` | State Surveillance (Matplotlib Regional Anomaly Distribution Charts & Global Audit Ledger) |
| **Any District** | `District Officer` | `VizagDSU99!` | District Officer (UAV Drone Resource Re-balancing Maps & Real-time Expiry Forecasts) |

---

### 📍 District 1: Visakhapatnam (Edge Nodes Workspace)

| Targeted Facility Dropdown | Username Selection Option | Required Password | Functional Mode Matrix Capability |
| :--- | :--- | :--- | :--- |
| **Pendurthi CHC Hub** | `Dr. S. Srinivasa Rao` | `MedicalDoc123` | **Local Mode**: Bed Occupancy. **Video Mode**: e-Sanjeevani API Engine & Rx |
| **Pendurthi CHC Hub` | `Smt. T. Appalanamma` | `VillageASHA456` | **Local Mode**: Vitals Screening & Logging. **Video Mode**: Tele-Triage Ingestion |
| **Pendurthi CHC Hub** | `Sri K. Jagannadham` | `PharmaStore456` | **Local Mode**: Over-The-Counter Dispensing. **Video Mode**: Autonomous Drone Resupply |

---

### 📍 District 2: Vizianagaram (Edge Nodes Workspace)

| Targeted Facility Dropdown | Username Selection Option | Required Password | Functional Mode Matrix Capability |
| :--- | :--- | :--- | :--- |
| **Gajapathinagaram PHC** | `Dr. Ch. Koteswara Rao` | `MedicalDoc123` | **Local Mode**: Bed Occupancy. **Video Mode**: e-Sanjeevani API Engine & Rx |
| **Gajapathinagaram PHC** | `Smt. D. Parvathi` | `VillageASHA456` | **Local Mode**: Vitals Screening & Logging. **Video Mode**: Tele-Triage Ingestion |
| **Gajapathinagaram PHC** | `Sri R. K. Prasad` | `PharmaStore456` | **Local Mode**: Over-The-Counter Dispensing. **Video Mode**: Autonomous Drone Resupply |

---

### 📍 District 3: Srikakulam (Edge Nodes Workspace)

| Targeted Facility Dropdown | Username Selection Option | Required Password | Functional Mode Matrix Capability |
| :--- | :--- | :--- | :--- |
| **Srikakulam Rural Center** | `Dr. K. Venkataswamy` | `MedicalDoc123` | **Local Mode**: Bed Occupancy. **Video Mode**: e-Sanjeevani API Engine & Rx |
| **Srikakulam Rural Center** | `Smt. K. Chittemma` | `VillageASHA456` | **Local Mode**: Vitals Screening & Logging. **Video Mode**: Tele-Triage Ingestion |
| **Srikakulam Rural Center** | `Sri B. Krishna` | `PharmaStore456` | **Local Mode**: Over-The-Counter Dispensing. **Video Mode**: Autonomous Drone Resupply |

---

## 🧪 Comprehensive Closed-Loop Prescription Evaluation Walkthrough

Follow this exact sequence to demonstrate the entire cross-role integration of the platform to the evaluation panel:

### Step 1: Decentralized Intake & Mode Choice (ASHA Worker)
1. Set the location router context to **Srikakulam** ➡️ **Srikakulam Rural Health Center**.
2. Select **Smt. K. Chittemma** from the username selector dropdown and input password: `VillageASHA456`.
3. In the intake dashboard, toggle the operational mode from *In-Person Local Screening* to *Remote Tele-Triage Ingestion*. Notice how the data capture canvas shifts parameters dynamically.
4. Input a valid 12-digit Aadhaar, enter a target patient phone number, assign the case to `Dr. K. Venkataswamy`, and click submit.

### Step 2: Virtual Consultation & Prescription Generation (Doctor Room)
1. Log out of the ASHA environment and authenticate into the same health center under **Dr. K. Venkataswamy** using password: `MedicalDoc123`.
2. Toggle the consultant duty mode to *e-Sanjeevani Video Call Telehealth*.
3. Review the patient triage queue populated in Step 1. Click the ** Launch Instant Video Consultation Channel** button to fire the dynamic browser link forwarding hook.
4. Scroll down to the *Formulate Digital Medical Prescription* section. Select your target medicine, type your custom dosage instructions, and click ** Issue Prescription to Pharmacy**.

### Step 3: Aero-Logistics Fulfillment (Pharmacist Counter)
1. Log out and log back into the same facility hub under **Sri B. Krishna** using password: `PharmaStore456`.
2. Toggle your inventory distribution mode selection interface to *Drone-Routed Aero Resupply Operations*.
3. Notice how the inbound prescription ledger populates with the precise order issued by the doctor in Step 2.
4. Click ** Authorize Autonomous Drone Resupply Delivery**. The app immediately decrements the local stock ledger, updates the patient prescription status field to `DRONE_DISPATCHED`, and launches an autonomous UAV route optimization path.
