import os
import csv
import sqlite3
import time
from datetime import datetime
from dotenv import load_dotenv

#Load settings
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "config", "settings.env"))
CSV_DIR = os.getenv("CSV_DIR", "data/logs")
DB_PATH = os.getenv("DB_PATH", "data/database/sensors.db")

#Ensure folders exist
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def init_db():
    """
    Initializes SQLite database and creates the table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            device_id TEXT,
            sensor_type TEXT,
            value REAL
        )
    """)
    conn.commit()
    conn.close()


def log_to_csv(data: dict):
    """
    Logs a single sensor reading to a CSV file.
    A new file is created for each day.
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    csv_file = os.path.join(CSV_DIR, f"{date_str}_sensors.csv")

    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "device_id", "sensor_type", "value"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def log_to_sqlite(data: dict):
    """
    Logs a single sensor reading to SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensor_data (timestamp, device_id, sensor_type, value) VALUES (?, ?, ?, ?)",
        (data["timestamp"], data["device_id"], data["sensor_type"], data["value"])
    )
    conn.commit()
    conn.close()
