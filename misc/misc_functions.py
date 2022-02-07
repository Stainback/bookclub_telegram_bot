from config import CHAT_ID
from data_loader import update_pbot_data
from loader import PROFILE_DATA, bot
from misc import Profile


def generate_meeting_message(meeting: dict) -> str:
    answer = (f'\n\t- {meeting["location"]}, {meeting["meeting_date"]} {meeting["meeting_time"]}.'
              f'\n\t  Discussion topic - {meeting["topic"]}.\n')
    if meeting["comment"] != "":
        answer += f'\t  {meeting["comment"]}\n'
    return answer


def create_new_member_profile(user):
    ids = [profile.data["user_id"] for profile in PROFILE_DATA]

    if user["id"] not in ids:
        new_member_data = {
                            "member_name": user["first_name"],
                            "user_id": user["id"],
                            "username": "@" + user["username"],
                            "birth_date": "",
                          }

        PROFILE_DATA.append(Profile(new_member_data))
        update_pbot_data(PROFILE_DATA)


def admin_check(function):
    """This decorator uses for message or callback verification - is it from chat admin or not.

       *args contains only one argument - object with Message or CallbackQuery type.
       **kwargs contains - object 'state' (FSMContext type), 'raw_state' (with state value), 'command'

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
