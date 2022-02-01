from aiogram.types import Chat, Message

from config import CHAT_ID
from data_loader import update_bot_data
from loader import PROFILE_DATA, MEETING_DATA, bot


def generate_meeting_message(meeting: dict) -> str:
    answer = (f'\n\t- {meeting["location"]}, {meeting["meeting_date"]} {meeting["meeting_time"]}.'
              f'\n\t  Discussion topic - {meeting["topic"]}.\n')
    if meeting["comment"] != "":
        answer += f'\t  {meeting["comment"]}\n'
    return answer


async def is_admin(user_id: int, chat: Chat) -> bool:
    user = await chat.get_member(int(user_id))
    admins = await chat.get_administrators()

    return user in admins


def create_new_member_profile(user):
    ids = [profile["t_user_id"] for profile in PROFILE_DATA]

    if user["id"] not in ids:
        new_member_data = {
                            "member_name": user["first_name"],
                            "birth_date": "",
                            "t_user_id": user["id"],
                            "t_username": "@" + user["username"],
                            "instagram": ""
                          }

        PROFILE_DATA.append(new_member_data)
        update_bot_data(MEETING_DATA, PROFILE_DATA)


def admin_check(function):
    async def wrapper(message: Message):

        chat = await bot.get_chat(CHAT_ID)
        if await is_admin(message["from"]["id"], chat):
            await function(message)
        else:
            await message.delete()

    return wrapper
