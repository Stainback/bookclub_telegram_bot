from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data_loader import get_message_prompt

greetings_keyboard = InlineKeyboardMarkup(row_width=1)

bot_start_button = InlineKeyboardButton(text=get_message_prompt("txt_bot_start"), callback_data="start_bot_chat")
greetings_keyboard.insert(bot_start_button)
