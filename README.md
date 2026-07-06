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

# BHARAT HEALTH AI: PILOT PHASE SECURE GATEWAY

## Authorized Credentials

| Authorized Username | Password | Clearance Role Authorized |
| :--- | :--- | :--- |
| `ap_state_admin` | `AmaravatiHealth2026!` | State Surveillance |
| `district_officer` | `VizagDSU99!` | District Officer |
| `chc_doctor` | `MedicalDoc123` | CHC Medical Practitioner |
| `asha_worker` | `VillageASHA456` | ASHA Community Worker |

## System Dispatch Summary Note

* **Administrative Accounts (`ap_state_admin` / `district_officer`)**
  * Test and review Matplotlib forecasting trends.
  * Monitor drone routing grids.
  * Access hidden system logs.

* **Frontline Accounts (`chc_doctor` / `asha_worker`)**
  * Access localized frontline point triage engines.
  * Generate active e-Sanjeevani WhatsApp sessions.
