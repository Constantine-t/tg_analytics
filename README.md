# Telegram Channel Analytics Pipeline  

**For Python 3.9+**

An automated system for extracting, updating, and synchronizing Telegram channel posts for further analysis in Google Sheets and Yandex DataLens.

[Read in Russian](#пайплайн-аналитики-телеграм-канала)

---

##  Project Overview

This project automates the collection and updating of Telegram channel data, ensuring timely analytical reports and dashboards.

---

##  Features

### Scripts

| Script | Description |
|--------|-------------|
| **`main.py`** | Extracts the complete post history starting from a specified date (default is 01.01.2024). Batch loading of 250 messages with delays to prevent rate-limit issues. |
| **`update_last_10.py`** | Updates the last 250 posts by adding new messages and updating existing ones in a CSV file. |
| **`sync_to_sheets.py`** | Uploads the latest CSV data to Google Sheets via a service account. |

---

##  Project Structure

```
telegram-analytics/
├── .env                        # Environment variables (secrets and API keys)
├── credentials.json            # Google Sheets API credentials (service account)
├── main.py                     # Main script to extract all posts
├── update_last_10.py           # Script for updating recent posts
├── sync_to_sheets.py           # Script for synchronization with Google Sheets
├── telegram_posts_history.csv  # Telegram posts data
├── .gitignore                  # List of ignored files
├── README.md                   # Project description
└── requirements.txt            # Python dependencies
```

---

##  Technical Details

- **Telegram API**: Utilizes the Telethon library.
- **Python**: Uses Pandas and asyncio for asynchronous operations.
- **Google Sheets API**: Authorized via a service account.

---

##  Installation

### 1. Clone Repository
```bash
git clone <your-repository-url>
cd telegram-analytics
```

### 2. Set up Virtual Environment and Install Dependencies
```bash
python -m venv env
source env/bin/activate  # Linux/macOS
.\env\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:
```env
TG_API_ID=your_api_id
TG_API_HASH=your_api_hash
CHANNEL_ID=your_channel_id
```

### 4. Configure Google Sheets
- Place your `credentials.json` file in the project's root directory.
- Create a Google Sheet with a specific name and sheet.

---

##  Usage

### Full Extraction of Posts
```bash
python main.py
```

### Updating Recent Posts
```bash
python update_last_10.py
```

### Synchronizing with Google Sheets
```bash
python sync_to_sheets.py
```

---

##  Automating Execution

It's recommended to use Cron (Linux) or Task Scheduler (Windows) to regularly update data:

Example cron job (every 30 minutes):

```bash
*/30 * * * * /path/to/env/bin/python /path/to/project/update_last_10.py
*/30 * * * * /path/to/env/bin/python /path/to/project/sync_to_sheets.py
```

---

##  Ignored Files

Files listed in `.gitignore` contain sensitive data and must not be uploaded to the repository (e.g., API keys, session files, Google Sheets configurations).

---

##  Future Improvements
- Implement automatic alerts based on key metric changes.
- Extend analytical capabilities using DataLens.
- Enhance error handling and logging.

# Пайплайн аналитики телеграм канала 

**Необходим Python 3.9 и выше**

Автоматическая система выгрузки, обновления и синхронизации постов Telegram-канала для последующего анализа в Google Sheets и Yandex DataLens.

---

##  Описание проекта

Проект автоматизирует сбор и обновление данных из Telegram-канала, обеспечивая актуальность аналитических отчётов и дашбордов.

---

##  Функционал

### Скрипты

| Скрипт | Описание |
|--------|-----------|
| **`main.py`** | Полная выгрузка истории постов, начиная с указанной даты (по умолчанию 01.01.2024). Использует пакетную загрузку по 250 сообщений с задержками для избежания rate-limit. |
| **`update_last_10.py`** | Обновляет последние 250 постов: добавляет новые и обновляет существующие посты в CSV-файле. |
| **`sync_to_sheets.py`** | Загружает актуальный CSV-файл в Google Sheets через сервисный аккаунт. |

---

##  Структура проекта

```
telegram-analytics/
├── .env                    # Переменные окружения (секреты и API-ключи)
├── credentials.json        # Доступ к Google Sheets API (сервисный аккаунт)
├── main.py                 # Основной скрипт выгрузки всех постов
├── update_last_10.py       # Скрипт обновления последних постов
├── sync_to_sheets.py       # Скрипт синхронизации с Google Sheets
├── telegram_posts_history.csv  # Данные постов Telegram
├── .gitignore              # Список игнорируемых файлов
├── README.md               # Описание проекта
└── requirements.txt        # Зависимости Python
```

---

##  Технические детали

- **Telegram API**: используется библиотека Telethon.
- **Python**: Pandas, asyncio для асинхронной работы.
- **Google Sheets API**: авторизация через сервисный аккаунт.

---

##  Установка

### 1. Клонирование репозитория
```bash
git clone <your-repository-url>
cd telegram-analytics
```

### 2. Создание виртуального окружения и установка зависимостей
```bash
python -m venv env
source env/bin/activate  # для Linux/macOS
.\env\Scripts\activate   # для Windows
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Создайте файл `.env`:
```env
TG_API_ID=ваш_api_id
TG_API_HASH=ваш_api_hash
CHANNEL_ID=ваш_channel_id
```

### 4. Настройка Google Sheets
- Поместите файл `credentials.json` в корень проекта.
- Создайте таблицу Google Sheets с нужным именем и листом.

---

##  Запуск

### Полная выгрузка постов
```bash
python main.py
```

### Обновление последних постов
```bash
python update_last_10.py
```

### Синхронизация с Google Sheets
```bash
python sync_to_sheets.py
```

---

##  Автоматизация запуска

Рекомендуется использовать Cron (Linux) или Планировщик заданий (Windows) для регулярного обновления данных:

Пример cron-задачи (каждые 30 минут):

```bash
*/30 * * * * /path/to/env/bin/python /path/to/project/update_last_10.py
*/30 * * * * /path/to/env/bin/python /path/to/project/sync_to_sheets.py
```

---

##  Игнорируемые файлы

Файлы, указанные в `.gitignore`, содержат чувствительные данные и не должны загружаться в репозиторий (например, API-ключи, сессии, конфиги Google Sheets).

---

##  Будущие улучшения
- Внедрение автоматических алертов при изменении ключевых метрик.
- Расширение аналитических возможностей с помощью DataLens.
- Улучшение обработки ошибок и логирования.
