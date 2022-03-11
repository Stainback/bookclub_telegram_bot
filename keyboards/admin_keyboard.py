from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data_loader import get_message_prompt

"""
    Main admin keyboard. 
"""
admin_keyboard = InlineKeyboardMarkup(row_width=1)

schedule_button = InlineKeyboardButton(text=get_message_prompt("txt_manage_button"),
                                       callback_data="admin_manage_meetings")
admin_keyboard.insert(schedule_button)


"""
  
"""


def create_pm_keyboard(c_data: str):
    admin_pick_meeting_keyboard = InlineKeyboardMarkup(row_width=1)

    admin_pick_button = InlineKeyboardButton(text=get_message_prompt("txt_pick_button"),
                                             callback_data=c_data)
    admin_pick_meeting_keyboard.insert(admin_pick_button)

    return admin_pick_meeting_keyboard


"""

"""
admin_manage_meeting_keyboard = InlineKeyboardMarkup(row_width=1)

admin_create_meeting_button = InlineKeyboardButton(text=get_message_prompt("txt_create_meeting"),
                                                   callback_data="admin_create_meeting")
admin_manage_meeting_keyboard.insert(admin_create_meeting_button)

admin_stop_assigning_button = InlineKeyboardButton(text=get_message_prompt("txt_stop_meeting"),
                                                   callback_data="admin_stop_assigning")
admin_manage_meeting_keyboard.insert(admin_stop_assigning_button)


"""

"""
admin_meeting_property_keyboard = InlineKeyboardMarkup(row_width=1)

admin_skip_property_button = InlineKeyboardButton(text=get_message_prompt("txt_skip_property"),
                                                  callback_data="admin_delete_meeting")
admin_meeting_property_keyboard.insert(admin_skip_property_button)

admin_delete_meeting_button = InlineKeyboardButton(text=get_message_prompt("txt_delete_meeting"),
                                                   callback_data="admin_delete_meeting")
admin_meeting_property_keyboard.insert(admin_delete_meeting_button)

admin_meeting_property_keyboard.insert(admin_stop_assigning_button)

"""

"""
admin_publish_meeting_keyboard = InlineKeyboardMarkup(row_width=1)

admin_approve_publishing_button = InlineKeyboardButton(text=get_message_prompt("txt_approve_publishing"),
                                                       callback_data="admin_approve_meeting_publishing")
admin_publish_meeting_keyboard.insert(admin_approve_publishing_button)

admin_publish_meeting_keyboard.insert(admin_stop_assigning_button)
