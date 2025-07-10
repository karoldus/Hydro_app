# Measurement API and Dashboard

A Flask application for receiving sensor measurements via API and displaying them in real-time on a web dashboard.

## Project Structure

```
measurement-app/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── test_script.py        # Test script for sending measurements
├── README.md             # This file
│
├── data/                 # CSV data files (created automatically)
│   └── measurements_*.csv
│
├── templates/            # HTML templates
│   └── index.html        # Dashboard page
│
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Dashboard styles
    └── js/
        └── dashboard.js  # Dashboard JavaScript
```

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access the dashboard at: http://localhost:5000

## API Endpoint

### POST /measurement

Send measurement data in JSON format:

```json
{
    "timestamp": 123456789,
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
```

## Testing

Use the provided `test_script.py` to send sample measurements:

```bash
python test_script.py
```

## Data Storage

- Measurements are saved to CSV files automatically
- One file per day: `measurements_YYYY-MM-DD.csv`
- Files are created in the `data/` directory
- The data directory is created automatically if it doesn't exist

## Features

- Real-time dashboard updates using WebSocket
- Automatic CSV file generation
- Clean, responsive web interface
- Connection status indicator
- Displays latest measurement data