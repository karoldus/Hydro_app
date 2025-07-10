import os
import csv
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import json
import asyncio
from telegram import Bot
from telegram.error import TelegramError

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

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE')
WATER_LEVEL_THRESHOLD = 20

# Initialize Telegram bot
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN != 'YOUR_BOT_TOKEN_HERE' else None

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

async def send_telegram_notification(water_level, timestamp):
    """Send Telegram notification for low water level"""
    if not telegram_bot or TELEGRAM_CHAT_ID == 'YOUR_CHAT_ID_HERE':
        print("Telegram bot not configured. Skipping notification.")
        return
    
    try:
        date_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        message = f"⚠️ *Low Water Level Alert!*\n\n"
        message += f"Water level is critically low: *{water_level} mm*\n"
        message += f"Threshold: {WATER_LEVEL_THRESHOLD} mm\n"
        message += f"Time: {date_time}\n\n"
        message += f"Please check the water tank!"
        
        await telegram_bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
        print(f"Telegram notification sent: Water level {water_level}mm")
    except TelegramError as e:
        print(f"Failed to send Telegram notification: {e}")
    except Exception as e:
        print(f"Error sending Telegram notification: {e}")

@app.route('/')
def index():
    """Serve the webpage"""
    return render_template('index.html')

@app.route('/measurement', methods=['POST'])
def measurement():
    """Handle measurement POST requests"""
    global latest_measurement
    
    try:
        # Get JSON data
        measurement_data = request.get_json()
        
        # Validate required fields
        if not measurement_data or 'timestamp' not in measurement_data or 'data' not in measurement_data:
            return jsonify({'error': 'Invalid data format'}), 400
        
        # Save to CSV
        save_to_csv(measurement_data)
        
        # Update latest measurement
        latest_measurement = measurement_data
        
        # Check water level and send notification if needed
        water_level = measurement_data['data']['water_level']
        if water_level <= WATER_LEVEL_THRESHOLD:
            # Run async notification in background
            asyncio.run(send_telegram_notification(water_level, measurement_data['timestamp']))
        
        # Emit to all connected clients
        socketio.emit('new_measurement', measurement_data)
        
        return jsonify({'status': 'success', 'message': 'Measurement saved'}), 200
        
    except Exception as e:
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
    if telegram_bot:
        print(f"Telegram notifications: ENABLED (threshold: {WATER_LEVEL_THRESHOLD}mm)")
    else:
        print("Telegram notifications: DISABLED (configure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)