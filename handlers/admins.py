from aiogram.types import Message

from keyboards import admin_keyboard
from loader import dp, bot
from misc.misc_functions import admin_check


@dp.message_handler(commands="adminpanel")
@admin_check
async def call_admin_panel(message: Message, **kwargs):

    await bot.send_message(message["from"]["id"],
                           text="Hi! You have called admin panel.",
                           reply_markup=admin_keyboard)
