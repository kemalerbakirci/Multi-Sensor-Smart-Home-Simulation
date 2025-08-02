import jsonschema
from jsonschema import validate

#Define the expected structure of sensor messages
sensor_schema = {
    "type": "object",
    "properties": {
        "timestamp": {"type": "number"},
        "device_id": {"type": "string"},
        "sensor_type": {"type": "string", "enum": ["temperature", "humidity", "motion"]},
        "value": {"type": ["number", "integer"]}
    },
    "required": ["timestamp", "device_id", "sensor_type", "value"]
}

def validate_message(message: dict) -> bool:
    """
    Validates a sensor message against the schema.
    
    Args:
        message (dict): The incoming JSON message.
    Returns:
        bool: True if valid, False if invalid.
    """
    try:
        validate(instance=message, schema=sensor_schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"[INVALID MESSAGE] {e.message}")
        return False
