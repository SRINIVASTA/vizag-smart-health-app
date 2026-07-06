vizag-smart-health-app/
│
├── .streamlit/
│   └── config.toml          # Custom theme configuration variables
│
├── data/
│   ├── schema.sql           # Database creation commands (Seeded for AP Pilot)
│   └── smart_health.db      # Local SQLite3 database instance
│
├── src/
│   ├── __init__.py          # Designates folder as importable package
│   ├── auth.py              # User registers and transaction log hooks
│   ├── drone_logistics.py   # Coordinate generator for flight paths
│   ├── language_pack.py     # Localized string matrix (EN, HI, TE)
│   ├── predictive_engine.py # Resource balancing and outbreak mapping algorithms
│   └── telehealth.py        # WhatsApp e-Sanjeevani link builder tools
│
├── app.py                   # System core orchestrator loop layout
├── README.md                # Technical operational setup documentation
└── requirements.txt         # Production library dependency manifest
