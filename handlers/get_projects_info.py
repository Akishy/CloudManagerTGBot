from aiogram import types, Dispatcher
from data.config import dispatcher
from aiogram.dispatcher import FSMContext
import logging

# Import Project ID Function
from cloud.iam_management.get_project_id import get_project_id

# # Import Main State
# from handlers.iam_login import User_IAM_Credentials

from utils.db_api import db_commands as cmd
from utils.db_api.db_gino import db


# ----- Configurating logs ----- #
logging.basicConfig(filename="logs/logs.txt", filemode='w', level=logging.INFO)


# ----- /my_projects ----- #
# @dispatcher.message_handler(commands=['my_projects'])
async def get_projects_info(message: types.Message):

	# Вытаскиваем токен относительно id пользователя телеграма
	tkn = await cmd.select_user(message.from_user.id)

	# Получаем значения ключей (имен проектов), делая из него список
	projects_name = list(get_project_id(tkn.token).keys())

	# Основная строка сообщения
	projects_info = "Ваши проекты:\n"

	# Динамическая генерация списка с проектами
	for i in range(len(projects_name)):
		projects_info = projects_info + f"\t\t<b>├─</b> {projects_name[i]}\n"
		
	# Вывод сообщения с названиями проектов
	await message.answer(text=f'{projects_info}', parse_mode="html")

	
	logging.info(f"!")


def register_handlers(dp: Dispatcher):
	dp.register_message_handler(get_projects_info, text=['📁 Мои проекты 📁'])