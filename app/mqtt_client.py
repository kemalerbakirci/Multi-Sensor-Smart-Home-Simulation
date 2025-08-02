import os
import logging
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

#Load environment variables from config/settings.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.env'))
BROKER_URL = os.getenv("BROKER_URL", "localhost")
BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))

#Setup structured logging for better debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def create_client(client_id: str, clean_session: bool = False) -> mqtt.Client:
    """
    Creates and returns an MQTT client with persistent session support.
    
    Args:
        client_id (str): Unique ID for the MQTT client (must be unique per device).
        clean_session (bool): If False, broker will store session data (persistent session).

    Returns:
        mqtt.Client: Configured MQTT client ready to connect.
    """

    #Create MQTT client with persistent session (clean_session=False)
    #clean_session=False → broker remembers subscriptions & queued messages
    client = mqtt.Client(client_id=client_id, clean_session=clean_session, protocol=mqtt.MQTTv311)

    #Attach event callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    #Connect to broker
    client.connect(BROKER_URL, BROKER_PORT)

    return client

def on_connect(client, userdata, flags, rc):
    """
    Callback executed when the client connects to the broker.
    rc (result code) = 0 means success
    """
    if rc == 0:
        logger.info(f"[MQTT] Connected successfully with client_id={client._client_id.decode()}")
    else:
        logger.error(f"[MQTT] Connection failed (rc={rc})")

def on_disconnect(client, userdata, rc):
    """
    Callback executed when the client disconnects.
    rc=0 → clean disconnect
    rc>0 → unexpected disconnection
    """
    logger.info(f"[MQTT] Disconnected (rc={rc})")
