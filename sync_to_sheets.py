import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# Авторизация через credentials.json
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Открываем нужный Google Sheet
spreadsheet = client.open("inkazan_tg_sheet")   # Название файла в Google Sheets
worksheet = spreadsheet.worksheet("inkazan")  # Название листа (вкладки)

# Загружаем актуальные данные из CSV
df = pd.read_csv("telegram_posts_history.csv", parse_dates=['date'])

# Заливаем в Google Sheet
set_with_dataframe(worksheet, df, include_index=False, resize=True)

print("✅ Google Sheet обновлён по данным из telegram_posts_history.csv")
