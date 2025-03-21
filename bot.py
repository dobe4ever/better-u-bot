from telegram.ext import Updater, CommandHandler, CallbackContext, Filters
import os

token = os.environ['TELEGRAM_BOT_TOKEN']  # Use this format. DO NOT EDIT!

# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Hey hot stuff! I'm your digital bae. What's cookin'?")

def start_command(update, context: CallbackContext):
    """Handle the /start command"""
    user = update.effective_user
    update.message.reply_text(f'Hello {user.first_name}!')

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Help!")

def main():
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help))

    updater.start_polling()
    updater.idle()
 
if __name__ == '__main__':
    main()