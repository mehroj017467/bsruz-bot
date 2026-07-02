import os
import asyncio
import threading
import pandas as pd
import requests
from http.server import HTTPServer, SimpleHTTPRequestHandler
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Bot tokeni
TOKEN = '8908099059:AAHgf-KtimF4hqhrkfaNCqcaWBOuxHoqBlc'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Google Sheets linki
SHEET_URL = "https://docs.google.com/spreadsheets/d/1IF1AWRYPkUUPQaK9fPm2rUBCqK5oTo6BdLXARTk1bw4/export?format=csv"

# Render uchun server
def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# Ma'lumotlarni yuklovchi funksiya
def get_builds_data():
    try:
        response = requests.get(SHEET_URL)
        response.raise_for_status()
        df = pd.read_csv(pd.io.common.BytesIO(response.content))
        return df
    except Exception as e:
        print(f"Xatolik: {e}")
        return pd.DataFrame()

# Bot komandalari
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Salom! Bot ishga tushdi va Google Sheets dan ma'lumotlarni o'qimoqda.")

# Asosiy funksiya
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
