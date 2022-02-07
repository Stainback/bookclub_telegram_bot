from aiogram.dispatcher import FSMContext

from aiogram.types import Message, CallbackQuery

from data_loader import update_mbot_data
from fsm.fsm_classes import FSMAdminRemove
from keyboards import admin_cremoval_keyboard
from loader import dp, bot, MEETING_DATA
from misc.misc_functions import admin_check


# FSM scenario for meeting removal
@dp.callback_query_handler(lambda c: c.data == "remove_meeting", state=None)
@admin_check
async def start_removal_scenario(call: CallbackQuery, **kwargs):
    await FSMAdminRemove.scenario_removing.set()

    ids = ""
    for meeting in MEETING_DATA:
        ids += f"\n{meeting.data['meeting_id']} - " \
               f"{meeting.data['topic']}, {meeting.data['meeting_date']} {meeting.data['meeting_time']}"

    await bot.send_message(call.from_user["id"], ids)

    await bot.send_message(call.from_user["id"], "Enter meeting id to remove",
                           reply_markup=admin_cremoval_keyboard)


@dp.message_handler(state=FSMAdminRemove.scenario_removing)
@admin_check
async def remove_meeting(message: Message, state: FSMContext, **kwargs):

    # Choose a meeting to delete
    meeting_id = message.text

    # Remove the meeting from meeting data
    for meeting in MEETING_DATA:
        if meeting.data["meeting_id"] == meeting_id:
            MEETING_DATA.pop(MEETING_DATA.index(meeting))
            update_mbot_data(MEETING_DATA)

            # Send notification message
            await bot.send_message(message["from"]["id"],
                                   f"Meeting \"{meeting.data['topic']}, {meeting.data['meeting_date']}"
                                   f" {meeting.data['meeting_time']}\" has been removed")

    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "admin_cancel_removal", state=FSMAdminRemove.scenario_removing)
@admin_check
async def cancel_schedule_operation(call: CallbackQuery, state: FSMContext, **kwargs):

    await bot.send_message(call.from_user["id"], "Operation has been canceled.")

    await state.finish()
