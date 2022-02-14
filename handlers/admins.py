from aiogram.types import Message, CallbackQuery

from keyboards import admin_keyboard
from loader import dp, bot
from misc.misc_functions import admin_check, generate_meeting_ids


@dp.message_handler(commands="adminpanel")
@admin_check
async def call_admin_panel(message: Message, **kwargs):

    await bot.send_message(message["from"]["id"],
                           text="Hi! You have called admin panel.",
                           reply_markup=admin_keyboard)


@dp.callback_query_handler(lambda c: c.data == "admin_meetings_ids", state=None)
@admin_check
async def show_existing_meeting(call: CallbackQuery, **kwargs):

    await bot.send_message(call.from_user["id"], generate_meeting_ids())
