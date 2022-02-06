from aiogram.types import Chat, Message

from config import CHAT_ID
from data_loader import update_pbot_data
from loader import PROFILE_DATA, bot


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
        update_pbot_data(PROFILE_DATA)


def admin_check(function):
    """This decorator uses for message or callback verification - is it from chat admin or not.

       *args contains only one argument - object with Message or CallbackQuery type.
       **kwargs contains - object 'state' (FSMContext type), 'raw_state' (with state value), 'command'

    """
    async def wrapper(message, **kwargs):

        chat = await bot.get_chat(CHAT_ID)
        if await is_admin(message["from"]["id"], chat):
            await function(message, **kwargs)
        else:
            await message.delete()

    return wrapper
