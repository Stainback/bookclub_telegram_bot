from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import URL_BOOKSHEET


"""
    Main user keyboard. 

    Calls in personal bot chat.
"""

user_keyboard = InlineKeyboardMarkup(row_width=2)

edit_form_button = InlineKeyboardButton(text="Заполнить клубную анкету", callback_data="edit_form")
user_keyboard.insert(edit_form_button)

meetings_button = InlineKeyboardButton(text="Собрания", callback_data="meetings_callback")
user_keyboard.insert(meetings_button)

wishlist_button = InlineKeyboardButton(text="Список пожеланий к прочтению", url=URL_BOOKSHEET)
user_keyboard.insert(wishlist_button)


"""
    Cancelling keyboard. 

    Attached to bot messages in personal bot chat during form creating operations.
"""
cancel_form_keyboard = InlineKeyboardMarkup(row_width=1)

cancel_form_button = InlineKeyboardButton(text="Отложить заполнение", callback_data="cancel_form")
cancel_form_keyboard.insert(cancel_form_button)


"""
    "Approve form removal" keyboard. 

    Attached to bot messages in personal bot chat during removal operations.
"""
approve_form_removal_keyboard = InlineKeyboardMarkup(row_width=2)

approve_form_removal_button = InlineKeyboardButton(text="Да", callback_data="remove_form_approved")
approve_form_removal_keyboard.insert(approve_form_removal_button)

reject_form_removal_button = InlineKeyboardButton(text="Нет", callback_data="cancel_removal")
approve_form_removal_keyboard.insert(reject_form_removal_button)

"""
    Form saving keyboard. 

    Attached to final bot message in form editing operation scenario in personal bot chat.
"""
save_form_keyboard = InlineKeyboardMarkup(row_width=1)


save_send_button = InlineKeyboardButton(text="Да, сохраните и опубликуйте анкету в чат",
                                        callback_data="save_send_form")
save_form_keyboard.insert(save_send_button)

delete_button = InlineKeyboardButton(text="Нет, удалите заполненные данные", callback_data="remove_form")
save_form_keyboard.insert(delete_button)

edit_button = InlineKeyboardButton(text="Нет, я хочу отредактировать ее", callback_data="edit_form")
save_form_keyboard.insert(edit_button)
