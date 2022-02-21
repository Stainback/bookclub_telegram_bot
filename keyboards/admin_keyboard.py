from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
    Main admin keyboard. 
    Contains "Schedule meeting", "Edit scheduled meeting", "Delete meeting" and "Show scheduled meetings" buttons.
    
    Calls in personal bot chat with /adminpanel command.
"""
admin_keyboard = InlineKeyboardMarkup(row_width=2)

schedule_button = InlineKeyboardButton(text="Manage meetings", callback_data="admin_manage_meetings")
admin_keyboard.insert(schedule_button)


"""
    
"""
admin_pick_meeting_keyboard = InlineKeyboardMarkup(row_width=1)

admin_pick_button = InlineKeyboardButton(text="Pick this meeting", callback_data="admin_cancel_scheduling")
admin_pick_meeting_keyboard.insert(admin_pick_button)


"""

"""
admin_create_meeting_keyboard = InlineKeyboardMarkup(row_width=1)

admin_create_meeting_button = InlineKeyboardButton(text="Create new meeting", callback_data="admin_create_meeting")
admin_create_meeting_keyboard.insert(admin_create_meeting_button)

"""
   
"""
admin_pick_property_keyboard = InlineKeyboardMarkup(row_width=1)

for i in range(5):
    admin_pick_property_button = InlineKeyboardButton(text=f"{i}", callback_data=f"admin_meeting_property_{i}")
    admin_pick_property_keyboard.insert(admin_pick_property_button)

admin_delete_meeting_button = InlineKeyboardButton(text="Delete this meeting", callback_data="admin_delete_meeting")
admin_pick_property_keyboard.insert(admin_delete_meeting_button)

admin_exit_meeting = InlineKeyboardButton(text="Save and exit", callback_data="admin_save_meeting")
admin_pick_property_keyboard.insert(admin_exit_meeting)


"""

"""
admin_reject_choice_keyboard = InlineKeyboardMarkup(row_width=1)

admin_reject_choice_button = InlineKeyboardButton(text="Reject choice", callback_data="admin_reject_choice")
admin_reject_choice_keyboard.insert(admin_reject_choice_button)
