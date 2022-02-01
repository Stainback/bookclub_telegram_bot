from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import URL_BOOKSHEET

user_keyboard = InlineKeyboardMarkup(row_width=2)

form_button = InlineKeyboardButton(text="Fill the Club Form", url=URL_BOOKSHEET)
user_keyboard.insert(form_button)

wishlist_button = InlineKeyboardButton(text="Book Wishlist", url=URL_BOOKSHEET)
user_keyboard.insert(wishlist_button)

meetings_button = InlineKeyboardButton(text="Meetings", callback_data="meetings_callback")
user_keyboard.insert(meetings_button)

link_button = InlineKeyboardButton(text="Send chat link to your friend", callback_data="send_link")
user_keyboard.insert(link_button)

feedback_button = InlineKeyboardButton(text="Send your feedback", callback_data="send_feedback")
user_keyboard.insert(feedback_button)