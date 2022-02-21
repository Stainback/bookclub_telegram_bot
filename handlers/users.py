from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType, CallbackQuery

from data_loader import update_bot_data
from keyboards.user_keyboard import user_keyboard
from keyboards.greetings import greetings_keyboard
from loader import dp, bot, MEETING_DATA, MESSAGE_DATA, PROFILE_DATA
from misc import Profile


@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def send_introduction_message(message: Message):
    new_member = message.new_chat_members[0]

    new_member_profile = Profile(new_member.id)
    new_member_profile.create_empty_profile()
    new_member_profile.edit_property("username", message["from"]["username"])

    await bot.send_message(message.chat.id,
                           text=MESSAGE_DATA["msg_greeting_001"].replace("@username", new_member.mention),
                           reply_markup=greetings_keyboard)


@dp.message_handler(Text(contains="bot", ignore_case=True))
async def call_bot(message: Message):

    await message.reply(text=MESSAGE_DATA["msg_hibot_001"].replace("@username", "@" + message["from"]["username"]),
                        reply_markup=user_keyboard)


@dp.callback_query_handler(lambda c: c.data == "meetings_callback")
async def send_meeting_notification(call: CallbackQuery):

    await call.answer(cache_time=3600)

    msg_text = "Hi! Following meetings are scheduled:\n"
    for meeting in MEETING_DATA:
        msg_text += meeting.generate_meeting_message()
    await bot.send_message(call.from_user["id"], msg_text)



