import logging
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import os

# Telegram
BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
bot = Bot(BOT_TOKEN)

def start(update, context):
    bot.send_message(chat_id=update.effective_chat.id, text="Hey hot stuff! I'm your digital bae. What's cookin'?")

def help_command(update, context):
    bot.send_message(chat_id=update.effective_chat.id, text="Help!")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # Start the Bot
    updater.start_polling()

    logging.info("Bot fucking started!")

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == "__main__":
    main()