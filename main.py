import os
import openai
from flask import Flask, request
import telegram

app = Flask(__name__)

# Инициализация переменных из Railway
TELEGRAM_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Настройка Telegram-бота
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

@app.route('/')
def home():
    return 'Bot is running'

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text

    # Ответ через OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # или "gpt-4", если доступен
            messages=[
                {"role": "user", "content": message_text}
            ]
        )
        reply_text = response['choices'][0]['message']['content']
    except Exception as e:
        reply_text = "Ошибка AI: " + str(e)

    bot.send_message(chat_id=chat_id, text=reply_text)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
