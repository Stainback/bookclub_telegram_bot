from config import CHAT_ID
from data_loader import update_bot_data
from loader import bot, MEETING_DATA, PROFILE_DATA
from misc import Profile


def generate_meeting_ids() -> str:
    ids = ""
    for meeting in MEETING_DATA:
        ids += f"\n{meeting.meeting_id} - " \
               f"{meeting.data['topic']}, {meeting.data['meeting_date']} {meeting.data['meeting_time']}"
    return ids or "No meetings scheduled"


def admin_check(function):
    """
        This decorator uses for message or callback verification - is it from chat admin or not.
    """
    async def wrapper(message, **kwargs):

        chat = await bot.get_chat(CHAT_ID)
        user = await chat.get_member(int(message["from"]["id"]))
        admins = await chat.get_administrators()
        if user in admins:
            await function(message, **kwargs)
        else:
            await message.delete()

    return wrapper
