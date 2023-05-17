from aiogram import executor, types
import logging
import datetime

# Import project files for bot
from data.config import dispatcher, bot
from handlers import info_of_bot, iam_login, get_projects_info, create_ecs
from keyboards import main_buttons


# ----- Configurating logs ----- #
logging.basicConfig(filename="logs/logs.txt", filemode='w', level=logging.INFO)


# ----- Logs: start a bot ----- #
async def on_startup(_):
	logging.info("Bot activated")


# ----- Start Text ----- #
start_msg = '🤖  Мои команды представлены в клавиатуре, чтобы тебе было удобнее со мной взаимодействовать! Советую сначала заглянуть в разлел <b>Инфо</b>!  🤖'


# ----- /start ----- #
# Функция запуска бота
@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
	await message.answer(text=f'🟪  Привет, {message.from_user.username}!  🟪\n\n' + f'{start_msg}', parse_mode="html", reply_markup=main_buttons)
	logging.info(f"Greeted successfully, user={message.from_user}, time={datetime.datetime.now()}")


# ----- Handlers from files ----- #
# ----- /info ----- #
info_of_bot.register_handlers(dispatcher)

# ----- /login ----- #
iam_login.register_handlers(dispatcher)

# ----- /myprojects ----- #
get_projects_info.register_handlers(dispatcher)

# ----- /create_ecs ----- #
create_ecs.register_handlers(dispatcher)


if __name__ == "__main__":
	# Start Bot
	executor.start_polling(dispatcher, skip_updates=False, on_startup=on_startup)