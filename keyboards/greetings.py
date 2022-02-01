from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import URL_BOOKSHEET

greetings_keyboard = InlineKeyboardMarkup(row_width=2)

form_button = InlineKeyboardButton(text="Fill the Club Form", url=URL_BOOKSHEET)
greetings_keyboard.insert(form_button)

wishlist_button = InlineKeyboardButton(text="Book Wishlist", url=URL_BOOKSHEET)
greetings_keyboard.insert(wishlist_button)

meetings_button = InlineKeyboardButton(text="Meetings", callback_data="meetings_callback")
greetings_keyboard.insert(meetings_button)
