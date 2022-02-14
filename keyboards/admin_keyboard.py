from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
    Main admin keyboard. 
    Contains "Schedule meeting", "Edit scheduled meeting", "Delete meeting" and "Show scheduled meetings" buttons.
    
    Calls in personal bot chat with /adminpanel command.
"""
admin_keyboard = InlineKeyboardMarkup(row_width=2)

schedule_button = InlineKeyboardButton(text="Schedule a new meeting", callback_data="admin_create_meeting")
admin_keyboard.insert(schedule_button)

edit_schedule_button = InlineKeyboardButton(text="Edit a meeting", callback_data="admin_edit_meeting")
admin_keyboard.insert(edit_schedule_button)

remove_button = InlineKeyboardButton(text="Remove a meeting", callback_data="admin_remove_meeting")
admin_keyboard.insert(remove_button)

ids_button = InlineKeyboardButton(text="Meetings", callback_data="admin_meetings_ids")
admin_keyboard.insert(ids_button)

"""
    Cancelling keyboard. 
    Contains "Cancel scheduling operation" button.

    Attached to bot messages in personal bot chat during scheduling operations.
"""
admin_cscheduling_keyboard = InlineKeyboardMarkup(row_width=1)

admin_csch_button = InlineKeyboardButton(text="Cancel scheduling", callback_data="admin_cancel_scheduling")
admin_cscheduling_keyboard.insert(admin_csch_button)


"""
    Meeting removal keyboard. 
    Contains "Cancel removal operation" button.

    Attached to bot messages in personal bot chat during removal operations.
"""
admin_cremoval_keyboard = InlineKeyboardMarkup(row_width=1)

admin_crem_button = InlineKeyboardButton(text="Cancel removal", callback_data="admin_cancel_removal")
admin_cremoval_keyboard.insert(admin_crem_button)

"""
    Meeting saving keyboard. 
    Contains "Save the meeting", "Save the meeting and send notification" and "Reject the meeting" buttons.

    Attached to final bot message in scheduling operation scenario in personal bot chat.
"""
admin_save_meeting_keyboard = InlineKeyboardMarkup(row_width=1)

admin_save_button = InlineKeyboardButton(text="Yes, save it.",
                                         callback_data="admin_save_meeting")
admin_save_meeting_keyboard.insert(admin_save_button)

admin_save_send_button = InlineKeyboardButton(text="Yes, save it and send notification to the general chat.",
                                              callback_data="admin_save_send_meeting")
admin_save_meeting_keyboard.insert(admin_save_send_button)

admin_delete_button = InlineKeyboardButton(text="No, delete it.", callback_data="admin_cancel_scheduling")
admin_save_meeting_keyboard.insert(admin_delete_button)
