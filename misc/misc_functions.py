from config import CHAT_ID
from loader import bot


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
