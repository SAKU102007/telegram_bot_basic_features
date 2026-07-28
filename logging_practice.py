import logging
from aiogram import Bot, Dispatcher, types, executor
import os
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO, filename='bot_info.log')


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    logging.error(f'Ошибка {update}: {exception}')


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer('<b>Здарова бро!⚽️</b>', parse_mode=types.ParseMode.HTML)
    # await message.answer('<b>Здарова бро!⚽️<b/>', parse_mode=types.ParseMode.HTML)
    # Доупщена ошибка: <b/> вместо </b> чтобы проверить заполнение .log файла
    logging.info(f'Пользователь {message.from_user.id} запустил бота')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
