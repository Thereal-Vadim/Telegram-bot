import asyncio
import aiohttp
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

API_KEY = "your_openweathermap_api_key"
DEFAULT_CITY = "Moscow"
INTERVALS = ["08:00", "14:00", "20:00"]

bot = Bot(token="token")
dp = Dispatcher()

async def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_wether}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                temp = data['main']['temp']
                weather_desc = data['weather'][0]['description']
                return f"Current weather in {city}: {temp}°C, {weather_desc}"
            else:
                return "City not found. Please try again."

async def send_weather():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in INTERVALS:
            weather_report = await get_weather(DEFAULT_CITY)
            await bot.send_message(chat_id="YOUR_CHAT_ID", text=weather_report)
        await asyncio.sleep(60)

@dp.message(Command("weather"))
async def weather_command(message: Message):
    city = message.text.split(" ", 1)
    if len(city) > 1:
        weather_report = await get_weather(city[1])
    else:
        weather_report = await get_weather(DEFAULT_CITY)
    await message.answer(weather_report)

@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer('This bot can provide weather updates: \n /start \n /help \n /weather [city]')

@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer('Hello! Use /weather [city] to get the current forecast.')

async def main():
    asyncio.create_task(send_weather())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
