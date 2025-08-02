# Multi-Sensor Smart Home Simulation

## 📌 Overview
This project simulates multiple smart home sensors (temperature, humidity, motion) that publish data to an MQTT broker with **persistent sessions** and **QoS 1/2**.  
A subscriber receives all sensor data, validates JSON payloads, and logs valid messages to **CSV files** and an **SQLite database**.  
The CLI dashboard provides options to run sensors, view data, export records, and visualize trends.

---

## 📂 Directory Structure
Multi-Sensor-Smart-Home-Simulation/
├── app/
│   ├── mqtt_client.py        # Creates persistent MQTT clients
│   ├── sensor_simulator.py   # Simulates multiple sensors
│   ├── subscriber.py         # Subscribes to MQTT topics and logs data
│   ├── data_logger.py        # Handles CSV and SQLite logging
│   ├── schema_validator.py   # Validates JSON payloads
│   └── cli.py                # CLI dashboard
├── config/settings.env       # Broker URL, topic prefix, DB path
├── data/logs/                # CSV logs (kept empty with .gitkeep)
├── data/database/            # SQLite DB (kept empty with .gitkeep)
├── requirements.txt
├── run.py
├── README.md
└── .gitignore

---

## 🚀 Features
✅ Simulates temperature, humidity, and motion sensors  
✅ Uses MQTT persistent sessions (`clean_session=False`)  
✅ Supports QoS 1 or 2 for reliable message delivery  
✅ Validates JSON payloads using JSON Schema  
✅ Logs data to **CSV files** and **SQLite database**  
✅ CLI dashboard to manage sensors and subscriber  
✅ Data export to **CSV & JSON**  
✅ Graph plotting and statistics display  

---

## 📦 Installation
```bash
git clone <repo-url>
cd Multi-Sensor-Smart-Home-Simulation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ⚙️ Configuration
Edit `config/settings.env`:
```
BROKER_URL=localhost
BROKER_PORT=1883
TOPIC_PREFIX=home/sensors
DB_PATH=data/database/sensors.db
CSV_DIR=data/logs
```

---

## ▶️ How to Run
### 1️⃣ Start MQTT Broker
```bash
mosquitto
```

### 2️⃣ Start CLI Dashboard
```bash
python run.py
```

### 3️⃣ Choose Options
```
==== Smart Home Simulation Dashboard ====
1) Start Smart Home Subscriber (Hub)
2) Start Temperature Sensor
3) Start Humidity Sensor
4) Start Motion Sensor
5) Start All Sensors
6) Exit
7) Show Last 10 Stored Records
8) Run All Sensors for Limited Time
9) Show Statistics (Avg/Min/Max)
10) Show Graphs
11) Export All Data (CSV & JSON)
```

---

## 📊 Data Storage
- CSV logs → `data/logs/` (one file per day)
- SQLite DB → `data/database/sensors.db` (auto-created)

To query database:
```bash
sqlite3 data/database/sensors.db
.tables
SELECT * FROM sensor_data LIMIT 5;
.exit
```

---

## 📂 Exports
Use Option 11 to export all records:  
- `exports/sensor_data_export.csv`  
- `exports/sensor_data_export.json`

---

## 📜 Learning Objectives
- Understand MQTT persistent sessions and QoS
- Use JSON Schema validation
- Log IoT data to CSV and SQLite
- Build a CLI dashboard with data export and visualization

---

## 📄 License
MIT License
