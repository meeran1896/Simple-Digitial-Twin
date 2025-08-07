"""
@author: Mohamed Meeran
"""
from influxdb_client import InfluxDBClient

token = "lbrO1-9JnC9yucjn0d40FkUMSvZVTXGjZBC6li_9TKpii-uwV-KEsOxUpafSEx3txaNhaRdvP1PqFT4KCj1noQ=="
org = "SUTD"
bucket = "tankdata"
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

query = '''
from(bucket:"tankdata")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "tank_level")
  |> filter(fn: (r) => r._field == "level" or r._field == "pump" or r._field == "valve")
  |> sort(columns: ["_time"])
'''

tables = query_api.query(query)

# Store data grouped by timestamp
data_by_time = {}

for table in tables:
    for record in table.records:
        timestamp = record.get_time()
        field = record.get_field()
        value = record.get_value()

        if timestamp not in data_by_time:
            data_by_time[timestamp] = {}

        data_by_time[timestamp][field] = value

# Print results
print(f"{'Timestamp':<30} {'Level':<10} {'Pump':<10} {'Valve':<10}")
print("-" * 60)
for timestamp, values in sorted(data_by_time.items()):
    level = values.get("level", "-")
    pump = values.get("pump", "-")
    valve = values.get("valve", "-")
    print(f"{timestamp:<30} {level:<10} {pump:<10} {valve:<10}")
