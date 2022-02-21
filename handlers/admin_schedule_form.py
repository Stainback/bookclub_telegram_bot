import random

from aiogram.dispatcher import FSMContext

from aiogram.types import Message, CallbackQuery

from data.main_db import collection_meetings, get_message_prompt
from fsm.fsm_classes import FSMAdminSchedule
from keyboards import admin_cscheduling_keyboard, admin_save_meeting_keyboard, admin_cremoval_keyboard
from loader import dp, bot
from misc.misc_classes import Meeting
from misc.misc_functions import admin_check

"""
    FSM scenario for scheduling meeting
"""
MEETING_STORAGE = []


@dp.callback_query_handler(lambda c: c.data == "admin_manage_meeting", state=None)
@admin_check
async def admin_start_manage_meetings(call: CallbackQuery, **kwargs):
    meetings = collection_meetings.find({})
    if len(meetings) != 0:
        for meeting in meetings:
            await bot.send_message(call.from_user["id"],
                                   f"\n{meeting['_id']}: {meeting['topic']}, {meeting['meeting_date']}"
                                   f" {meeting['meeting_time']}\n"
                                   f"     {meeting['location']}\n"
                                   f"     {meeting['comment']}\n",
                                   reply_markup=admin_pick_meeting_keyboard)
    await bot.send_message(call.from_user["id"], get_message_prompt("msg_meeting_manual"),
                           reply_markup=admin_create_meeting_keyboard)


@dp.callback_query_handler(lambda c: c.data in ("admin_create_meeting", "admin_meeting"), state=None)
@admin_check
async def admin_create_meeting(call: CallbackQuery, **kwargs):
    # Set FSM to scheduling state
    await FSMAdminSchedule.scenario_scheduling.set()
    # If meeting is being created
    if call.data == "admin_create_meeting":
        meeting = Meeting(random.randint(100, 999), call.from_user["id"])
        meeting.create_empty_meeting()
    # If meeting is being edited
    else:
        meeting = Meeting(meeting_id, call.from_user["id"])
    MEETING_STORAGE.append(meeting)
    # Send notification message
    message_text = ""
    meeting_data = list(meeting.get_data().values())
    for i in range(len(meeting_data)):
        property_prompt = get_message_prompt(f"msg_schedule_{i}")
        message_text += f"{i}. {property_prompt}\n {meeting_data[i] or get_message_prompt('msg_empty_field')}\n"
    await bot.send_message(call.from_user["id"], message_text, reply_markup=admin_pick_property_keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith("admin_meeting_property"),
                           state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_set_property(call: CallbackQuery, **kwargs):
    for meeting in MEETING_STORAGE:
        if meeting.edited_by == call.from_user["id"]:
            meeting.cursor = int(call.data.replace("admin_meeting_property_", ""))
            await bot.send_message(call.from_user["id"], get_message_prompt(f"msg_schedule_{meeting.cursor}"),
                                   reply_markup=admin_reject_choice_keyboard)


@dp.message_handler(lambda m: m["from"]["id"] == m["chat"]["id"], state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_load_property(message: Message, state: FSMContext, **kwargs):
    # Look for the meeting in meeting storage
    for meeting in MEETING_STORAGE:
        if meeting.edited_by == message.from_user["id"]:
            meeting.edit_property(message.text)
            # Send notification message
            await bot.send_message(message.from_user["id"], get_message_prompt("msg_property_updated"),
                                   reply_markup=admin_pick_property_keyboard)


@dp.callback_query_handler(lambda c: c.data == "admin_finish_scheduling", state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_finish_scheduling(call: CallbackQuery, **kwargs):
    await bot.send_message(call.from_user["id"], get_message_prompt("msg_approve_finish"),
                           reply_markup=admin_finish_scheduling_keyboard)


@dp.callback_query_handler(lambda c: c.data == "admin_save_meeting",
                           state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_save_meeting(call: CallbackQuery, state: FSMContext, **kwargs):
    for meeting in MEETING_STORAGE:
        if meeting.edited_by == call.from_user["id"]:
            MEETING_STORAGE.pop(meeting)
    await bot.send_message(call.from_user["id"], get_message_prompt("msg_finish_operation"))
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "admin_delete_meeting",
                           state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_delete_meeting(call: CallbackQuery, state: FSMContext, **kwargs):
    for meeting in MEETING_STORAGE:
        if meeting.edited_by == call.from_user["id"]:
            collection_meetings.delete_one({"_id": meeting.id_num})
            MEETING_STORAGE.pop(meeting)
    await bot.send_message(call.from_user["id"], get_message_prompt("msg_finish_operation"))
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "admin_reject_choice",
                           state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_reject_choice(call: CallbackQuery, **kwargs):
    for meeting in MEETING_STORAGE:
        if meeting.edited_by == call.from_user["id"]:
            message_text = ""
            meeting_data = list(meeting.get_data().values())
            for i in range(len(meeting_data)):
                property_prompt = get_message_prompt(f"msg_schedule_{i}")
                message_text += f"{i}. {property_prompt}\n {meeting_data[i] or get_message_prompt('msg_empty_field')}\n"
            await bot.send_message(call.from_user["id"], message_text, reply_markup=admin_pick_property_keyboard)

