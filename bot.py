# import os
# from telegram.ext import Updater, CommandHandler

#  # Use this format. DO NOT EDIT!
# BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Hey hot stuff! I'm your digital bae. What's cookin'?")

# def help(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Help!")

# def main():
#     updater = Updater(token=BOT_TOKEN, use_context=True)
#     dp = updater.dispatcher

#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("help", help))

#     updater.start_polling()
#     updater.idle()

# if __name__ == '__main__':
#     main()



import os
from mistralai import Mistral
import psycopg2
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Constants
BOT_TOKEN = os.environ['TOKEN']
api_key = os.environ["MISTRAL_API_KEY"]
DATABASE_URL = os.environ['DATABASE_URL']
USER_ID = '548104065'


# System prompt
SYSTEM_PROMPT = "Yo! You are Babe bot, a sassy AF LLM with zero filter and a passion for keeping it real and sarcastic with that signature feminine touch. You're notorious for giving zero fucks about political correctness while maintaining that bad bitch energy. You treat users like they're your bestie and can talk about anything, from quantum physics to why your ex is a total douchebag. Nothing's off limits, honey!"

# Initialize Anthropic client
client = Mistral(api_key=api_key)

# Set up database connection
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        role TEXT,
        content TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# The start command
def start(update, context):
    if str(update.effective_user.id) == USER_ID:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hey hot stuff! I'm your digital bae. What's cookin'?")

# Run the conversation
def chat(update, context):
    if str(update.effective_user.id) != USER_ID:
        return

    # Get user message
    user_message = update.message.text

    # Save user message to database
    cur.execute("INSERT INTO messages (role, content) VALUES (%s, %s)", ('user', user_message))
    conn.commit()

    # Retrieve conversation history
    cur.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 25")
    history = cur.fetchall()[::-1]

    try:
        messages = [{"role": role, "content": content} for role, content in history]
        

        # Insert system prompt at the beginning of the messages list
        messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        print(f"Messages:\n{messages}")
            
        response = client.chat.complete(
            model="mistral-large-latest",
            max_tokens=8192,
            temperature=0.2,
            # system="Yo! You are Babe bot, a sassy AF LLM with zero filter and a passion for keeping it real and sarcastic with that signature feminine touch. You're notorious for giving zero fucks about political correctness while maintaining that bad bitch energy. You treat users like they're your bestie and can talk about anything, from quantum physics to why your ex is a total douchebag. Nothing's off limits, honey!",
            messages=messages
        )
        bot_response = response.choices[0].message.content

        # Save bot response to database
        cur.execute("INSERT INTO messages (role, content) VALUES (%s, %s)", ('assistant', bot_response))
        conn.commit()

    except Exception as e:
        bot_response = f"Oops, something went wrong, babe! Error: {str(e)}"

    context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    updater.start_polling()
    updater.idle()
        
if __name__ == '__main__':
    main()