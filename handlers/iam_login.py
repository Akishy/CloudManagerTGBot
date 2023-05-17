from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from data.config import dispatcher
from keyboards import cancel_buttons
import logging

from utils.db_api import db_commands as cmd
from utils.db_api.db_gino import db, PostgresURI


# Imports From Files
from cloud.iam_management.get_user_token import get_user_token
from cloud.iam_management.validate_token import validate_token

# States
from states.credentials_state import User_IAM_Credentials


# ----- Configurating logs ----- #
logging.basicConfig(filename="logs/logs.txt", filemode='w', level=logging.INFO)


# ----- Main message in /login----- #
login_text = """
🔔  Для того, чтобы иметь возможность удаленного управления Cloud\'ом, необходимо зайти в аккаунт!  🔔

🟪  Чтобы зайти в аккаунт, введи последовательно IAM-данные для входа в личный кабинет:
\t\t<b>├─</b> IAM user name (ivanov)
\t\t<b>├─</b> Account name (ex. ADV-12345...)
\t\t<b>└─</b> Password

🔒  Не переживай, я создам все необходимые данные, чтобы ты смог получить доступ ко всем необходимым командам. В любое время ты можешь выйти из аккаунта, применив соответствующую команду.  🔒

🔔  Если передумал проходить процедуру ввода или ввел что-то неправильно, нажми на "Отмена" ниже данного сообщения  🔔
"""


# ----- /login ----- #
# Doc: Начало диалога с пользователем. Диалог предсназначен для получения IAM данных от пользователя
# @dispatcher.message_handler(commands=['login'])
async def iam_login(message: types.Message, state=None):

	# Перехватываем ответ и переносим в следующий хэндлер для обратотки
	await User_IAM_Credentials.iam_user_name.set()

	# Выводим главное сообщение
	await message.answer(text=f'{login_text}', parse_mode="html", reply_markup=cancel_buttons)

	# Запрашиваем у пользователя IAM user name
	await message.answer(text='Пожалуйста, для начала введи IAM user name:', parse_mode="html")

	# Лог
	logging.info(f"Запрошен {message.from_user} IAM user name")
# ---------------------------------------- #


# ----- State: iam_user_name ----- #
async def get_user_name_iam(message: types.Message, state: FSMContext):
	# Присваиваем значение полю iam_user_name
	async with state.proxy() as data:
		data['iam_user_name'] = message.text

	# Лог
	logging.info(f"От пользователя {message.from_user} получен параметр IAM user name")

	# Переходим далее по состоянию
	await User_IAM_Credentials.next()

	# Сообщаем пользователю, что IAM user name получен успешно
	await message.answer(text="IAM user name получен, теперь введи Account name (e.g. ADV-1234...): ")

	# Лог
	logging.info(f"Запрошен {message.from_user} Account name")
# ---------------------------------------- #


# ----- State: iam_account_name ----- #
async def get_account_name_iam(message: types.Message, state: FSMContext):
	# Присваиваем значение полю iam_user_name
	async with state.proxy() as data:
		data['iam_account_name'] = message.text

	# Лог
	logging.info(f"От пользователя {message.from_user} получен параметр Account name (ADV)")

	# Переходим далее по состоянию
	await User_IAM_Credentials.next()

	# Сообщаем пользователю, что Account name получен успешно
	await message.answer(text="ADV успешно получен, осталось только ввести пароль 🔑: ")

	# Лог
	logging.info(f"Запрошен {message.from_user} пароль")
# ---------------------------------------- #


# ----- State: iam_password ----- #
async def get_user_password_iam(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['iam_password'] = message.text
		
		# Дополнительно получаем id пользователя в Telegram (для последующей записи в БД)
		tg_id_user = message.from_user.id
	
		# Лог
		logging.info(f"От пользователя {message.from_user} получен параметр Password")

		# Сообщаем пользователю, что Account name получен успешно
		await message.answer(text="Пароль успешно получен. Генерирую необходимые данные для дальнейшей работы!")

		# Лог
		logging.info(f"Генерируется {message.from_user} токен")

		# Из функции получаем объект, откуда забираем значение токена (X-Subject-Token)
		token = get_user_token(data['iam_user_name'], data['iam_account_name'], data['iam_password'])
	
		# Если response code отличен от 201, то запрос не корректен, поэтому останавливаем state'ы
		if token[1] != 201 & token[1] != 200:
			await message.answer(text="❌  Ваши введенные данные некорректны, попробуйте повторно пройти процедуру логина, предварительно проверив вводимые данные!  ❌")
			await state.finish()
		else:
			# Извлекаем токен из ответа
			auth_token = token[0]['X-Subject-Token']

			# Работаем с базой данных - добавляем запись пользователя
			await db.set_bind(PostgresURI)
			# await db.gino.drop_all()

			await db.gino.create_all()

			if await cmd.select_user(tg_id_user) == None:
				await cmd.add_user_and_token(tg_id_user, data['iam_user_name'],  data['iam_account_name'], data['iam_password'], auth_token)
			else:
				await message.answer(text="Ранее ты уже регистрировался, я тебя распознал, но надо проверить некоторые данные для дальнейшего взаимодействия")
			
			# 
			if validate_token(auth_token, auth_token) == 200:
				await message.answer(text="✅  Процедура аутентификации прошла успешно, можно приступать к работе. Напоминаю, для простоты манипулирования используй мою клавиатуру  ✅")
				await state.finish()
			else:
				await message.answer(text="❌ TOKEN Ваши введенные данные некорректны, попробуйте повторно пройти процедуру логина, предварительно проверив вводимые данные!  ❌")
				await state.finish()
# ---------------------------------------- #


# ----- Cancel Login Callback Handler ----- #
async def cancel_login_signal(callback_query: types.CallbackQuery, state: FSMContext):
	# Данный callback предназначен для того, чтобы отменить процедуру аутентификации и очистить введенные данные на случае, если пользователь ошибся
	await state.finish()
	await callback_query.message.answer("Отмена! Жду дальнейших указаний! Напоминаю, чтобы иметь полный доступ к командам, необходимо пройти аутентификацию")
	await callback_query.answer()
# ---------------------------------------- #


def register_handlers(dp: Dispatcher):
	# Register Login Handler
	dp.register_message_handler(iam_login, text=['🔑 Вход 🔑'])

	# Register States of Login Handler
	dp.register_message_handler(get_user_name_iam, state=User_IAM_Credentials.iam_user_name)
	dp.register_message_handler(get_account_name_iam, state=User_IAM_Credentials.iam_account_name)
	dp.register_message_handler(get_user_password_iam, state=User_IAM_Credentials.iam_password)
	dp.register_callback_query_handler(cancel_login_signal, state=User_IAM_Credentials)
