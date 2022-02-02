from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from data_loader import load_bot_data


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
MEETING_DATA, PROFILE_DATA, MESSAGE_DATA = load_bot_data()