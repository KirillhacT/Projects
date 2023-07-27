from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler

from keyboards import menu_kb, start_kb, ikb, ExitReplay, get_inline_keyboard, cb, ReplyKeyboardMarkup, KeyboardButton
from other.sqlite import db_start, create_profile, edit_profile
import random
from pprint import pprint

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

TOKEN_API = "5330446051:AAEWOOzIukJqBgyI0N5CjRAZv9ooTJaIe5Q"
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())
admin_id = 1390059189

#Middleware

def set_key(key: str = None):
    def decorator(func):
        setattr(func, "key", key)
        return func
    return decorator

class AddminMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        if handler:
            key = getattr(handler, "key", "Такого атрибута нет")
            print(key)


#Машина состояний
class ClientStatesGroup(StatesGroup):
    photo = State()
    desc = State()

def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отмена'))

@dp.message_handler(text="Отмена", state="*")
async def cancel_st(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply("Отменил", reply_markup=menu_kb)
    await state.finish()

@dp.message_handler(text='Создание профиля', state=None)
async def start_st(message: types.Message):
    await ClientStatesGroup.photo.set()
    await message.answer("Отправь фото", reply_markup=get_cancel())

@dp.message_handler(lambda message: not message.photo, state=ClientStatesGroup.photo)
async def check_photo(message: types.Message):
    return await message.reply("Это не фотография!")


@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=ClientStatesGroup.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data: #Получаем доступ к хранилищу состояний
        data['photo'] = message.photo[0].file_id
    await ClientStatesGroup.next()
    await message.reply("Теперь отправь свое имя")

@dp.message_handler(state=ClientStatesGroup.desc)
async def load_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data: #Получаем доступ к хранилищу состояний
        data['desc'] = message.text
    # await ClientStatesGroup.next()
    await edit_profile(state, user_id=message.chat.id)
    await message.reply("Ваш профиль создан")

    # async with state.proxy() as data:
    #     await bot.send_photo(message.chat.id,
    #                          photo=data["photo"],
    #                          caption=data["desc"])
    await state.finish()  # Заканчиваем
# @dp.message_handler(Text("Отмена"), state='*')




# admin_name = "Kirill"
stickerExample = "CAACAgIAAxkBAAEH-7xkAkIVDFgDcNq14QbDzcNY1mB91AACAw4AAkD-yUuLHupAbb8sOC4E"
KB = ExitReplay("Меню")()
number = 0
photos_list = []
with open("photos.txt", encoding='utf-8') as file:
    for i in file:
        photos_list.append(i)
# kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#one_time_keyboard - клавиатура закрывается после первого использования

def send_random_photo():
    random_number = random.randint(0, len(photos_list) - 1)
    return photos_list.pop(random_number)

async def on_startup(_):
    print("Бот был запущен")
    await db_start()

#Функционал бота
@dp.message_handler(commands=['start'])
async def echo(message: types.Message):
    text = "Привет, добро пожаловать в бота"
    await bot.send_sticker(message.from_user.id, sticker=stickerExample)
    await message.answer(text=text, reply_markup=start_kb)
    await create_profile(user_id=message.from_user.id)

@dp.message_handler(Text(equals="Меню"))
@set_key("Hello!")
async def echo(message: types.Message):
    text = "Меню бота: "
    await message.answer(text=text, reply_markup=menu_kb)

# @dp.callback_query_handler(lambda call: call.data.startswith('btn'))
@dp.callback_query_handler(cb.filter())
async def ikb_cd_handler(callback: types.CallbackQuery, callback_data: dict) -> None:
    global number
    if callback_data.get('action') == "btn_+":
        number += 1
        await callback.message.edit_text(f"The current number is {number}", reply_markup=get_inline_keyboard())
    elif callback_data.get('action') == "btn_-":
        number -= 1
        await callback.message.edit_text(f"The current number is {number}", reply_markup=get_inline_keyboard())
    elif callback_data.get('action') == "btn_random":
        number = random.randint(1, 100)
        await callback.message.edit_text(f"The current number is {number}", reply_markup=get_inline_keyboard())

@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == "like":
        await callback.answer(show_alert=True, text="Вам понравилось")
    elif callback.data == "dislike":
        await callback.answer(show_alert=True, text="Вам не понравилось")
    elif callback.data == "dont_like":
        random_photo = send_random_photo()
        await callback.message.edit_media(types.InputMedia(media=random_photo, type="photo"), reply_markup=ikb)
        await callback.answer()
    elif callback.data == "menu":
        await callback.message.delete()
        await callback.message.answer(text="Главное меню", reply_markup=menu_kb)


@dp.message_handler(Text(equals="Помощь"))
async def help(message: types.Message):
    text = "<em>Помощь <b>находится</b> в разработке!</em>😅"
    await message.answer(text=text, parse_mode="HTML")
    await bot.send_location(chat_id=message.chat.id, latitude=55, longitude=10, reply_markup=KB)

@dp.message_handler(Text(equals="Выход"))
async def exit(message: types.Message):
    await bot.send_message(message.chat.id, text="Оривидерчи", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(Text(equals="Отправить фото")) #Будет отправлять в чат, из которого написали
async def send_photo(message: types.Message):
    # await bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Нравится ли тебе эта фотография?", reply_markup=ikb)
    random_photo = send_random_photo()
    await message.answer(text="Рандомная фотка!", reply_markup=ReplyKeyboardRemove())
    await bot.send_photo(message.chat.id, photo=random_photo, reply_markup=ikb)


@dp.message_handler(Text(equals="Счетчик"))
async def gen(message: types.Message):
    await message.answer(f"The current number is {number}", reply_markup=get_inline_keyboard())

# @dp.message_handler()
# async def question(message: types.Message):
#     user = message.from_user.full_name
#     if user != admin_name:
#         text = f"Пользователь [{user}] задал вопрос:\n{message.text}"
#         await bot.send_message(admin_id, text=text)
#         await message.answer('Сообщение отправлено')

if __name__ == '__main__':
    dp.middleware.setup(AddminMiddleware())
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)