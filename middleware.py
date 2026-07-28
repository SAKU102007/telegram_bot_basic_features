from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.middlewares import BaseMiddleware
import os
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)



class MyMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, update: types.Update, data:dict):
        print('Сообщение перед апдейтом')
        print(update)

    async def on_process_message(self, update: types.Update, data:dict):
        print('Сообщение во время обработки апдейта')



@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer('Здарова бро!⚽️')


if __name__ == '__main__':
    dp.middleware.setup(MyMiddleware())
    executor.start_polling(dp, skip_updates=True)
