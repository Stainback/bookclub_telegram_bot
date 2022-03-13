import asyncio
from datetime import date

import aioschedule

from config import CHAT_ID, DATE_CLUB_BIRTHDAY

from data_loader import collection_profiles, get_message_prompt, collection_meetings, generate_meeting_messages
from loader import bot


async def send_daily_notification():
    """This function is expected to be launched via Scheduler at 9:00 on daily basis."""
    print("\"Daily notification\" function is active.")
    today = date.isoformat(date.today())[5::]

    # Check if today is someone's birthday or/and club birthday
    birthday_profiles = collection_profiles.find({"birth_date": today})
    if birthday_profiles is not None:
        print(birthday_profiles)
        for profile in birthday_profiles:
            await bot.send_message(CHAT_ID,
                                   get_message_prompt("msg_birthday_001").replace("@username", profile["username"]))

    if today == DATE_CLUB_BIRTHDAY:
        print("Club birthday event has been started")
        await bot.send_message(CHAT_ID, get_message_prompt("msg_clubbirthday_001"))

    # Check if today is scheduled meeting
    todays_meetings = generate_meeting_messages({"data": {"meeting_date": today}}).values()
    print(todays_meetings)
    for meeting_text in todays_meetings:
        await bot.send_message(CHAT_ID, meeting_text)


async def remove_obsolete_meetings():
    """This function is expected to be launched via Scheduler at 22:00 on daily basis."""
    print("Looking for obsolete meetings...")
    today = date.isoformat(date.today())
    collection_meetings.delete_many({"data": {"meeting_date": today}})


async def scheduler():
    aioschedule.every().day.at("09:00").do(send_daily_notification)
    aioschedule.every().day.at("22:00").do(remove_obsolete_meetings)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)



