"""
Optional configuration file for advanced settings
"""
import os

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE')

# Water Level Settings
WATER_LEVEL_THRESHOLD = int(os.environ.get('WATER_LEVEL_THRESHOLD', '20'))

# Notification Settings
NOTIFICATION_COOLDOWN = int(os.environ.get('NOTIFICATION_COOLDOWN', '300'))  # 5 minutes default
NOTIFICATION_TIMEOUT = int(os.environ.get('NOTIFICATION_TIMEOUT', '10'))  # 10 seconds default

# Rate Limiting (to prevent notification spam)
# This tracks the last notification time to avoid sending too many
last_notification_time = {}

def should_send_notification(measurement_type='water_level'):
    """
    Check if enough time has passed since the last notification
    """
    import time
    current_time = time.time()
    
    if measurement_type not in last_notification_time:
        last_notification_time[measurement_type] = current_time
        return True
    
    time_since_last = current_time - last_notification_time[measurement_type]
    
    if time_since_last >= NOTIFICATION_COOLDOWN:
        last_notification_time[measurement_type] = current_time
        return True
    
    return False

# CSV Settings
CSV_DIRECTORY = os.environ.get('CSV_DIRECTORY', 'data')
CSV_DATE_FORMAT = os.environ.get('CSV_DATE_FORMAT', '%Y-%m-%d')

# Server Settings
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', '5000'))
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'