from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import URL_BOOKSHEET

from data_loader import get_message_prompt

"""
    Main user keyboard. 
"""
user_keyboard = InlineKeyboardMarkup(row_width=2)

edit_form_button = InlineKeyboardButton(text=get_message_prompt("txt_edit_form"), callback_data="edit_form")
user_keyboard.insert(edit_form_button)

meetings_button = InlineKeyboardButton(text=get_message_prompt("txt_meetings_notification"),
                                       callback_data="meetings_callback")
user_keyboard.insert(meetings_button)

wishlist_button = InlineKeyboardButton(text=get_message_prompt("txt_wishlist"), url=URL_BOOKSHEET)
user_keyboard.insert(wishlist_button)

"""
    Form management keyboard. 
"""
manage_form_keyboard = InlineKeyboardMarkup(row_width=1)

start_editing_button = InlineKeyboardButton(text=get_message_prompt("txt_start_editing"), callback_data="start_editing")
manage_form_keyboard.insert(start_editing_button)

clear_data_button = InlineKeyboardButton(text=get_message_prompt("txt_clear_data"), callback_data="clear_form_data")
manage_form_keyboard.insert(clear_data_button)

stop_editing_button = InlineKeyboardButton(text=get_message_prompt("txt_stop_editing"), callback_data="stop_editing")
manage_form_keyboard.insert(stop_editing_button)

"""
    Keyboard attached to messages with questions
"""
question_keyboard = InlineKeyboardMarkup(row_width=1)

skip_question_button = InlineKeyboardButton(text=get_message_prompt("txt_skip_question"),
                                            callback_data="skip_question")
question_keyboard.insert(skip_question_button)

question_keyboard.insert(stop_editing_button)

"""
    Keyboard attached to message which sends after filling all questions
"""
publish_form_keyboard = InlineKeyboardMarkup(row_width=2)

approve_publishing_button = InlineKeyboardButton(text=get_message_prompt("txt_approve_publishing"),
                                                 callback_data="publish_form")
publish_form_keyboard.insert(approve_publishing_button)

publish_form_keyboard.insert(stop_editing_button)
