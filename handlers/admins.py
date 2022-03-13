import logging

from aiogram.types import Message

from data_loader import get_message_prompt
from keyboards import admin_keyboard
from loader import dp, bot
from misc.misc_functions import admin_check


@dp.message_handler(commands="adminpanel")
@admin_check
async def call_admin_panel(message: Message, **kwargs):
    logging.info(f"Admin panel has been called by @{message.from_user['username']}")
    message_text = get_message_prompt("msg_admin_panel").replace("@username", message.from_user["username"])
    await bot.send_message(message.from_user["id"], text=message_text, reply_markup=admin_keyboard)
