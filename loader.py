from aiogram import Bot, Dispatcher

from config import TOKEN
from data_loader import load_bot_data

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
MEETING_DATA, PROFILE_DATA, MESSAGE_DATA = load_bot_data()
