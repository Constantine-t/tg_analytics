import os
import asyncio
from datetime import datetime, timezone
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import MessageService
import pandas as pd

# Загрузка переменных окружения
load_dotenv()

# Проверка обязательных переменных
required_vars = ['TG_API_ID', 'TG_API_HASH', 'CHANNEL_ID']
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"❌ Переменная {var} отсутствует в .env")

api_id = int(os.getenv('TG_API_ID'))
api_hash = os.getenv('TG_API_HASH')
session_name = os.getenv('TG_SESSION', 'tg_session')
channel_id = int(os.getenv('CHANNEL_ID'))

# Константы
START_DATE = datetime(2024, 1, 1, tzinfo=timezone.utc)
BATCH_SIZE = 150
SLEEP_SECONDS = 2

client = TelegramClient(session_name, api_id, api_hash)
all_data = []

async def fetch_posts():
    await client.start()
    print("✅ Подключение к Telegram")
    
    try:
        channel = await client.get_entity(channel_id)
    except Exception as e:
        print(f"❌ Ошибка доступа к каналу: {e}")
        return

    offset_id = 0
    total_messages = 0

    while True:
        messages = []
        async for msg in client.iter_messages(channel, limit=BATCH_SIZE, offset_id=offset_id):
            if isinstance(msg, MessageService) or not msg.date:
                continue
            if msg.date < START_DATE:
                print(f"🏁 Достигнута стартовая дата {START_DATE} — завершение")
                return
            messages.append(msg)

        if not messages:
            break

        for message in messages:
            data = {
                'date': message.date,
                'message_id': message.id,
                'text': message.text[:1000] if message.text else '',
                'views': getattr(message, 'views', 0),
                'forwards': getattr(message, 'forwards', 0),
                'comments': message.replies.replies if message.replies else 0,
                'reactions': {r.reaction.emoticon: r.count for r in message.reactions.results} if message.reactions else {},
                'post_link': f"https://t.me/c/{str(channel_id).replace('-100', '')}/{message.id}"
            }
            all_data.append(data)

        total_messages += len(messages)
        offset_id = messages[-1].id  # ID последнего сообщения
        print(f"📦 Получено {total_messages} сообщений. Ждем {SLEEP_SECONDS} сек.")
        await asyncio.sleep(SLEEP_SECONDS)

# Запуск
with client:
    client.loop.run_until_complete(fetch_posts())

# Сохраняем
if all_data:
    df = pd.DataFrame(all_data)
    print(df.head())
    df.to_csv('telegram_posts_history.csv', index=False)
    print("✅ Сохранено в telegram_posts_history.csv")
else:
    print("⚠️ Нет данных для сохранения")
