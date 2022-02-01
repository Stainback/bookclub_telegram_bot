import asyncio
from datetime import date

import aioschedule

from config import CHAT_ID, DATE_CLUB_BIRTHDAY
from data_loader import update_bot_data
from loader import PROFILE_DATA, bot, MEETING_DATA, MESSAGE_DATA
from misc.misc_functions import generate_meeting_message


async def send_daily_notification():
    """This function is expected to be launched via Scheduler at 9:00 on daily basis."""
    today = date.isoformat(date.today())[5::]

    # Check if today is someone's birthday or/and club birthday
    for profile in PROFILE_DATA:
        if today == profile["birth_date"]:

            await bot.send_message(CHAT_ID, MESSAGE_DATA[1].replace("@username", profile["username"]))

        if today == DATE_CLUB_BIRTHDAY:

            await bot.send_message(CHAT_ID, MESSAGE_DATA[2])

    # Check if today is scheduled meeting
    for meeting in MEETING_DATA:
        if today == meeting["meeting_date"][5::]:

            await bot.send_message(CHAT_ID, generate_meeting_message(meeting))


async def remove_obsolete_meetings():
    """This function is expected to be launched via Scheduler at 22:00 on daily basis."""
    today = date.isoformat(date.today())

    for meeting in MEETING_DATA:
        if meeting["meeting_date"] == today:
            MEETING_DATA.pop(MEETING_DATA.index(meeting))
            update_bot_data(MEETING_DATA, PROFILE_DATA)


async def scheduler():
    aioschedule.every().day.at("09:00").do(send_daily_notification)
    aioschedule.every().day.at("22:00").do(remove_obsolete_meetings)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)



