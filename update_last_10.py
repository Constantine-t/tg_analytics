import os
import asyncio
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

# Подключение Telethon-клиента
client = TelegramClient(session_name, api_id, api_hash)


async def fetch_last_posts(limit=200):
    await client.start()
    print("✅ Подключение к Telegram установлено")

    try:
        channel = await client.get_entity(channel_id)
    except Exception as e:
        print(f"❌ Не удалось получить доступ к каналу: {e}")
        return pd.DataFrame()

    messages = []
    async for msg in client.iter_messages(channel, limit=limit, reverse=False):  # От нового к старому
        if isinstance(msg, MessageService) or not msg.date:
            continue

        data = {
            'date': msg.date,
            'message_id': msg.id,
            'text': msg.text[:1000] if msg.text else '',
            'views': getattr(msg, 'views', 0),
            'forwards': getattr(msg, 'forwards', 0),
            'comments': msg.replies.replies if msg.replies else 0,
            'reactions': {r.reaction.emoticon: r.count for r in msg.reactions.results} if msg.reactions else {},
            'reactions_count': sum(r.count for r in msg.reactions.results) if msg.reactions else 0,
            'post_link': f"https://t.me/c/{str(channel_id).replace('-100', '')}/{msg.id}"
        }
        messages.append(data)

    df = pd.DataFrame(messages)
    df['date'] = pd.to_datetime(df['date'])  # Явно задаём формат даты
    return df


# Основная функция
async def main():
    new_posts_df = await fetch_last_posts()

    if new_posts_df.empty:
        print("⚠️ Новых данных нет")
        return

    # Попытка прочитать старый файл
    try:
        existing_posts_df = pd.read_csv('telegram_posts_history.csv', parse_dates=['date'])
    except FileNotFoundError:
        print("⚠️ Файл telegram_posts_history.csv не найден.")
        existing_posts_df = pd.DataFrame()

    if not existing_posts_df.empty:
        # Объединяем по message_id
        merged_df = pd.concat([
            existing_posts_df.set_index('message_id'),
            new_posts_df.set_index('message_id')
        ])
        merged_df = merged_df[~merged_df.index.duplicated(keep='last')].reset_index()
        print("🔄 Данные успешно обновлены")

        # Подсчёт обновлений
        old_ids = set(existing_posts_df['message_id'])
        new_ids = set(new_posts_df['message_id'])
        new_count = len(new_ids - old_ids)
        updated_count = len(new_ids & old_ids)
        print(f"➕ Добавлено новых постов: {new_count}")
        print(f"♻️ Обновлено существующих: {updated_count}")
    else:
        merged_df = new_posts_df
        print("📥 Создан новый датафрейм с последними постами")

    # Сортируем по дате
    merged_df = merged_df.sort_values('date', ascending=False)

    # (опционально) Удаляем дубли по ссылке, если такое возможно
    merged_df = merged_df.drop_duplicates(subset='post_link', keep='first')

    # Сохраняем
    merged_df.to_csv('telegram_posts_history.csv', index=False)
    print("✅ Файл telegram_posts_history.csv успешно сохранён.")
    print(merged_df.head())


# Запуск кода
with client:
    client.loop.run_until_complete(main())
