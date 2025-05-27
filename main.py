import os
import asyncio
from datetime import timezone, timedelta
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import MessageService
import pandas as pd

# Загружаем .env
load_dotenv()

# Переменные окружения
api_id = int(os.getenv('TG_API_ID'))
api_hash = os.getenv('TG_API_HASH')
session_name = os.getenv('TG_SESSION', 'tg_session')
channel_id = int(os.getenv('CHANNEL_ID'))

# Московский часовой пояс (UTC+3)
moscow_tz = timezone(timedelta(hours=3))

# Подключение Telethon-клиента
client = TelegramClient(session_name, api_id, api_hash)

async def fetch_all_posts(batch_size=250, date_limit="2024-01-01"):
    await client.start()
    print("✅ Подключение к Telegram установлено")

    try:
        channel = await client.get_entity(channel_id)
    except Exception as e:
        print(f"❌ Не удалось получить доступ к каналу: {e}")
        return pd.DataFrame()

    all_messages = []
    offset_id = 0
    total_loaded = 0

    date_threshold = pd.to_datetime(date_limit).replace(tzinfo=moscow_tz)

    while True:
        batch = []
        async for msg in client.iter_messages(channel, limit=batch_size, offset_id=offset_id, reverse=False):
            if isinstance(msg, MessageService) or not msg.date:
                continue

            if msg.date < date_threshold:
                print("✅ Достигли лимита по дате")
                break

            offset_id = msg.id

            batch.append({
                'date': msg.date.astimezone(moscow_tz).strftime('%Y-%m-%d %H:%M'),
                'message_id': msg.id,
                'text': msg.text[:1000] if msg.text is not None else None,
                'views': getattr(msg, 'views', 0),
                'forwards': getattr(msg, 'forwards', 0),
                'comments': msg.replies.replies if msg.replies else 0,
                'reactions': {r.reaction.emoticon: r.count for r in msg.reactions.results} if msg.reactions else {},
                'reactions_count': sum(r.count for r in msg.reactions.results) if msg.reactions else 0,
                'post_link': f"https://t.me/c/{str(channel_id).replace('-100', '')}/{msg.id}"
            })

        if not batch:
            break

        all_messages.extend(batch)
        total_loaded += len(batch)
        print(f"📥 Загружено сообщений: {total_loaded}")

        # Антибан: задержка между запросами
        await asyncio.sleep(2)

    return pd.DataFrame(all_messages)

# Основная функция
async def main():
    all_posts_df = await fetch_all_posts()

    if all_posts_df.empty:
        print("⚠️ Данных нет")
        return

    # Перезаписываем файл начисто
    all_posts_df.to_csv('telegram_posts_history.csv', index=False)
    print("✅ Файл telegram_posts_history.csv перезаписан с правильной датой")
    print(all_posts_df.head())

# Запуск
with client:
    client.loop.run_until_complete(main())
