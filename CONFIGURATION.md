# Project Configuration

This document captures the exact configuration of the Better-U-Bot project to ensure reproducibility and avoid dependency conflicts.

## Python Version
- Required: Python 3.10.x (specified in pyproject.toml: `>=3.10,<3.11`)
- Runtime file specifies: python-3.10.13
- Current development environment using: Python 3.12.1 (will need to be downgraded on deployment)

## Dependencies
From requirements.txt:
```
python-dotenv==1.0.1
python-telegram-bot==13.15
psycopg2-binary==2.9.5
SQLAlchemy==2.0.15
pymysql
anthropic
mistralai
openai
```

## Critical Import Patterns
From examining bot.py and the python-telegram-bot v13.15 documentation:

```python
# Main imports for bot functionality
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

# For defining bot commands and handling updates
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Important note: telegram.ext.Updater is the main class for starting the bot
# Use uppercase for classes (Update, CallbackContext) and lowercase for modules (telegram, telegram.ext)
```

## Bot Structure
- Entry point: `updater = Updater(token=BOT_TOKEN, use_context=True)`
- Dispatcher: `dp = updater.dispatcher`
- Command registration: `dp.add_handler(CommandHandler("command", function))`
- Starting bot: `updater.start_polling()` and `updater.idle()`

## Command Handler Pattern
```python
def command_name(update, context):
    """Handles the /command_name command"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Response message")
```

## Environment Variables
- TELEGRAM_BOT_TOKEN - Required for bot authentication

## Notes on Version Specifics
- python-telegram-bot v13.15 uses the old-style handlers with `update` and `context` parameters
- This version requires `use_context=True` in the Updater constructor
- The project does NOT use the newer v20+ API which has different import patterns and async-based handlers

## Important Commit Reference
- Commit [b7745ae](https://github.com/dobe4ever/better-u-bot/commit/b7745ae) - "Downgrade Python to 3.10 for compatibility"
- This commit establishes the working configuration that resolved previous compatibility issues

## Railway Deployment Configuration
```json
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "python -m pip install --upgrade pip && pip install -r requirements.txt"
  },
  "nixpacks": {
    "python": {
      "version": "3.10"
    }
  },
  "deploy": {
    "runtime": "V2",
    "numReplicas": 1,
    "startCommand": "python bot.py",
    "sleepApplication": true,
    "multiRegionConfig": {
      "us-west1": {
        "numReplicas": 1
      }
    },
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```