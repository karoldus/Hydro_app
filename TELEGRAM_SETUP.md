# Telegram Bot Setup Guide

This guide will help you set up Telegram notifications for low water level alerts.

## Step 1: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Start a conversation with BotFather
3. Send the command `/newbot`
4. Choose a name for your bot (e.g., "Water Level Monitor")
5. Choose a username for your bot (must end with 'bot', e.g., "water_level_monitor_bot")
6. BotFather will give you a token that looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
7. **Save this token** - you'll need it for the `TELEGRAM_BOT_TOKEN`

## Step 2: Get Your Chat ID

1. Start a conversation with your bot (search for the username you created)
2. Send any message to your bot
3. Open this URL in your browser (replace YOUR_BOT_TOKEN with your actual token):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
4. Look for `"chat":{"id":123456789}` in the response
5. The number (123456789) is your Chat ID
6. **Save this Chat ID** - you'll need it for the `TELEGRAM_CHAT_ID`

## Step 3: Configure the Application

### Option 1: Using Environment Variables (Recommended)

Create a `.env` file in your project directory:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

Install python-dotenv:
```bash
pip install python-dotenv
```

### Option 2: Using System Environment Variables

On Linux/Mac:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

On Windows:
```cmd
set TELEGRAM_BOT_TOKEN=your_bot_token_here
set TELEGRAM_CHAT_ID=your_chat_id_here
```

### Option 3: Direct Code Modification (Not Recommended)

Edit `app.py` and replace the placeholder values:
```python
TELEGRAM_BOT_TOKEN = 'your_actual_bot_token_here'
TELEGRAM_CHAT_ID = 'your_actual_chat_id_here'
```

## Step 4: Test the Setup

1. Run the application:
   ```bash
   python app.py
   ```

2. Test with low water level:
   ```bash
   python test_script.py --low-water
   ```

3. You should receive a Telegram message like:
   ```
   ⚠️ Low Water Level Alert!
   
   Water level is critically low: 15 mm
   Threshold: 20 mm
   Time: 2025-07-10 15:30:45
   
   Please check the water tank!
   ```

## Customization

### Change the Water Level Threshold

The default threshold is 20mm. To change it:

1. Set an environment variable:
   ```bash
   export WATER_LEVEL_THRESHOLD=30
   ```

2. Or modify in `app.py`:
   ```python
   WATER_LEVEL_THRESHOLD = 30
   ```

## Troubleshooting

### Bot not sending messages?

1. Check if the bot token is correct
2. Verify the chat ID is correct
3. Make sure you've started a conversation with your bot
4. Check the console output for error messages

### "Telegram bot not configured" message?

This means either:
- `TELEGRAM_BOT_TOKEN` is not set or is still the placeholder value
- `TELEGRAM_CHAT_ID` is not set or is still the placeholder value

### Test your bot manually:

Send a test message using curl:
```bash
curl -X POST "https://api.telegram.org/botYOUR_BOT_TOKEN/sendMessage" \
     -H "Content-Type: application/json" \
     -d '{"chat_id": "YOUR_CHAT_ID", "text": "Test message"}'
```

## Security Notes

- **Never commit** your bot token or chat ID to version control
- Use environment variables or `.env` files
- Add `.env` to your `.gitignore` file
- Keep your bot token secret - anyone with the token can control your bot