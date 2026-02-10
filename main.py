import os
import time
import schedule
from telegram import Bot
from openai import OpenAI

bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
channel_id = os.environ["CHANNEL_ID"]
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

PROMPT = """
Ты пишешь пост для Telegram-канала "Чувственная Я".
Стиль: чувственный, мягкий, вдохновляющий.
Обращение на "ты".

Создай уникальный пост 800-1200 символов.
Добавь немного эмодзи.
В конце добавь хэштеги.
"""

def generate_post():
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": PROMPT}]
    )
    return response.choices[0].message.content

def post():
    text = generate_post()
    bot.send_message(chat_id=channel_id, text=text)

post()    
schedule.every().day.at("13:00").do(post)
schedule.every().day.at("19:00").do(post)

while True:
    schedule.run_pending()
    time.sleep(30)
