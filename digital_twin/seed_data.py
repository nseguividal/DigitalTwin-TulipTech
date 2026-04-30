# seed.py
import requests
import random
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# Realistic ranges per stand — each stand has slightly different conditions
STANDS = {
    "A1": {"temp": (19.5, 21.5), "hum": (62.0, 68.0)},
    "A2": {"temp": (21.0, 23.5), "hum": (58.0, 65.0)},
    "B1": {"temp": (20.0, 22.0), "hum": (70.0, 76.0)},
    "B2": {"temp": (18.5, 20.5), "hum": (74.0, 80.0)},
    "C1": {"temp": (22.0, 24.5), "hum": (55.0, 62.0)},
}

READINGS_PER_STAND = 3

print("Seeding database...\n")

for stand_id, ranges in STANDS.items():
    for i in range(READINGS_PER_STAND):
        payload = {
            "stand_id":    stand_id,
            "temperature": round(random.uniform(*ranges["temp"]), 1),
            "humidity":    round(random.uniform(*ranges["hum"]),  1),
        }
        response = requests.post(f"{BASE_URL}/api/sensors/", json=payload)

        if response.status_code == 201:
            data = response.json()
            print(f"  ✓ {stand_id}  |  {data['temperature']}°C  {data['humidity']}% RH  |  {data['timestamp']}")
        else:
            print(f"  ✗ {stand_id}  |  HTTP {response.status_code}  |  {response.text}")

print(f"\nDone — {len(STANDS) * READINGS_PER_STAND} rows inserted.")
print(f"Open http://localhost:8000 and click each stand to see the data.")