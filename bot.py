from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from requests.api import get
from typing import Text
import asyncio
import logging
import aiohttp
import config
import sqlite3

conn = sqlite3.connect("bd.db") 
cursor = conn.cursor()

async def get_bitcoin_price():
    # Делаем запрос на получение цены биткоина
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd') as response:
            bitcoin = await response.json()
        return int(bitcoin["bitcoin"]["usd"])


# Объект бота
bot = Bot(config.token)

# Диспетчер для бота
dp = Dispatcher(bot)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Хэндлер на команду /price
@dp.message_handler(commands=["price"])
async def priceb(message: types.Message):
    await message.answer(f"Цена биткоина = {await get_bitcoin_price()}")

# Хэндлер на команду /alert для оповещения, когда цена дойдёт 
@dp.message_handler(commands=["alert"])
async def alarm(message: types.Message):
    mean = int(message.text[6:])
    cursor.execute(f'INSERT INTO meanb (meanfield) VALUES ({mean})')
    conn.commit()
    if mean > await get_bitcoin_price():
        while True:
            await asyncio.sleep(3)
            if mean < await get_bitcoin_price():
                await message.answer(f"Цена биткоина пересекла вашу отметку {mean}")
                break
    if mean < await get_bitcoin_price():
        while True:
            await asyncio.sleep(3)
            if mean > await get_bitcoin_price():
                await message.answer(f"Цена биткоина пересекла вашу отметку {mean}")
                break
    while True:
            await asyncio.sleep(3)
            if mean == await get_bitcoin_price():
                await message.answer(f"Цена биткоина пересекла вашу отметку {mean}")
                break


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
