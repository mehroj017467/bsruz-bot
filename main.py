import os
import asyncio
import nest_asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Siz bergan token
TOKEN = '8908099059:AAHgf-KtimF4hqhrkfaNCqcaWBOuxHoqBlc'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Render "Failed" demasligi uchun yengil veb-server
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    # Render PORT ni avtomatik beradi, bo'lmasa 8080 ishlatiladi
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

# Bot komandalari (boshqa kodlaringizni shu yerga qo'shishingiz mumkin)
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Salom! Bot 24/7 rejimda ishga tushdi!")

# Asosiy ishga tushirish
async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
  
