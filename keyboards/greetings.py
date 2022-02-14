from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


greetings_keyboard = InlineKeyboardMarkup(row_width=2)

bot_start_button = InlineKeyboardButton(text="Go to chat with Book Club Bot", callback_data="start_bot_chat")
greetings_keyboard.insert(bot_start_button)
