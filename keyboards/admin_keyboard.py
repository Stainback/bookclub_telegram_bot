from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


admin_keyboard = InlineKeyboardMarkup(row_width=2)

schedule_button = InlineKeyboardButton(text="Schedule a new meeting", callback_data="schedule_meeting")
admin_keyboard.insert(schedule_button)

remove_button = InlineKeyboardButton(text="Remove a meeting", callback_data="remove_meeting")
admin_keyboard.insert(remove_button)

ids_button = InlineKeyboardButton(text="Meetings", callback_data="meetings_ids")
admin_keyboard.insert(ids_button)


admin_cscheduling_keyboard = InlineKeyboardMarkup(row_width=1)

admin_csch_button = InlineKeyboardButton(text="Cancel scheduling", callback_data="admin_cancel_scheduling")
admin_cscheduling_keyboard.insert(admin_csch_button)


admin_cremoval_keyboard = InlineKeyboardMarkup(row_width=1)

admin_crem_button = InlineKeyboardButton(text="Cancel removal", callback_data="admin_cancel_removal")
admin_cremoval_keyboard.insert(admin_crem_button)
