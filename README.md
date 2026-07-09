# Vizag Smart Health Application (Andhra Pradesh Pilot Project)

An integrated, multi-tiered digital healthcare ecosystem tailored for the Visakhapatnam region. This application maps directly onto the Indian administrative hierarchy (State ➔ Division ➔ District ➔ Mandal ➔ Panchayat ➔ Village) to power guided telemedicine, real-time epidemic tracking, and autonomous drone logistics for hard-to-reach tribal tracts like Araku and Paderu.

🌐 **Live Interactive Web App:** [Launch Live Streamlit Dashboard](https://vizag-smart-health-app-hwpexsovxwurku4vqcuwpt.streamlit.app/))
## 🖥️ Project Presentation Pitch Deck

[![Pitch Deck PDF](https://shields.io)](https://github.com/SRINIVASTA/msme-financial-health-passport/blob/main/MSME%20Financial%20Health%20Passport.pdf
)

📌 *Note for Judges: Click the red badge above to open our complete **Project Underwriting Pitch Deck PDF** directly within GitHub's native, interactive document viewer.*

---
# BUILD WITH AI: CODE FOR COMMUNITIES (VIZAG EDITION)
Powered by Google Cloud | Hosted via Hack2skill & GDG Vizag

### 🏛️ Parliamentary Track Patrons
*   Sujeet Kumar (Hon'ble MP, Rajya Sabha) – Governance Innovation Lead
*   Gaurav Gogoi (Hon'ble MP, Lok Sabha) – Public Challenge Ideator
*   Bansuri Swaraj (Hon'ble MP, Lok Sabha) – Civic Progress Systems Advisor
*   Sasmit Patra (Hon'ble MP, Rajya Sabha) – Local Governance Tech Mentor
*   Lavu Sri Krishna Devarayalu (Hon'ble MP, Lok Sabha) – 'Kisan Alert' Challenge Mandate (Narasaraopet)
*   Mathukumilli Bharat (Hon'ble MP, Lok Sabha) – Student Skill Deployment Catalyst

### ⚡ GDG Vizag Core Leadership
*   Usha Ramani Vemuru – Event Leader & Primary Organiser (Founder, GURUJADA)
*   Sai Sampath Kumar Balivada & Satheesh Karnatakapu – Logistics & Co-Organisers
*   Harsh Dattani – Strategic Ecosystem Advisor & Support

### 🧠 AMA Technical Mentors & Experts
*   Saurabh Mishra | Jay Thakkar | Belal Khan (@probelalkhan) | Ajoe Joseph 
*   Namrata More | Chivukula Krishnamohan | Rakesh Asapanna | Darahas Muggu

### 🛠️ Support, Infrastructure & Volunteering
*   Jyothsna Ardhahakula – Event Volunteer
*   Ashwini & Sayyed Emkay – Community Support Enablers (Ientity)

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
# Health System User Management Portal

This repository contains the configuration, deployment scripts, and credential distribution guidelines for the regional health management system. The portal manages role-based access control (RBAC) across regional hubs, spokes, and rural clinics.

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
- [Credentials Reference](#credentials-reference)
- [Security Guidelines](#security-guidelines)
- [Setup & Installation](#setup--installation)

---

## Overview
The platform connects state administrators, district offices, hub/spoke medical facilities, community health workers (ASHA), and pharmacies into a single secure network. It ensures seamless data sharing for patient care, stock distribution, and regional health monitoring.

## System Architecture
The network is split hierarchically into geographical nodes:
- **State Level:** Overarching management across all districts.
- **District Level:** Focused nodes for major administrative areas (Visakhapatnam, Vizianagaram, Srikakulam).
- **Facility Level:** 
  - **Hubs:** Comprehensive health centers managing data flow (e.g., Pendurthi CHC Hub).
  - **Spokes:** Connected clinics reporting to a central hub (e.g., Bheemili Spoke).
  - **Rural Units:** Remote locations delivering localized care (e.g., Gajapathinagaram, Srikakulam Rural).

---

## Role-Based Access Control (RBAC)
The system enforces strict data isolation based on assigned roles:

| System Role | Scope of Access | Key Responsibilities |
| :--- | :--- | :--- |
| **State Administrator** | System-wide (All Districts) | Global configurations, master backups, broad reporting. |
| **District Officer** | District-wide (Local Nodes) | Local facility approvals, district health audits. |
| **Medical Doctor** | Hub/Spoke Specific | Patient diagnostics, electronic health records (EHR), referrals. |
| **ASHA Worker** | Area / Field Level | Community health tracking, localized survey submissions. |
| **Pharmacist** | Facility Counter | Inventory management, prescription fulfillment logs. |

---

## Credentials Reference

> [!WARNING]  
> The following staging matrix outlines preset local node user accounts. Never commit real production credentials to public version control.

| System Role | Target Location / Node | User ID / Selection Option | Unique Password |
| :--- | :--- | :--- | :--- |
| State Administrator | All Districts | `ap_state_admin` | `AmaravatiHealth2026!` |
| District Officer | Visakhapatnam | `vsp_district_officer` | `VizagCMO#2026!` |
| District Officer | Vizianagaram | `vzm_district_officer` | `VizmCMO#2026!` |
| District Officer | Srikakulam | `skl_district_officer` | `SklmCMO#2026!` |
| Medical Doctor | Pendurthi CHC Hub (Vizag) | `Dr. S. Srinivasa Rao` | `SrinivasaDoc#77` |
| Medical Doctor | Pendurthi CHC Hub (Vizag) | `Dr. K. Anuradha` | `AnuradhaPed#45` |
| Medical Doctor | Bheemili Spoke (Vizag) | `Dr. A. Lakshmi Prasanna` | `LakshmiBhm#12` |
| Medical Doctor | Gajapathinagaram (Vzm) | `Dr. Ch. Koteswara Rao` | `KoteswaraVzm#39` |
| Medical Doctor | Srikakulam Rural (Skl) | `Dr. K. Venkataswamy` | `VenkatSklm#88` |
| ASHA Worker | Pendurthi Area (Vizag) | `asha_worker` | `AshaVizag$Pnd` |
| ASHA Worker | Gajapathinagaram (Vzm) | `asha_gajapathinagaram` | `AshaVizm$Gjn` |
| ASHA Worker | Srikakulam Rural (Skl) | `asha_srikakulam` | `AshaSklm$Rur` |
| Pharmacist | Pendurthi Counter (Vizag) | `pharma_person` | `PharmaPnd%99` |
| Pharmacist | Gajapathinagaram (Vzm) | `pharma_gajapathinagaram` | `PharmaGjn%88` |
| Pharmacist | Srikakulam Rural (Skl) | `pharma_srikakulam_rur` | `PharmaRur%77` |

---

## Security Guidelines
**Environment Variable Safeguards:** For automated initialization pipelines, inject usernames and passwords securely using `.env` configurations:
   ```bash
   SYS_ADMIN_USER="ap_state_admin"
   SYS_ADMIN_PASS="AmaravatiHealth2026!"
   ```

## ✒️ Author and Credits

* **Lead Architect & Developer:** [Srinivasta](https://github.com/SRINIVASTA) & My Team Mate:T.Pujitha Sri, BTECH (ECE), 2ND YEAR Student.

### Connect with Me
- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/srinivas-t-a-557637119/)  
- [![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/srinivasta)  
- [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tasrinivass@gmail.com)  
- [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/srinivasta)

