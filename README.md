                      ┌──────────────────────────┐
                      │   1. Flask App (API)     │
                      │ ──────────────────────── │
                      │   /simulate (GET)        │
                      │   /reset (POST)          │
                      └────────────┬─────────────┘
                                   │
                       [Internal Python Thread]
                                   │
                                   ▼
                      ┌──────────────────────────┐
                      │ 2. Simulator Logic        │
                      │ ──────────────────────── │
                      │ Tank Level, Valve, Pumps │
                      │  ➜ Generates data every 1s│
                      └────────────┬─────────────┘
                                   │
                                   ▼
                      ┌──────────────────────────┐
                      │ 3. ZMQ Publisher (PUB)    │
                      │   tcp://*:5556           │
                      └────────────┬─────────────┘
                                   │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
   ┌────────────────────────┐         ┌────────────────────────┐
   │ 4. ZMQ Subscriber      │         │ (Future) Other Clients │
   │ ────────────────────── │         │ that listen via ZMQ    │
   │ ➜ Listens on port 5556 │         └────────────────────────┘
   │ ➜ Parses incoming JSON │
   │ ➜ Writes to InfluxDB   │
   └────────────┬───────────┘
                │
                ▼
   ┌────────────────────────┐
   │ 5. InfluxDB (TimeSeries)│
   └────────────┬───────────┘
                │
                ▼
   ┌────────────────────────┐
   │ 6. Grafana Dashboard   │
   │ ➜ Real-time graphs     │
   │ ➜ No manual refresh    │
   └────────────────────────┘
