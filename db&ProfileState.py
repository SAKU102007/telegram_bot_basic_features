from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from state_db import db_start, create_profile, edit_profile
import os
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class ProfileStates(StatesGroup):
    name = State()
    age = State()
    description = State()
    photo = State()


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer('Здарова бро!⚽️\nДля заполнения анкеты введи команду /create')
    await create_profile(user_id=message.from_user.id)


@dp.message_handler(commands=["cancel"], state='*')
async def cancel_command(message: types.Message, state: FSMContext):
    if state is None:
        return

    await state.finish()
    await message.reply('Ты прервал заполнение анкеты(')


@dp.message_handler(commands=["create"])
async def create_command(message: types.Message):
    await message.answer('Пришли своё имя')
    await ProfileStates.name.set()


@dp.message_handler(state=ProfileStates.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer('Введи свой возраст')
    await ProfileStates.next()


@dp.message_handler(lambda message: not message.text.isdigit(), state=ProfileStates.age)
async def checking_input_age(message: types.Message):
    return await message.reply("ТЫ ввел не число!")


@dp.message_handler(state=ProfileStates.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    await message.answer('Расскажи что-нибудь про себя')
    await ProfileStates.next()


@dp.message_handler(state=ProfileStates.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await message.answer('Добавь свое фото')
    await ProfileStates.next()


@dp.message_handler(lambda message: not message.photo, state=ProfileStates.photo)
async def checking_input_photo(message: types.Message):
    return await message.reply("ТЫ отправил не фото!")


@dp.message_handler(content_types=['photo'],state=ProfileStates.photo)
async def process_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await bot.send_photo(message.chat.id, photo=data['photo'],
                             caption=f"{data['name']}, {data['age']}\n{data['description']}")

    await edit_profile(state=state, user_id=message.from_user.id)
    await message.answer('Твоя анкета успешно создана!)')
    await state.finish()


async def on_startup(_):
    await db_start()
    print('Подключение к базе данных выполнено успешно!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
