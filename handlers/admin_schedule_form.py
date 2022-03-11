import random

from aiogram.dispatcher import FSMContext

from aiogram.types import Message, CallbackQuery

from data_loader import collection_meetings, get_message_prompt
from fsm.fsm_classes import FSMAdminSchedule
from keyboards import create_pm_keyboard, admin_manage_meeting_keyboard, admin_publish_meeting_keyboard, \
    admin_meeting_property_keyboard
from loader import dp, bot
from misc.misc_classes import Meeting, BotContainer
from misc.misc_functions import admin_check


MEETING_STORAGE = BotContainer("m")

"""
    FSM scenario for scheduling meeting
"""


@dp.callback_query_handler(lambda c: c.data == "admin_manage_meeting", state=None)
@admin_check
async def admin_manage_meetings(call: CallbackQuery, **kwargs):
    # Show existing meetings
    for meeting in collection_meetings.find({}):
        meeting_data = meeting["data"]
        # Generate message text for a meeting
        meeting_text = f"\n{meeting_data['topic']}. {meeting_data['meeting_date']}, {meeting_data['meeting_time']}." \
                       f"\n{meeting_data['location']}\n{meeting_data['comment']}\n"
        # Send message with meeting information
        await bot.send_message(call.from_user["id"], meeting_text,
                               reply_markup=create_pm_keyboard(f"admin_pick_{meeting['_id']}"))    # will it work?
    # Send message with meetings management interface
    await bot.send_message(call.from_user["id"], get_message_prompt("msg_manual_meeting"),
                           reply_markup=admin_manage_meeting_keyboard)  # create_meeting, stop_assigning


@dp.callback_query_handler(lambda c: c.data == "admin_create_meeting" or c.data.startswith("admin_pick"), state=None)
@admin_check
async def admin_edit_meeting(call: CallbackQuery, **kwargs):
    # Set FSM to edit state
    FSMAdminSchedule.scenario_scheduling.set()
    # Create Meeting object and add it to container
    try:
        if call.data.startswith("admin_pick"):
            meeting = Meeting(call.from_user["id"], int(call.data.replace("admin_pick_", "")))
        else:
            meeting = Meeting(call.from_user["id"], random.randint(100, 999))
            meeting.create_empty_meeting()
        MEETING_STORAGE.add_object(meeting)
        await bot.send_message(call.from_user["id"], get_message_prompt(f"msg_schedule_0"),
                               reply_markup=admin_meeting_property_keyboard)
    except ValueError as e:
        print(e)


async def process_user_response(text: str, message):
    try:
        # Find profile in container
        meeting = MEETING_STORAGE.find_object(message.from_user["id"])
        # Process response
        if text != "skip_property":
            meeting.edit_property(message.text)
        meeting.cursor += 1
        # Send message with next question
        next_property = get_message_prompt(f"msg_schedule_{meeting.cursor}")
        await bot.send_message(message.from_user["id"], next_property,
                               reply_markup=admin_meeting_property_keyboard)
    except ValueError as err:
        print(err)
    except KeyError:
        meeting = MEETING_STORAGE.find_object(message.from_user["id"])
        await bot.send_message(message.from_user["id"], meeting.generate_meeting_text(),
                               reply_markup=admin_publish_meeting_keyboard)


@dp.message_handler(lambda m: m["from"]["id"] == m["chat"]["id"], state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_receive_response(message: Message, state: FSMContext, **kwargs):
    await process_user_response(message.text, message)


@dp.callback_query_handler(lambda c: c.data == "admin_skip_property", state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_skip_property(call: CallbackQuery, **kwargs):
    await process_user_response(call.data, call)


@dp.callback_query_handler(lambda c: c.data in ("admin_delete_meeting", "admin_stop_assigning"),
                           state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_delete_meeting(call: CallbackQuery, state: FSMContext, **kwargs):
    try:
        meeting = MEETING_STORAGE.find_object(call.from_user["id"])
        MEETING_STORAGE.remove_object(meeting)
        if call.data == "admin_delete_meeting":
            collection_meetings.delete_one({"_id": meeting.id_db})
        # Send notification message
        await bot.send_message(call.from_user["id"], get_message_prompt("msg_delete_meeting"))
        # Close FSM
        await state.finish()
    except ValueError as err:
        print(err)


@dp.callback_query_handler(lambda c: c.data == "admin_publish_meeting", state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def admin_publish_meeting(call: CallbackQuery, state: FSMContext, **kwargs):
    meeting = MEETING_STORAGE.find_object(call.from_user["id"])
    await bot.send_message(CHAT_ID, meeting.generate_meeting_text())
    await admin_delete_meeting(call, state)
