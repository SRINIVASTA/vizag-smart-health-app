# Vizag Smart Health Application (Andhra Pradesh Pilot Project)

An integrated, multi-tiered digital healthcare ecosystem tailored for the Visakhapatnam region. This application maps directly onto the Indian administrative hierarchy (State ➔ Division ➔ District ➔ Mandal ➔ Panchayat ➔ Village) to power guided telemedicine, real-time epidemic tracking, and autonomous drone logistics for hard-to-reach tribal tracts like Araku and Paderu.

🌐 **Live Interactive Web App:** [Launch Live Streamlit Dashboard](https://vizag-smart-health-app-hwpexsovxwurku4vqcuwpt.streamlit.app/)

## 🖥️ Project Presentation Pitch Deck

[![Pitch Deck PDF](https://shields.io)](https://github.com/SRINIVASTA/vizag-smart-health-app/blob/main/Visakhapatnam%20Smart%20Health%20Presentation.pdf)

📌 *Note for Judges: Click the badge above to open our complete **Project Underwriting Pitch Deck PDF** directly within GitHub's native, interactive document viewer.*

---

# BUILD WITH AI: CODE FOR COMMUNITIES (VIZAG EDITION)
Powered by Google Cloud | Hosted via Hack2skill & GDG Vizag

### 🏛️ Parliamentary Track Patrons
*   **Sujeet Kumar** (Hon'ble MP, Rajya Sabha) – Governance Innovation Lead
*   **Gaurav Gogoi** (Hon'ble MP, Lok Sabha) – Public Challenge Ideator
*   **Bansuri Swaraj** (Hon'ble MP, Lok Sabha) – Civic Progress Systems Advisor
*   **Sasmit Patra** (Hon'ble MP, Rajya Sabha) – Local Governance Tech Mentor
*   **Lavu Sri Krishna Devarayalu** (Hon'ble MP, Lok Sabha) – 'Kisan Alert' Challenge Mandate (Narasaraopet)
*   **Mathukumilli Bharat** (Hon'ble MP, Lok Sabha) – Student Skill Deployment Catalyst

### ⚡ GDG Vizag Core Leadership
*   **Usha Ramani Vemuru** – Event Leader & Primary Organiser (Founder, GURUJADA)
*   **Sai Sampath Kumar Balivada & Satheesh Karnatakapu** – Logistics & Co-Organisers
*   **Harsh Dattani** – Strategic Ecosystem Advisor & Support

### 🧠 AMA Technical Mentors & Experts
*   Saurabh Mishra | Jay Thakkar | Belal Khan (@probelalkhan) | Ajoe Joseph 
*   Namrata More | Chivukula Krishnamohan | Rakesh Asapanna | Darahas Muggu

### 🛠️ Support, Infrastructure & Volunteering
*   Jyothsna Ardhahakula – Event Volunteer
*   Ashwini & Sayyed Emkay – Community Support Enablers (Ientity)

---

## 🔑 Interactive Evaluation Guide (Passwordless Demo Login)

To optimize the evaluation process for judges and security reviewers, this application implements a secure, context-aware interface that eliminates hardcoded text secrets. 

### 🚀 Option 1: One-Click Evaluator Access (Recommended)
The live Streamlit application features a specialized **Judge Quick Demo Login** panel at the top of the sidebar. Evaluators can bypass manual sign-in entirely by clicking any of the preset role buttons:
*   **👑 State Admin Demo**: Launches macro epidemic analytics and state surveillance boards across Andhra Pradesh districts.
*   **📊 District Officer Demo**: Restricts tracking scope specifically to the Visakhapatnam administrative grid.
*   **🩺 Medical Doctor Demo**: Unlocks electronic health record (EHR) treatment tables and simulated e-Sanjeevani WebRTC stream rooms.
*   **🌾 ASHA Worker Demo**: Loads front-line mobile-friendly intake metrics forms for localized village data collection.
*   **💊 Pharmacist Demo**: Opens the fulfillment desk integrated with automated drone aero-logistics map tracking.

### 🔑 Option 2: Manual Staging Sign-In Form
If you prefer to test the manual input box elements, choose a role from the dropdown menu and use the unified sandbox testing password:
*   **System Password:** `demo123`

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

### 1. Multi-Tier Governance & RBAC (`app.py`)
Maps application views and dashboard permissions dynamically based on the administrative layer of the logged-in user without running cross-district visibility leaks.

### 2. Guided Telemedicine (`app.py`)
Implements the e-Sanjeevani hub-and-spoke logic. It pairs high-risk patients at rural Gram Panchayats with specialists at **King George Hospital (KGH), Visakhapatnam**, auto-triggering browser text-to-speech audio alerts for attending physicians.

### 3. Epidemic Engine (`src/predictive_engine.py`)
An automated local adaptation of India’s **Integrated Health Information Platform (IHIP)**. The engine constantly evaluates syndromic reporting input from the field to flag spatial anomaly risk clusters.

### 4. Drone Delivery Logistics (`app.py`)
Generates autonomous Beyond Visual Line of Sight (BVLOS) flight paths mapping from urban distribution hubs directly to inaccessible terrains in the **Vizag Agency areas (Ananthagiri, Paderu, Araku)** for time-critical drug drops, rendered natively via Streamlit's geospatial mapping framework.

### 5. Multi-Language Support (`app.py`)
Provides seamless UI toggles between **English and Hindi** to make the operational platform fully accessible to field staff on the ground.

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

### 4. Execute the Core Orchestrator
Launch the main application interface locally using Streamlit:
```bash
streamlit run app.py
```

---

## ✒️ Author and Credits
*   **Lead Architect & Developer:** Srinivasta
*   **Co-Developer:** T. Pujitha Sri (BTech ECE, 2nd Year Student)
