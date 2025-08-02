import json
import os
from app.mqtt_client import create_client
from app.schema_validator import validate_message
from app.data_logger import log_to_csv, log_to_sqlite, init_db
from dotenv import load_dotenv

#Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "config", "settings.env"))
TOPIC_PREFIX = os.getenv("TOPIC_PREFIX", "home/sensors")

def on_message(client, userdata, msg):
    """
    Callback executed whenever a subscribed MQTT message is received.
    """
    try:
        payload = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON received on {msg.topic}")
        return

    if validate_message(payload):
        print(f"[RECEIVED] Topic: {msg.topic} | Data: {payload}")
        log_to_csv(payload)
        log_to_sqlite(payload)
    else:
        print(f"[INVALID] Topic: {msg.topic} | Payload rejected")

def start_subscriber():
    """
    Connects to MQTT broker and subscribes to all sensor topics.
    """
    #Ensure database is ready
    init_db()

    #Create persistent MQTT client
    client = create_client(client_id="smart-home-subscriber", clean_session=False)

    #Subscribe to all sensors (temperature, humidity, motion)
    topic = f"{TOPIC_PREFIX}/#"
    client.subscribe(topic, qos=1)

    client.on_message = on_message

    print(f"[INFO] Subscribed to {topic}")
    client.loop_forever()  # Keep listening forever
