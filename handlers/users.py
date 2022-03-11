from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType, CallbackQuery

from data_loader import get_message_prompt, collection_meetings
from keyboards.user_keyboard import user_keyboard
from keyboards.greetings import greetings_keyboard
from loader import dp, bot
from misc import Profile


@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def send_introduction_message(message: Message):
    new_member = message.new_chat_members[0]
    # Create profile post for new member in db
    new_member_profile = Profile(new_member.id)
    new_member_profile.create_empty_profile()
    new_member_profile.edit_property("username", message["from"]["username"])
    # Send notification message
    await bot.send_message(message.chat.id,
                           text=get_message_prompt("msg_greeting_001").replace("@username", new_member.mention),
                           reply_markup=greetings_keyboard)


@dp.message_handler(Text(contains="bot", ignore_case=True))
async def call_bot(message: Message):
    # Send message with bot interface as answer on call
    await message.reply(text=get_message_prompt("msg_hibot_001").replace("@username", "@" + message["from"]["username"]),
                        reply_markup=user_keyboard)


@dp.callback_query_handler(lambda c: c.data == "meetings_callback")
async def send_meeting_notification(call: CallbackQuery):
    # Timeout assignment
    await call.answer(cache_time=3600)
    meeting_text = ""
    for meeting in collection_meetings.find({}):
        meeting_data = meeting["data"]
        # Generate message text for a meeting
        meeting_text += f"\n{meeting_data['topic']}. {meeting_data['meeting_date']}, {meeting_data['meeting_time']}." \
                        f"\n{meeting_data['location']}\n{meeting_data['comment']}\n"
    await bot.send_message(call.from_user["id"], meeting_text)
