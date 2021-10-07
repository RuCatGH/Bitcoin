import logging
from typing import Text
from aiogram import Bot, Dispatcher, executor, types
import config
import requests
import json
from aiogram.dispatcher.filters import Text

# Делаем запрос на получение цены биткоина
response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd').text
bitcoinjson = json.loads(response)
pricebitcoin = bitcoinjson["bitcoin"]["usd"]

# Объект бота
bot = Bot(config.token)

# Диспетчер для бота
dp = Dispatcher(bot)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Хэндлер на команду /price
@dp.message_handler(commands="price")
async def priceb(message: types.Message):
    await message.answer(f"Цена биткоина = {pricebitcoin}")

@dp.message_handler(Text(equals = 'будильник', ignore_case = True))
async def alarm(message: types.Message):
    await message.answer(message.text)
    


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
