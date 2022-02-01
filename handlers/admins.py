from aiogram.types import Message

from config import CHAT_ID
from keyboards import admin_keyboard
from loader import dp, bot, MEETING_DATA, PROFILE_DATA
from data_loader import update_bot_data
from misc.misc_functions import is_admin, admin_check


@dp.message_handler(commands="adminpanel")
@admin_check
async def call_admin_panel(message: Message):

    await bot.send_message(message["from"]["id"],
                           text="Hi! You have called admin panel.",
                           reply_markup=admin_keyboard)


@dp.message_handler(commands="schedule")
@admin_check
async def schedule_meeting(message: Message):

    # Create a meeting
    message_text = message.get_args().split(sep='/')

    # Update bot data with created meeting
    location, meeting_date, meeting_time, topic, comment = message_text[0], message_text[1], message_text[2], message_text[3], message_text[4]
    MEETING_DATA.append({
        "meeting_id": meeting_date.replace("-", "") + meeting_time.replace(":", ""),
        "location": location,
        "meeting_date": meeting_date,
        "meeting_time": meeting_time,
        "topic": topic,
        "comment": comment
    })
    update_bot_data(MEETING_DATA, PROFILE_DATA)

    # Send a notification message
    await bot.send_message(message["from"]["id"], f"New meeting has been scheduled."
                                                  f"\n\t- {location}, {meeting_date} {meeting_time}"
                                                  f"\n\t  Discussion topic - {topic}"
                                                  f"\n\t  {comment}")


@dp.message_handler(commands="remove")
@admin_check
async def remove_meeting(message: Message):

    # Choose a meeting to delete
    meeting_id = message.get_args()

    # Remove the meeting from meeting data
    for meeting in MEETING_DATA:
        if meeting["meeting_id"] == meeting_id:
            MEETING_DATA.pop(MEETING_DATA.index(meeting))
            update_bot_data(MEETING_DATA, PROFILE_DATA)

            # Send notification message
            await bot.send_message(message["from"]["id"],
                                   f"Meeting \"{meeting['topic']}, {meeting['meeting_date']}"
                                   f" {meeting['meeting_time']}\" has been removed")


@dp.message_handler(commands="showids")
@admin_check
async def show_meeting_ids(message: Message):

    ids = ""
    for meeting in MEETING_DATA:
        ids += f"\n{meeting['meeting_id']} - {meeting['topic']}, {meeting['meeting_date']} {meeting['meeting_time']}"

    await bot.send_message(message["from"]["id"], ids)

