# Project Configuration

This document captures the exact configuration of the Better-U-Bot project to ensure reproducibility and avoid dependency conflicts.

## Python Version
- **ACTUAL DEPLOYED VERSION**: Python 3.11 (used by Railway in production)
- Runtime file specifies: python-3.11
- Local development environment using: Python 3.12.1

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

## Railway Installed Packages
```
Successfully installed APScheduler-3.6.3 CFFI-1.17.1 SQLAlchemy-2.0.15 
annotated-types-0.7.0 anthropic-0.49.0 anyio-4.9.0 cachetools-4.2.2 
certifi-2025.1.31 distro-1.9.0 eval-type-backport-0.2.2 greenlet-3.1.1 
h11-0.14.0 httpcore-1.0.7 httpx-0.28.1 idna-3.10 jiter-0.9.0 
jsonpath-python-1.0.6 mistralai-1.5.2 mypy-extensions-1.0.0 numpy-2.2.4 
openai-1.68.0 psycopg2-binary-2.9.5 pycparser-2.22 pydantic-2.10.6 
pydantic-core-2.27.2 pymysql-1.1.1 python-dateutil-2.9.0.post0 
python-dotenv-1.0.1 python-telegram-bot-13.15 pytz-2025.1 six-1.17.0 
sniffio-1.3.1 sounddevice-0.5.1 tornado-6.1 tqdm-4.67.1 
typing-extensions-4.12.2 typing-inspect-0.9.0 tzlocal-5.3.1
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
- Commit [4de5fa4](https://github.com/dobe4ever/better-u-bot/commit/4de5fa4) - "Add comprehensive configuration documentation and telegram bot reference"
- This commit contains the definitive reference documentation for the project's configuration

## Railway Deployment Configuration
The actual Railway deployment uses:

```
Nixpacks v1.34.1
setup: python311, postgresql_16.dev, gcc
install: python -m venv --copies /opt/venv && . /opt/venv/bin/activate && pip install -r requirements.txt
build: python -m pip install --upgrade pip && pip install -r requirements.txt
start: python bot.py
```

Railway JSON configuration:
```json
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "python -m pip install --upgrade pip && pip install -r requirements.txt"
  },
  "nixpacks": {
    "python": {
      "version": "3.11"
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