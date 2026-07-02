import os
import asyncio
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Tokeningiz
TOKEN = '8908099059:AAHgf-KtimF4hqhrkfaNCqcaWBOuxHoqBlc'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Render uchun oddiy server (hech qanday aiohttp kerak emas)
def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Serverni fonda yurgizamiz
threading.Thread(target=run_server, daemon=True).start()

# Bot komandalari
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Salom! Bot 24/7 rejimda ishlamoqda.")

# Asosiy funksiya
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
