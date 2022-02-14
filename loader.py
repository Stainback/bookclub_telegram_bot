from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from data_loader import load_bot_data, load_message_data

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
MESSAGE_DATA = load_message_data()
MEETING_DATA, PROFILE_DATA = load_bot_data()

