import requests
import json
import time
import sys

# API endpoint
url = "http://localhost:5000/measurement"

# Sample measurement data
measurement = {
    "timestamp": int(time.time()),
    "data": {
        "water_level": 50,
        "inside": {
            "up": {
                "temperature": 22.5,
                "humidity": 45.0
            },
            "down": {
                "temperature": 21.0,
                "humidity": 50.0
            }
        },
        "outside": {
            "up": {
                "temperature": 20.0,
                "humidity": 55.0,
                "lux": 300.0
            },
            "down": {
                "temperature": 19.5,
                "humidity": 60.0,
                "lux": 250.0
            }
        }
    }
}

# Check if user wants to test low water level
if len(sys.argv) > 1 and sys.argv[1] == '--low-water':
    measurement['data']['water_level'] = 15
    print("Testing with LOW WATER LEVEL (15mm)")

# Send the measurement
response = requests.post(url, json=measurement)

if response.status_code == 200:
    print("Measurement sent successfully!")
    print(f"Water level: {measurement['data']['water_level']}mm")
    print(f"Response: {response.json()}")
else:
    print(f"Error: {response.status_code}")
    print(f"Response: {response.text}")