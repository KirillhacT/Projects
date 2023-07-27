import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import asyncio
from photoToText import getPhotoToText

logging.basicConfig(level=logging.INFO)
TOKEN = ""
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Директория для сохранения картинок
image_dir = "images"

# Создаем директорию, если ее нет
def delete_all_photos():
    arr = os.listdir(image_dir)
    for i in arr:
        os.remove(f"{image_dir}/{i}")

@dp.message_handler(commands=['start'])
async def start_cmd_handler(message: types.Message):
    await message.reply("Привет! Отправь мне картинку, и я сохраню ее в папку 'images'.")

@dp.message_handler(commands=["update"])
async def update(message: types.Message):
    text = getPhotoToText()
    await asyncio.sleep(2)
    await bot.send_message(message.chat.id, text)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photos(message: types.Message):
    delete_all_photos()
    file_info = message.photo[-1]
    file_id = file_info.file_id
    file_info = await bot.get_file(file_id)
    file = await bot.download_file(file_info.file_path)
    file_name = f"{image_dir}/{file_info.file_id}.jpg"
    with open(file_name, "wb") as f:
        f.write(file.read())
    await asyncio.sleep(1)
    await message.reply(f"Картинка сохранена в {file_name}")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)