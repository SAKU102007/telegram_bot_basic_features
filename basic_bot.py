from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InputFile, MediaGroup, \
    ContentType, ChatActions, ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from random import randint
import asyncio
import os
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


HELP_TEXT = '''
/help - список команд
/start - запуск бота
/clear - очистить историю чата
/sticker - отправить стикер
/photo - отправить фото
/video - отправить видео
/group - отправить видеогруппу
/note - отправить видео-кружок

/create_keyboard - создать клавиатуру
/delete_keyboard - удалить клавиатуру

/inline - инлайн клавиутура
'''



keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_remove = ReplyKeyboardRemove()

btn1 = KeyboardButton(text='/photo')
btn2 = KeyboardButton(text='/note')
btn3 = KeyboardButton(text='/video')
btn4 = KeyboardButton(text='/help')

keyboard.add(btn1, btn2).add(btn3, btn4)



messages = {}


def append_messages(message):
    messages.setdefault(message.chat.id, []).append(message)


def count_all_messages(messages):
    all_messages = 0
    for key, value in messages.items():
        all_messages += len(value)
    return all_messages



@dp.message_handler(commands=["create_keyboard"])
async def create_keyboard(message: types.Message):
    append_messages(message)
    reply = await bot.send_message(message.chat.id, text='Клавиатура создана', reply_markup=keyboard)
    append_messages(reply)


@dp.message_handler(commands=["delete_keyboard"])
async def delete_keyboard(message: types.Message):
    append_messages(message)
    reply = await bot.send_message(message.chat.id, text='Клавиатура удалена', reply_markup=keyboard_remove)
    append_messages(reply)


@dp.message_handler(commands=["inline"])
async def inline_keyboard_command(message: types.Message):
    append_messages(message)
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    i_btn1 = InlineKeyboardButton(text='Сайт Месси', url='https://messi.com/')
    i_btn2 = InlineKeyboardButton(text='Генерация случайного числа', callback_data='random_value')
    inline_keyboard.add(i_btn1, i_btn2)
    reply = await bot.send_message(message.chat.id, text='Выберите кнопку:', reply_markup=inline_keyboard)
    append_messages(reply)


@dp.callback_query_handler(text_contains='random_value')
async def send_random_value(callback: CallbackQuery):
    random_value = randint(0, 100)
    reply = await bot.send_message(callback.message.chat.id, text=f'{random_value}')
    append_messages(reply)
    await callback.answer(text=f'{random_value}')



@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    append_messages(message)
    reply = await message.answer(HELP_TEXT)
    append_messages(reply)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    append_messages(message)
    reply = await bot.send_message(message.chat.id, text='Здарова бро!⚽️')
    append_messages(reply)


@dp.message_handler(commands=["sticker"])
async def sticker_command(message: types.Message):
    append_messages(message)
    sticker_id = 'CAACAgIAAxkBAAERdn1qQFBw672sYuyjCR8VAa1553n_4gACaWsAAmBeIUjhlv71-J_a4TwE'
    reply = await bot.send_sticker(message.chat.id, sticker_id)
    reply.text = f'Стикер с id = {sticker_id}'
    append_messages(reply)


@dp.message_handler(commands=["photo"])
async def photo_command(message: types.Message):
    append_messages(message)
    photo = InputFile('messi.jpg')
    reply = await bot.send_photo(message.chat.id, photo=photo, caption='Лионель Местный')
    reply.text = f'Фото с названием = {photo.filename}'
    append_messages(reply)


@dp.message_handler(commands=["video"])
async def video_command(message: types.Message):
    append_messages(message)
    video = InputFile('messi.mp4')
    reply = await bot.send_video(message.chat.id, video=video, caption='Видео из дзена про Месси')
    reply.text = f'Видео с названием = {video.filename}'
    append_messages(reply)


@dp.message_handler(commands=["group"])
async def group_command(message: types.Message):
    append_messages(message)
    media = MediaGroup()
    media.attach_photo(InputFile('messi.jpg'),  caption='Изображение')
    media.attach_video(InputFile('messi.mp4') ,  caption='Видео')
    reply = await bot.send_media_group(message.chat.id, media=media)
    for media_item in reply:
        media_item.text = f'Медиаэлемент с типом = {media_item.caption}'
        append_messages(media_item)


@dp.message_handler(commands=["note"])
async def note_command(message: types.Message):
    append_messages(message)
    video = InputFile('messi_video_note.mp4')
    await bot.send_chat_action(message.chat.id, ChatActions.RECORD_VIDEO_NOTE)
    await asyncio.sleep(1.5)
    await bot.send_chat_action(message.chat.id, ChatActions.UPLOAD_VIDEO_NOTE)
    await asyncio.sleep(1.5)
    reply = await bot.send_video_note(message.chat.id, video_note=video)
    reply.text = f'Видео-кружочек с названием = {video.filename}'
    append_messages(reply)


@dp.message_handler(commands=["clear"])
async def clear_command(message: types.Message):
    append_messages(message)
    previous_number_of_messages = count_all_messages(messages)
    messages_for_this_chat = messages.get(message.chat.id, [])
    for message in messages_for_this_chat:
        print(message.text, end='\n\n')
        await bot.delete_message(message.chat.id, message.message_id)
        await asyncio.sleep(0.05)
    del messages[message.chat.id]
    current_number_of_messages = count_all_messages(messages)
    print(f'Было сообщений: {previous_number_of_messages}\n'
          f'Стало сообщений: {current_number_of_messages}\n'
          f'Удалено сообщений: {previous_number_of_messages - current_number_of_messages}\n')


async def clear_all_chats():
    pass
    previous_number_of_messages = count_all_messages(messages)
    chats = []
    for msg_list in messages.values():
        chats.append(msg_list)
    for chat in chats:
        temp = chat[0].chat.id
        for message in chat:
            print(message.text, end='\n\n')
            await bot.delete_message(message.chat.id, message.message_id)
            await asyncio.sleep(0.05)
        del messages[temp]
    current_number_of_messages = count_all_messages(messages)
    print(f'Было сообщений: {previous_number_of_messages}\n'
          f'Стало сообщений: {current_number_of_messages}\n'
          f'Удалено сообщений: {previous_number_of_messages - current_number_of_messages}\n')


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message: types.Message):
    append_messages(message)
    reply = await message.reply("Я не шарю что тебе сказать даже на это(\nПопробуй /help юзануть что-ли)")
    append_messages(reply)


async def on_startup(_):
    print('Бот был перезапущен!\n')

async def on_shutdown(_):
    print("Бот останавливается. Удаляю все отправленные сообщения...")
    await clear_all_chats()
    print("Готово.")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
