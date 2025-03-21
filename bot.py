import os
from telegram.ext import Updater, CommandHandler

 # Use this format. DO NOT EDIT!
token = os.environ['TELEGRAM_BOT_TOKEN']

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey hot stuff! I'm your digital bae. What's cookin'?")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Help!")

def main():
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()


