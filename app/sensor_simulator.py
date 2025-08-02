import json
import time
import random
import os
from app.mqtt_client import create_client
from dotenv import load_dotenv

# Load environment variables from config/settings.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.env'))
TOPIC_PREFIX = os.getenv("TOPIC_PREFIX", "home/sensors")

def simulate_sensor(sensor_type: str, device_id: str, interval: float = 2.0, qos: int = 1, duration: float = None):
    """
    Simulates a sensor publishing random values to an MQTT topic.

    Args:
        sensor_type (str): Type of sensor (temperature, humidity, motion).
        device_id (str): Unique ID for the sensor.
        interval (float): Seconds between messages.
        qos (int): MQTT QoS level.
        duration (float, optional): If set, stops after X seconds.
    """
    client = create_client(client_id=f"{sensor_type}-{device_id}", clean_session=False)
    client.loop_start()  # Start background network thread

    start_time = time.time()

    try:
        while True:
            # Stop after 'duration' seconds if specified
            if duration and (time.time() - start_time) >= duration:
                print(f"[INFO] {sensor_type} sensor finished after {duration} seconds.")
                break

            # Generate random sensor value
            if sensor_type == "temperature":
                value = round(random.uniform(18.0, 30.0), 2)
            elif sensor_type == "humidity":
                value = round(random.uniform(30.0, 90.0), 2)
            elif sensor_type == "motion":
                value = random.choice([0, 1])
            else:
                raise ValueError("Unknown sensor type")

            payload = {
                "timestamp": time.time(),
                "device_id": device_id,
                "sensor_type": sensor_type,
                "value": value
            }

            topic = f"{TOPIC_PREFIX}/{sensor_type}/{device_id}"
            client.publish(topic, json.dumps(payload), qos=qos)

            print(f"[PUBLISH] {sensor_type.upper()} | Topic: {topic} | Payload: {payload}")
            time.sleep(interval)

    finally:
        client.loop_stop()
        client.disconnect()