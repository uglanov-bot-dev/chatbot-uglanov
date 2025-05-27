from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Bot is alive"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
import os
import openai
import telegram
from telegram.ext import Updater, MessageHandler, Filters

openai.api_key = os.getenv("OPENAI_API_KEY")
bot_token = os.getenv("BOT_TOKEN")

def handle_message(update, context):
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )
    reply = response.choices[0].message.content
    update.message.reply_text(reply)

if __name__ == "__main__":
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()
