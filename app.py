import os
import csv
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store the latest measurement in memory
latest_measurement = None

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
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)