#!/usr/bin/env python3
"""
Test script to verify Telegram notifications are working correctly
"""
import os
import requests
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE')

def test_telegram_notification():
    """Test sending a notification directly to Telegram"""
    
    # Check configuration
    if TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Error: TELEGRAM_BOT_TOKEN not configured")
        print("Please set your bot token in .env file or environment variables")
        return False
    
    if TELEGRAM_CHAT_ID == 'YOUR_CHAT_ID_HERE':
        print("❌ Error: TELEGRAM_CHAT_ID not configured")
        print("Please set your chat ID in .env file or environment variables")
        return False
    
    print(f"Testing Telegram notification...")
    print(f"Bot Token: {TELEGRAM_BOT_TOKEN[:20]}...")
    print(f"Chat ID: {TELEGRAM_CHAT_ID}")
    
    # Prepare test message
    message = "🧪 *Test Notification*\n\n"
    message += "This is a test message from your Water Level Monitor.\n"
    message += "If you see this, Telegram notifications are working! ✅"
    
    # Send the message
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(url, json={
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }, timeout=10)
        
        if response.status_code == 200:
            print("✅ Success! Telegram notification sent successfully")
            print("Check your Telegram for the test message")
            return True
        else:
            print(f"❌ Error: Failed to send notification")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Common error explanations
            if response.status_code == 401:
                print("\n💡 This usually means your bot token is incorrect")
            elif response.status_code == 400:
                print("\n💡 This usually means your chat ID is incorrect")
                print("Make sure you've started a conversation with your bot first")
            
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out after 10 seconds")
        print("Check your internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to Telegram")
        print("Check your internet connection and firewall settings")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_bot_info():
    """Get information about the bot"""
    if TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        return
    
    print("\nChecking bot information...")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            bot_info = response.json()['result']
            print(f"Bot Name: {bot_info.get('first_name', 'Unknown')}")
            print(f"Bot Username: @{bot_info.get('username', 'Unknown')}")
        else:
            print("Could not retrieve bot information")
    except:
        pass

if __name__ == "__main__":
    print("Water Level Monitor - Telegram Notification Test")
    print("=" * 50)
    
    # Check bot info
    check_bot_info()
    
    print()
    
    # Test notification
    success = test_telegram_notification()
    
    if not success:
        print("\nTroubleshooting steps:")
        print("1. Make sure you've created a bot with @BotFather")
        print("2. Verify your bot token is correct")
        print("3. Start a conversation with your bot")
        print("4. Get your chat ID from: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates")
        print("5. Set both values in your .env file")
        sys.exit(1)
    else:
        print("\n✅ All tests passed! Your notifications are ready to go.")
        sys.exit(0)