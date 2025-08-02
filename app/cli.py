import threading
import sqlite3
import os
import matplotlib.pyplot as plt
import pandas as pd
import json
from dotenv import load_dotenv
from app.subscriber import start_subscriber
from app.sensor_simulator import simulate_sensor
from app.data_logger import init_db

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "config", "settings.env"))
DB_PATH = os.getenv("DB_PATH", "data/database/sensors.db")

MENU = """
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
Choose an option: """

def show_last_records():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, device_id, sensor_type, value FROM sensor_data ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("\n=== Last 10 Records ===")
        for row in rows:
            print(f"Timestamp: {row[0]} | Device: {row[1]} | Sensor: {row[2]} | Value: {row[3]}")
    else:
        print("[INFO] No records found yet.")

def show_statistics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT AVG(value), MIN(value), MAX(value) FROM sensor_data WHERE sensor_type='temperature'")
    temp_stats = cursor.fetchone()

    cursor.execute("SELECT AVG(value), MIN(value), MAX(value) FROM sensor_data WHERE sensor_type='humidity'")
    hum_stats = cursor.fetchone()

    conn.close()

    print("\n=== Sensor Statistics ===")
    if temp_stats[0] is not None:
        print(f"Temperature -> Avg: {temp_stats[0]:.2f}, Min: {temp_stats[1]:.2f}, Max: {temp_stats[2]:.2f}")
    else:
        print("Temperature -> No data yet")

    if hum_stats[0] is not None:
        print(f"Humidity    -> Avg: {hum_stats[0]:.2f}, Min: {hum_stats[1]:.2f}, Max: {hum_stats[2]:.2f}")
    else:
        print("Humidity    -> No data yet")

def plot_graph():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT timestamp, sensor_type, value FROM sensor_data", conn)
    conn.close()

    if df.empty:
        print("[INFO] No data available for plotting.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    for sensor in ["temperature", "humidity"]:
        subset = df[df["sensor_type"] == sensor]
        if not subset.empty:
            plt.figure(figsize=(8, 5))
            plt.plot(subset["timestamp"], subset["value"], marker="o", label=sensor.capitalize())
            plt.title(f"{sensor.capitalize()} Over Time")
            plt.xlabel("Time")
            plt.ylabel("Value")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

def export_data():
    """Exports all stored data to CSV and JSON files."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sensor_data", conn)
    conn.close()

    if df.empty:
        print("[INFO] No data available to export.")
        return

    os.makedirs("exports", exist_ok=True)
    csv_path = "exports/sensor_data_export.csv"
    json_path = "exports/sensor_data_export.json"

    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2)

    print(f"[INFO] Data exported to {csv_path} and {json_path}")

def main():
    while True:
        choice = input(MENU).strip()

        if choice == "1":
            print("[INFO] Starting subscriber (hub)...")
            threading.Thread(target=start_subscriber, daemon=True).start()

        elif choice == "2":
            threading.Thread(target=simulate_sensor, args=("temperature", "temp-1", 2.0, 1), daemon=True).start()

        elif choice == "3":
            threading.Thread(target=simulate_sensor, args=("humidity", "hum-1", 2.0, 1), daemon=True).start()

        elif choice == "4":
            threading.Thread(target=simulate_sensor, args=("motion", "motion-1", 2.0, 1), daemon=True).start()

        elif choice == "5":
            threading.Thread(target=simulate_sensor, args=("temperature", "temp-1", 2.0, 1), daemon=True).start()
            threading.Thread(target=simulate_sensor, args=("humidity", "hum-1", 2.0, 1), daemon=True).start()
            threading.Thread(target=simulate_sensor, args=("motion", "motion-1", 2.0, 1), daemon=True).start()

        elif choice == "6":
            print("[INFO] Exiting simulation.")
            break

        elif choice == "7":
            show_last_records()

        elif choice == "8":
            try:
                duration = float(input("Enter duration in seconds: "))
                print(f"[INFO] Running all sensors for {duration} seconds...")
                threading.Thread(target=simulate_sensor, args=("temperature", "temp-1", 2.0, 1, duration), daemon=True).start()
                threading.Thread(target=simulate_sensor, args=("humidity", "hum-1", 2.0, 1, duration), daemon=True).start()
                threading.Thread(target=simulate_sensor, args=("motion", "motion-1", 2.0, 1, duration), daemon=True).start()
            except ValueError:
                print("[ERROR] Please enter a valid number.")

        elif choice == "9":
            show_statistics()

        elif choice == "10":
            plot_graph()

        elif choice == "11":
            export_data()

        else:
            print("[ERROR] Invalid option. Please choose 1-11.")
