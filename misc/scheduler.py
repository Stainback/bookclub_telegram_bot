import asyncio
from datetime import date

import aioschedule

from config import CHAT_ID, DATE_CLUB_BIRTHDAY

from data_loader import collection_profiles, get_message_prompt, collection_meetings
from loader import bot


async def send_daily_notification():
    """This function is expected to be launched via Scheduler at 9:00 on daily basis."""
    today = date.isoformat(date.today())[5::]

    # Check if today is someone's birthday or/and club birthday
    birthday_profiles = collection_profiles.find({"birth_date": today})
    if birthday_profiles is not None:
        for profile in birthday_profiles:
            await bot.send_message(CHAT_ID,
                                   get_message_prompt("msg_birthday_001").replace("@username", profile["username"]))

    if today == DATE_CLUB_BIRTHDAY:
        await bot.send_message(CHAT_ID, get_message_prompt("msg_clubbirthday_001"))

    # Check if today is scheduled meeting
    todays_meetings = collection_meetings.find({"data": {"meeting_date": today}})
    if todays_meetings is not None:
        for meeting in todays_meetings:
            await bot.send_message(CHAT_ID, meeting.generate_meeting_message())


async def remove_obsolete_meetings():
    """This function is expected to be launched via Scheduler at 22:00 on daily basis."""
    today = date.isoformat(date.today())

    todays_meetings = collection_meetings.find({"data": {"meeting_date": today}})
    if todays_meetings is not None:
        for meeting in todays_meetings:
            collection_meetings.delete_one({"_id": meeting["_id"]})


async def scheduler():
    aioschedule.every().day.at("09:00").do(send_daily_notification)
    aioschedule.every().day.at("22:00").do(remove_obsolete_meetings)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)



