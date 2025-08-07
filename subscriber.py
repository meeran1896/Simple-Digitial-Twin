"""
@author: Mohamed Meeran
"""

import zmq
from influxdb_client import InfluxDBClient, Point, WritePrecision

# InfluxDB Config
token = "lbrO1-9JnC9yucjn0d40FkUMSvZVTXGjZBC6li_9TKpii-uwV-KEsOxUpafSEx3txaNhaRdvP1PqFT4KCj1noQ=="
org = "SimpleDigitalTwin"
bucket = "tankdata"
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api()

def write_to_influx(data):
    point = Point("tank_level") \
        .tag("device", "simulator1") \
        .field("level", data["tank_level"]) \
        .field("pump1", data["pump1_state"]) \
        .field("pump2", data["pump2_state"]) \
        .field("valve", data["valve_state"]) \
        .field("jp1", data["jp_state"]) \
        .field("jpv1", data["jpv1_state"]) \
        .time(data["timestamp"], WritePrecision.MS)
    write_api.write(bucket=bucket, org=org, record=point)
    print("✅ Written to InfluxDB:", data)

# ZMQ Subscriber Setup
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.setsockopt_string(zmq.SUBSCRIBE, '')

print("📡 Listening for tank data on tcp://localhost:5556...")

# ---- Main Loop ----
try:
    while True:
        message = socket.recv_json()
        write_to_influx(message)

except KeyboardInterrupt:
    print("\n⛔ Stopped by user.")
finally:
    socket.close()
    context.term()
    client.close()
