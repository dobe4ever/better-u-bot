import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

# Telegram
BOT_TOKEN = os.environ("TELEGRAM_BOT_TOKEN")

def start(update):
    # user = add_user(update.effective_user)
    update.message.reply_text("I'm alive motherfucker! What you want?")

def help_command(update):
    update.message.reply_text("Help!")


def echo(update):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    logging.info("Bot fucking started!")

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == "__main__":
    main()