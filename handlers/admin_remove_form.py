from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from data_loader import update_mbot_data
from keyboards import admin_cremoval_keyboard
from loader import dp, bot, MEETING_DATA
from misc.misc_functions import admin_check


class FSMAdminRemove(StatesGroup):
    meeting_id = State()


@dp.callback_query_handler(lambda c: c.data == "admin_cancel_removal", state=FSMAdminRemove.meeting_id)
@admin_check
async def cancel_schedule_operation(call: CallbackQuery, state: FSMContext, **kwargs):

    await bot.send_message(call.from_user["id"], "Operation has been canceled.")

    await state.finish()


# FSM scenario for meeting removal
@dp.callback_query_handler(lambda c: c.data == "remove_meeting", state=None)
@admin_check
async def start_removal_scenario(call: CallbackQuery, **kwargs):
    await FSMAdminRemove.meeting_id.set()

    ids = ""
    for meeting in MEETING_DATA:
        ids += f"\n{meeting['meeting_id']} - {meeting['topic']}, {meeting['meeting_date']} {meeting['meeting_time']}"

    await bot.send_message(call.from_user["id"], ids)

    await bot.send_message(call.from_user["id"], "Enter meeting id to remove",
                           reply_markup=admin_cremoval_keyboard)


@dp.message_handler(state=FSMAdminRemove.meeting_id)
@admin_check
async def remove_meeting(message: Message, state: FSMContext, **kwargs):

    # Choose a meeting to delete
    meeting_id = message.text

    # Remove the meeting from meeting data
    for meeting in MEETING_DATA:
        if meeting["meeting_id"] == meeting_id:
            MEETING_DATA.pop(MEETING_DATA.index(meeting))
            update_mbot_data(MEETING_DATA)

            # Send notification message
            await bot.send_message(message["from"]["id"],
                                   f"Meeting \"{meeting['topic']}, {meeting['meeting_date']}"
                                   f" {meeting['meeting_time']}\" has been removed")

    await state.finish()
