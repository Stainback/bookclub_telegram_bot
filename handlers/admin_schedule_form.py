from aiogram.dispatcher import FSMContext

from aiogram.types import Message, CallbackQuery

from config import CHAT_ID
from data_loader import update_bot_data
from fsm.fsm_classes import FSMAdminSchedule
from keyboards import admin_cscheduling_keyboard, admin_save_meeting_keyboard, admin_cremoval_keyboard
from loader import dp, bot, MEETING_DATA, MESSAGE_DATA
from misc.misc_classes import Meeting
from misc.misc_functions import admin_check, generate_meeting_ids

"""
    FSM scenario for scheduling meeting
"""


@dp.callback_query_handler(lambda c: c.data == "admin_create_meeting", state=None)
@admin_check
async def admin_create_meeting(call: CallbackQuery, **kwargs):
    # Set FSM to scheduling state
    await FSMAdminSchedule.scenario_scheduling.set()
    # Create a meeting and append it to meeting storage
    meeting = Meeting()
    meeting.set_owner(call.from_user["id"])
    MEETING_DATA.append(meeting)
    # Send notification message
    await bot.send_message(call.from_user["id"], MESSAGE_DATA[f"msg_schedule_{meeting.scenario_count}"],
                           reply_markup=admin_cscheduling_keyboard)


@dp.callback_query_handler(lambda c: c.data == "admin_edit_meeting", state=None)
@admin_check
async def admin_start_edit_meeting(call: CallbackQuery, **kwargs):
    if MEETING_DATA:
        # Set FSM to editing state
        await FSMAdminSchedule.scenario_editing_meeting.set()
        # Send notification message
        await bot.send_message(call.from_user["id"], generate_meeting_ids())
        await bot.send_message(call.from_user["id"], "Enter meeting id that you want to edit.",
                               reply_markup=admin_cscheduling_keyboard)
    else:
        await bot.send_message(call.from_user["id"], "No meetings scheduled.")


@dp.message_handler(lambda m: m["from"]["id"] == m["chat"]["id"] and m.text.isdigit(),
                    state=FSMAdminSchedule.scenario_editing_meeting)
@admin_check
async def admin_set_meeting_to_edit_mode(message: Message, state: FSMContext, **kwargs):
    # Look for the meeting in meeting storage
    for meeting in MEETING_DATA:
        if meeting.meeting_id == int(message.text):
            meeting.set_owner(message.from_user["id"])
            await FSMAdminSchedule.scenario_scheduling.set()
            await bot.send_message(message.from_user["id"], MESSAGE_DATA[f"msg_schedule_{meeting.scenario_count}"],
                                   reply_markup=admin_cscheduling_keyboard)
            return
    # Send notification message if meeting has not been found
    await bot.send_message(message.from_user["id"], "Meeting has not been found")
    # Abort scenario
    await state.finish()


@dp.message_handler(lambda m: m["from"]["id"] == m["chat"]["id"], state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_load_property(message: Message, state: FSMContext, **kwargs):
    # Look for the meeting in meeting storage
    for meeting in MEETING_DATA:
        if meeting.owner_id == message.from_user["id"]:
            if message.text == "skip":
                meeting.scenario_count += 1
            else:
                meeting.fill_property(message.text)  # scenario_count += 1

            while meeting.scenario_count <= len(meeting.properties) - 1:
                await bot.send_message(message.from_user["id"],
                                       f"{MESSAGE_DATA[f'msg_schedule_{meeting.scenario_count}']}\n"
                                       f"\t{meeting.data[meeting.properties[meeting.scenario_count]]}",
                                       reply_markup=admin_cscheduling_keyboard)
                return

            # Move to "save meeting" stage if Meeting goes out of unfilled properties
            await bot.send_message(message.from_user["id"], f"{meeting.generate_meeting_message()}\n"
                                                            f"Do you want to save the meeting?",
                                   reply_markup=admin_save_meeting_keyboard)
            return
    # Send notification message if meeting has not been found
    await bot.send_message(message.from_user["id"], "Meeting has not been found")
    # Abort scenario
    await state.finish()


@dp.callback_query_handler(lambda c: c.data in ("admin_save_send_meeting", "admin_save_meeting"),
                           state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_save_meeting(call: CallbackQuery, state: FSMContext, **kwargs):
    # Update file with meeting data
    update_bot_data([meeting.data for meeting in MEETING_DATA], "data/data_meetings.json")
    # Send notification message
    await bot.send_message(call.from_user["id"], "Meeting has been saved")
    if call.data == "admin_save_send_meeting":
        # Publish meeting
        for meeting in MEETING_DATA:
            if meeting.owner_id == call.from_user["id"]:
                meeting.set_owner()
                await bot.send_message(CHAT_ID, meeting.generate_meeting_message())
    # Finish scenario
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "admin_cancel_scheduling", state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_cancel_scheduling(call: CallbackQuery, state: FSMContext, **kwargs):
    # Delete meeting
    for meeting in MEETING_DATA:
        if meeting.owner_id == call.from_user["id"]:
            MEETING_DATA.pop(MEETING_DATA.index(meeting))
            update_bot_data([meeting.data for meeting in MEETING_DATA], "data/data_meetings.json")
    # Send notification message
    await bot.send_message(call.from_user["id"], "Operation has been cancelled")
    # Finish scenario
    await state.finish()


"""
    FSM scenario for meeting removal
"""


@dp.callback_query_handler(lambda c: c.data == "admin_remove_meeting", state=None)
@admin_check
async def admin_start_removal_scenario(call: CallbackQuery, **kwargs):
    # Set FSM to removing state
    await FSMAdminSchedule.scenario_removing.set()
    # Generate meeting ids and send them in message
    await bot.send_message(call.from_user["id"], generate_meeting_ids())
    await bot.send_message(call.from_user["id"], "Enter meeting id to remove",
                           reply_markup=admin_cremoval_keyboard)


@dp.message_handler(lambda m: m["from"]["id"] == m["chat"]["id"] and m.text.isdigit(),
                    state=FSMAdminSchedule.scenario_removing)
@admin_check
async def admin_remove_meeting(message: Message, state: FSMContext, **kwargs):
    # Remove the meeting from meeting data
    for meeting in MEETING_DATA:
        if meeting.meeting_id == int(message.text):
            MEETING_DATA.pop(MEETING_DATA.index(meeting))
            update_bot_data([meeting.data for meeting in MEETING_DATA], "data/data_meetings.json")
            # Send notification message
            await bot.send_message(message["from"]["id"], "Meeting has been removed")
    # Finish removal scenario
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "admin_cancel_removal", state=FSMAdminSchedule.scenario_removing)
@admin_check
async def admin_cancel_removal(call: CallbackQuery, state: FSMContext, **kwargs):
    # Send notification message
    await bot.send_message(call.from_user["id"], "Operation has been canceled.")
    # Finish scenario
    await state.finish()
