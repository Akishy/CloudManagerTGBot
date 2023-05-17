from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Main object of bot
bot = Bot(token='')


# Dispatcher for bot
dispatcher = Dispatcher(bot, storage=MemoryStorage())



