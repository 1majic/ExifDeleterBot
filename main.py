from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from pdf import pdf_file
import shutil

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Отправьте файл")


@dp.message_handler(content_types=["document"])
async def make_watermarked_image(message: types.Message):
    try:
        mess = await message.answer("Загрузка...")
        file = await bot.get_file(message["document"]["file_id"])
        path = f"files/{message.from_user.id}/"
        string = path + file.file_path.split('/')[-1].split(".")[0] + "/"
        await mess.edit_text("Скачивание файла...")
        await bot.download_file_by_id(file.file_id, string + message.document.file_name)
        await mess.edit_text("Обработка...")
        pdf_file(string + message.document.file_name, string + message.document.file_name)
        await message.reply_document(open(string + message.document.file_name, "rb"))
        await mess.delete()
        shutil.rmtree(string, ignore_errors=False, onerror=None)
    except Exception as e:
        await mess.edit_text("Ошибка")
        print(e)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
