# ⚠️ IMPORTANT PROJECT SPECS: 


## Important Commit Reference
- Commit [4de5fa4](https://github.com/dobe4ever/better-u-bot/commit/4de5fa4) 
- This commit contains the definitive reference documentation & the bot runs with zero conflics in railway production.

## Python Version
```python
- **ACTUAL DEPLOYED VERSION**: Python 3.11 (used by Railway in production)
- Runtime file specifies: python-3.11

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

## Exact dependency versions that work
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

## Environment Variables in Railway

Railway automatically provides to all builds and deployments:

### System Variables
- `RAILWAY_PRIVATE_DOMAIN`
- `RAILWAY_TCP_PROXY_DOMAIN`
- `RAILWAY_TCP_PROXY_PORT`
- `RAILWAY_TCP_APPLICATION_PORT`
- `RAILWAY_PROJECT_NAME`
- `RAILWAY_ENVIRONMENT_NAME`
- `RAILWAY_SERVICE_NAME`
- `RAILWAY_PROJECT_ID`
- `RAILWAY_ENVIRONMENT_ID`
- `RAILWAY_SERVICE_ID`
- `RAILWAY_VOLUME_ID`
- `RAILWAY_VOLUME_NAME`
- `RAILWAY_VOLUME_MOUNT_PATH`
- `RAILWAY_DEPLOYMENT_DRAINING_SECONDS`

### PostgreSQL Variables
- `DATABASE_URL`
- `DATABASE_PUBLIC_URL`
- `PGDATA`
- `PGDATABASE`
- `PGHOST`
- `PGPASSWORD`
- `PGPORT`
- `PGUSER`
- `POSTGRES_DB`
- `POSTGRES_PASSWORD`
- `POSTGRES_USER`
- `SSL_CERT_DAYS`

### Custom Variables
- `ANTHROPIC_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `MISTRAL_API_KEY`
- `DEEPSEEK_API_KEY`
- `OPENAI_API_KEY`

___

```python
# Python - CORRECT for Railway
import os
api_key = os.environ['API_KEY']  # USE THIS FORMAT!
# NOT THESE:
# api_key = os.getenv('API_KEY')
# api_key = os.environ.get('API_KEY')
```
## Notes on Version Specifics
- python-telegram-bot v13.15 uses the old-style handlers with `update` and `context` parameters
- This version requires `use_context=True` in the Updater constructor
- The project does NOT use the newer v20+ API which has different import patterns and async-based handlers

## Code example

```python
# Main imports for bot functionality
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

## Command Handler Pattern
```python
def command_name(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Response message")
```