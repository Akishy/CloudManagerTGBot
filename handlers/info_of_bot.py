from aiogram import types, Dispatcher
from data.config import dispatcher
import logging


# ----- Configurating logs ----- #
logging.basicConfig(filename="logs/logs.txt", filemode='w', level=logging.INFO)


# ----- Info Text ----- #
info_text = f"""
❗❗  Для начала самое главное: чтобы использовать мои команды, необходимо пройти процедуру аутентификации, используя свои данные IAM аккаунта  ❗❗

✅  Для этого, используй - 🔑 <b>Вход</b> 🔑 - и следуй инструкциям внутри команды  ✅

📄  Чтобы более детально ознакомиться с информацией обо мне, открой сайт, кнопка которого (Info) располагается слева от поля ввода сообщения  📄
"""

# ----- /info ----- #
# @dispatcher.message_handler(commands=['info'])
async def info_of_bot(message: types.Message):
	await message.answer(text=f'{info_text}', parse_mode="html")
	logging.info(f"Passed")


def register_handlers(dp: Dispatcher):
	dp.register_message_handler(info_of_bot, text=['📝 Инфо 📝'], state=None)