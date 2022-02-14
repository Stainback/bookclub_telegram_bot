import asyncio
from datetime import date

import aioschedule

from config import CHAT_ID, DATE_CLUB_BIRTHDAY
from loader import bot, PROFILE_DATA, MEETING_DATA, MESSAGE_DATA
from data_loader import update_bot_data


async def send_daily_notification():
    """This function is expected to be launched via Scheduler at 9:00 on daily basis."""
    today = date.isoformat(date.today())[5::]

    # Check if today is someone's birthday or/and club birthday
    for profile in PROFILE_DATA:
        if today == profile.data["birth_date"]:

            await bot.send_message(CHAT_ID, MESSAGE_DATA["msg_birthday_001"].replace("@username", profile["username"]))

        if today == DATE_CLUB_BIRTHDAY:

            await bot.send_message(CHAT_ID, MESSAGE_DATA["msg_clubbirthday_001"])

    # Check if today is scheduled meeting
    for meeting in MEETING_DATA:
        if today == meeting.data["meeting_date"]:

            await bot.send_message(CHAT_ID, meeting.generate_meeting_message())


async def remove_obsolete_meetings():
    """This function is expected to be launched via Scheduler at 22:00 on daily basis."""
    today = date.isoformat(date.today())

    for meeting in MEETING_DATA:
        if meeting.data["meeting_date"] == today[5::]:
            MEETING_DATA.pop(MEETING_DATA.index(meeting))
            update_bot_data([meeting.data for meeting in MEETING_DATA], "data/data_meetings.json")


async def scheduler():
    aioschedule.every().day.at("09:00").do(send_daily_notification)
    aioschedule.every().day.at("22:00").do(remove_obsolete_meetings)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)



