from .admin_schedule_form import *
from .admin_remove_form import *

from keyboards import admin_keyboard
from misc.misc_functions import admin_check


@dp.message_handler(commands="adminpanel")
@admin_check
async def call_admin_panel(message: Message):

    await bot.send_message(message["from"]["id"],
                           text="Hi! You have called admin panel.",
                           reply_markup=admin_keyboard)

