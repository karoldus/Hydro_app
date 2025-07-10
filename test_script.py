import requests
import json
import time

# API endpoint
url = "http://localhost:5000/measurement"

# Sample measurement data
measurement = {
    "timestamp": int(time.time()),
    "data": {
        "water_level": 40,
        "inside": {
            "up": {
                "temperature": 23.5,
                "humidity": 43.0
            },
            "down": {
                "temperature": 23.0,
                "humidity": 53.0
            }
        },
        "outside": {
            "up": {
                "temperature": 23.0,
                "humidity": 53.0,
                "lux": 303.0
            },
            "down": {
                "temperature": 13.5,
                "humidity": 63.0,
                "lux": 253.0
            }
        }
    }
}

# Send the measurement
response = requests.post(url, json=measurement)

if response.status_code == 200:
    print("Measurement sent successfully!")
    print(f"Response: {response.json()}")
else:
    print(f"Error: {response.status_code}")
    print(f"Response: {response.text}")