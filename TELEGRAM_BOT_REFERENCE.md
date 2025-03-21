# Python Telegram Bot Reference

Quick reference for python-telegram-bot v13.15 with common patterns and examples.

## Basic Imports

```python
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
```

## Bot Initialization

```python
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Add handlers here
    dp.add_handler(CommandHandler("start", start_command))
    
    # Start the bot
    updater.start_polling()
    updater.idle()
```

## Command Handlers

```python
def start_command(update, context: CallbackContext):
    """Handle the /start command"""
    user = update.effective_user
    update.message.reply_text(f'Hello {user.first_name}!')
```

## Message Handlers

```python
# Handle text messages
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))

def text_handler(update: Update, context: CallbackContext):
    """Handle text messages"""
    text = update.message.text
    update.message.reply_text(f'You said: {text}')
```

## Inline Keyboards

```python
def keyboard_command(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='option1'),
            InlineKeyboardButton("Option 2", callback_data='option2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

# Callback handler for inline keyboard
dp.add_handler(CallbackQueryHandler(button_callback))

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()  # Acknowledge the button press
    
    if query.data == 'option1':
        query.edit_message_text(text="Option 1 selected!")
    elif query.data == 'option2':
        query.edit_message_text(text="Option 2 selected!")
```

## Reply Keyboards

```python
def reply_keyboard_command(update: Update, context: CallbackContext):
    keyboard = [
        ['Option 1', 'Option 2'],
        ['Option 3', 'Option 4']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
```

## Conversation Handlers

```python
# Define states
NAME, AGE = range(2)

def start_conversation(update: Update, context: CallbackContext):
    update.message.reply_text('What is your name?')
    return NAME

def get_name(update: Update, context: CallbackContext):
    user_name = update.message.text
    context.user_data['name'] = user_name
    update.message.reply_text(f'Hello {user_name}! What is your age?')
    return AGE

def get_age(update: Update, context: CallbackContext):
    user_age = update.message.text
    name = context.user_data.get('name', 'Unknown')
    update.message.reply_text(f'Your name is {name} and you are {user_age} years old.')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Conversation cancelled.')
    return ConversationHandler.END

# Create conversation handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('survey', start_conversation)],
    states={
        NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
        AGE: [MessageHandler(Filters.text & ~Filters.command, get_age)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
dp.add_handler(conv_handler)
```

## Sending Media

```python
# Send photo
def send_photo(update: Update, context: CallbackContext):
    update.message.reply_photo(
        photo=open('image.jpg', 'rb'),
        caption='Check out this image!'
    )

# Send document/file
def send_document(update: Update, context: CallbackContext):
    update.message.reply_document(
        document=open('document.pdf', 'rb'),
        caption='Here is your document'
    )
```

## Error Handler

```python
def error_handler(update: Update, context: CallbackContext):
    """Log errors caused by updates."""
    logger.error(f'Update {update} caused error {context.error}')

dp.add_error_handler(error_handler)
```