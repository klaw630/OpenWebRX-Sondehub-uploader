#!/usr/bin/env python3
import json
import sys
import datetime
import paho.mqtt.client as mqtt

# MQTT broker settings
MQTT_BROKER = "172.17.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "openwebrx/SONDE"

# Required SondeHub fields and defaults
DEFAULTS = {
    "id": "UNKNOWN",
    "type": "RS41",
    "frame": 0,
    "lat": 0.0,
    "lon": 0.0,
    "alt": 0.0,
    "heading": 0.0,
    "speed": 0.0,
    "vspeed": 0.0,
    "temperature": 0.0,
    "humidity": 0.0,
    "pressure": 0.0,
    "freq": 0.0,  # MHz
    "datetime": datetime.datetime.utcnow().isoformat() + "Z"
}

# Convert incoming MQTT telemetry to SondeHub-compatible JSON
def convert_to_sondehub(telem):
    # If wrapped in "data" key (like OpenWebRX)
    if "data" in telem:
        telem = telem["data"]

    # Ensure required fields exist
    for key, val in DEFAULTS.items():
        if key not in telem or telem[key] is None:
            telem[key] = val

    # Convert frequency to MHz if needed
    if "tx_frequency" in telem:
        telem["freq"] = telem["tx_frequency"] / 1_000_000.0  # Hz -> MHz
    elif "freq" in telem:
        # Ensure it's float
        telem["freq"] = float(telem["freq"])
    else:
        telem["freq"] = 0.0

    # Ensure datetime is ISO format string
    if isinstance(telem.get("datetime"), (int, float)):
        telem["datetime"] = datetime.datetime.utcfromtimestamp(telem["datetime"] / 1000.0).isoformat() + "Z"

    return telem

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}", file=sys.stderr)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        sh_telemetry = convert_to_sondehub(data)
        # Pipe to sondehub.py
        print(json.dumps(sh_telemetry), flush=True)
    except Exception as e:
        print(f"Failed to process line: {msg.payload.decode()} - {e}", file=sys.stderr)

# MQTT client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Run MQTT loop
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Stopping...", file=sys.stderr)
