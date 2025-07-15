# Measurement API and Dashboard

A Flask application for receiving sensor measurements via API and displaying them in real-time on a web dashboard. Includes Telegram notifications for low water level alerts.

## Features

- Real-time dashboard updates using WebSocket
- Automatic CSV file generation
- Clean, responsive web interface
- Connection status indicator
- Displays latest measurement data
- **Telegram notifications when water level is low (≤20mm)**

## Project Structure

```
measurement-app/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── test_script.py        # Test script for sending measurements
├── test_notification.py  # Test script for Telegram notifications
├── config.py             # Optional advanced configuration
├── README.md             # This file
├── TELEGRAM_SETUP.md     # Telegram bot setup guide
├── .env.example          # Example environment variables
├── .gitignore           # Git ignore file
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

Use the provided test scripts:

```bash
# Test normal water level (50mm)
python test_script.py

# Test low water level (15mm) - triggers Telegram notification
python test_script.py --low-water

# Test Telegram notifications directly (without sending measurement)
python test_notification.py
```

## Telegram Notifications

The app can send Telegram notifications when water level drops to 20mm or below.

### Quick Setup

1. Create a bot with @BotFather on Telegram
2. Get your bot token and chat ID
3. Set environment variables:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token"
   export TELEGRAM_CHAT_ID="your_chat_id"
   ```

See `TELEGRAM_SETUP.md` for detailed instructions.

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
- Visual water level status indicator
- Telegram notifications when water level is low (≤20mm)