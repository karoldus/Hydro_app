import os
import csv
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import json
import threading
import requests
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store the latest measurement in memory
latest_measurement = None
last_notification_time = 0

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE')
WATER_LEVEL_THRESHOLD = int(os.environ.get('WATER_LEVEL_THRESHOLD', '20'))
NOTIFICATION_COOLDOWN = int(os.environ.get('NOTIFICATION_COOLDOWN', '300'))  # 5 minutes default

# Check if Telegram is configured
telegram_configured = (TELEGRAM_BOT_TOKEN != 'YOUR_BOT_TOKEN_HERE' and 
                      TELEGRAM_CHAT_ID != 'YOUR_CHAT_ID_HERE')

def save_to_csv(measurement):
    """Save measurement data to CSV file"""
    # Get the date from timestamp
    timestamp = measurement['timestamp']
    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    
    # Create filename with date in data directory
    filename = os.path.join('data', f'measurements_{date}.csv')
    
    # Extract data
    data = measurement['data']
    row = [
        timestamp,
        data['water_level'],
        data['inside']['up']['temperature'],
        data['inside']['up']['humidity'],
        data['inside']['down']['temperature'],
        data['inside']['down']['humidity'],
        data['outside']['up']['temperature'],
        data['outside']['up']['humidity'],
        data['outside']['up']['lux'],
        data['outside']['down']['temperature'],
        data['outside']['down']['humidity'],
        data['outside']['down']['lux']
    ]
    
    # Check if file exists
    file_exists = os.path.isfile(filename)
    
    # Write to CSV
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header if file is new
        if not file_exists:
            header = [
                'timestamp', 'water_level', 
                'inside_up_temperature', 'inside_up_humidity',
                'inside_down_temperature', 'inside_down_humidity',
                'outside_up_temperature', 'outside_up_humidity', 'outside_up_lux',
                'outside_down_temperature', 'outside_down_humidity', 'outside_down_lux'
            ]
            writer.writerow(header)
        
        writer.writerow(row)

def send_telegram_notification_thread(water_level, timestamp):
    """Send Telegram notification in a separate thread"""
    try:
        send_telegram_notification(water_level, timestamp)
    except Exception as e:
        logger.error(f"Error in telegram notification thread: {e}")

def send_telegram_notification(water_level, timestamp):
    """Send Telegram notification for low water level using requests"""
    if not telegram_configured:
        logger.info("Telegram bot not configured. Skipping notification.")
        return
    
    global last_notification_time
    
    try:
        date_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        # Prepare the message
        message = f"⚠️ *Halo! Hydro domaga się wody!*\n\n"
        message += f"Aktualny poziom: *{water_level} mm*\n"
        message += f"Threshold: {WATER_LEVEL_THRESHOLD} mm\n"
        message += f"Czas: {date_time}\n\n"
        message += f"Dolej wody, bo biedne roślinki umrą ☠️!"
        
        # Telegram API URL
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        # Send the message
        response = requests.post(url, json={
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"Telegram notification sent successfully: Water level {water_level}mm")
        else:
            logger.error(f"Failed to send Telegram notification. Status code: {response.status_code}, Response: {response.text}")
            
    except requests.exceptions.Timeout:
        logger.error("Telegram notification timed out after 10 seconds")
        last_notification_time = 0
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to Telegram API")
        last_notification_time = 0
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {e}")
        last_notification_time = 0

@app.route('/')
def index():
    """Serve the webpage"""
    return render_template('index.html')

@app.route('/measurement', methods=['POST'])
def measurement():
    """Handle measurement POST requests"""
    global latest_measurement, last_notification_time
    
    try:
        # Get JSON data
        measurement_data = request.get_json()
        
        # Validate required fields
        if not measurement_data or 'data' not in measurement_data:
            return jsonify({'error': 'Invalid data format'}), 400
        
        # get current timestamp
        measurement_data['timestamp'] = int(datetime.now().timestamp())
        
        # Save to CSV
        save_to_csv(measurement_data)
        
        # Update latest measurement
        latest_measurement = measurement_data
        
        # Check water level and send notification if needed
        water_level = measurement_data['data']['water_level']
        current_time = time.time()
        
        if water_level <= WATER_LEVEL_THRESHOLD:
            # Check if enough time has passed since last notification
            if current_time - last_notification_time >= NOTIFICATION_COOLDOWN:
                last_notification_time = current_time
                
                # Send notification in a separate thread to avoid blocking
                notification_thread = threading.Thread(
                    target=send_telegram_notification_thread,
                    args=(water_level, measurement_data['timestamp'])
                )
                notification_thread.daemon = True
                notification_thread.start()
            else:
                remaining_time = NOTIFICATION_COOLDOWN - (current_time - last_notification_time)
                logger.info(f"Skipping notification - cooldown active. Next notification in {remaining_time:.0f} seconds")
        
        # Emit to all connected clients
        socketio.emit('new_measurement', measurement_data)
        
        return jsonify({'status': 'success', 'message': 'Measurement saved'}), 200
        
    except Exception as e:
        logger.error(f"Error processing measurement: {e}")
        return jsonify({'error': str(e)}), 500

@socketio.on('request_latest')
def handle_request_latest():
    """Send the latest measurement to the requesting client"""
    if latest_measurement:
        emit('new_measurement', latest_measurement)

if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Run the app
    print("Starting Measurement API and Web App...")
    print("API endpoint: http://localhost:5000/measurement")
    print("Web interface: http://localhost:5000")
    
    # Telegram bot status
    if telegram_configured:
        print(f"Telegram notifications: ENABLED")
        print(f"  - Water level threshold: {WATER_LEVEL_THRESHOLD}mm")
        print(f"  - Notification cooldown: {NOTIFICATION_COOLDOWN} seconds")
    else:
        print("Telegram notifications: DISABLED (configure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)