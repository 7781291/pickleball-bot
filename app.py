import os
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
import uvicorn

# Получаем токен и URL из настроек Render
TOKEN = os.getenv("BOT_TOKEN", "8841704204:AAGCcvHLy53c4r4e2wWRzhbBW_LUMpwjmgg")
APP_URL = os.getenv("RENDER_EXTERNAL_URL", "")

bot = Bot(token=TOKEN)
dp = Dispatcher()
app = FastAPI()

# Реакция бота на /start
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    web_app_url = APP_URL if APP_URL else "https://example.com"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏓 Открыть турнир", web_app=WebAppInfo(url=web_app_url))]
        ]
    )
    await message.answer(
        "Привет! Добро пожаловать в турнирный бот по пиклболу 🏓\n\n"
        "Нажмите кнопку ниже, чтобы открыть приложение:",
        reply_markup=keyboard
    )

# Веб-страница (Mini App интерфейс)
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pickleball Tournament</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            body { font-family: sans-serif; background: #1c1c1e; color: #fff; text-align: center; padding: 20px; }
            .btn { background: #007aff; color: white; border: none; padding: 12px 20px; border-radius: 10px; font-size: 16px; margin: 10px; cursor: pointer; }
            .card { background: #2c2c2e; padding: 15px; border-radius: 12px; margin-top: 15px; }
        </style>
    </head>
    <body>
        <h2>🏓 Управление Турниром</h2>
        <p>Выберите формат турнира:</p>
        
        <div class="card"><button class="btn" onclick="alert('Формат Americano выбран!')">Americano</button></div>
        <div class="card"><button class="btn" onclick="alert('Формат Mexicana выбран!')">Mexicana</button></div>
        <div class="card"><button class="btn" onclick="alert('Формат Король Корта выбран!')">Король корта (Лесенка)</button></div>
        <div class="card"><button class="btn" onclick="alert('Формат Round Robin выбран!')">Round Robin</button></div>

        <script>
            Telegram.WebApp.ready();
            Telegram.WebApp.expand();
        </script>
    </body>
    </html>
    """

# Фоновый запуск бота вместе с веб-сервером
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(dp.start_polling(bot))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
