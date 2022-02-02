from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from data_loader import update_mbot_data
from keyboards import admin_cscheduling_keyboard
from loader import dp, bot, MEETING_DATA
from misc.misc_functions import admin_check, generate_meeting_message


class FSMAdminSchedule(StatesGroup):
    location = State()
    meeting_date = State()
    meeting_time = State()
    topic = State()
    comment = State()


data = {}


@dp.message_handler(commands="cancel_sch", state="*")
@admin_check
async def cancel_schedule_operation(message: Message, state: FSMContext):
    if await state.get_state() in ("FSMAdminSchedule:location", "FSMAdminSchedule:meeting_time",
                                   "FSMAdminSchedule:meeting_date", "FSMAdminSchedule:topic"):
        await bot.send_message(message["from"]["id"], "Operation has been canceled.")

    elif await state.get_state() == "FSMAdminSchedule:comment":
        data["comment"] = ""
        data["meeting_id"] = data["meeting_date"].replace("-", "") + data["meeting_time"].replace(":", "")

        MEETING_DATA.append(data)
        update_mbot_data(MEETING_DATA)

        await bot.send_message(message["from"]["id"], f"Meeting has been created. \n {generate_meeting_message(data)}")

    await state.finish()


# FSM scenario for meeting scheduling
@dp.message_handler(commands="schedule", state=None)
@admin_check
async def start_meeting_scheduling(message: Message):

    await FSMAdminSchedule.location.set()

    await bot.send_message(message["from"]["id"], "Enter meeting location (place name, address)",
                           reply_markup=admin_cscheduling_keyboard)


@dp.message_handler(state=FSMAdminSchedule.location)
@admin_check
async def fill_location(message: Message):

    data["location"] = message.text

    await FSMAdminSchedule.meeting_date.set()
    await bot.send_message(message["from"]["id"], "Enter meeting date in format YYYY-MM-DD",
                           reply_markup=admin_cscheduling_keyboard)


@dp.message_handler(state=FSMAdminSchedule.meeting_date)
@admin_check
async def fill_date(message: Message):

    data["meeting_date"] = message.text

    await FSMAdminSchedule.meeting_time.set()
    await bot.send_message(message["from"]["id"], "Enter meeting time in format HH:MM",
                           reply_markup=admin_cscheduling_keyboard)


@dp.message_handler(state=FSMAdminSchedule.meeting_time)
@admin_check
async def fill_date(message: Message):

    data["meeting_time"] = message.text

    await FSMAdminSchedule.topic.set()
    await bot.send_message(message["from"]["id"], "Enter meeting topic (book, author, etc.)",
                           reply_markup=admin_cscheduling_keyboard)


@dp.message_handler(state=FSMAdminSchedule.topic)
@admin_check
async def fill_date(message: Message):

    data["topic"] = message.text

    await FSMAdminSchedule.comment.set()
    await bot.send_message(message["from"]["id"], "Enter any additional comment here. Press 'Cancel' to skip comment.",
                           reply_markup=admin_cscheduling_keyboard)


@dp.message_handler(state=FSMAdminSchedule.comment)
@admin_check
async def fill_date(message: Message, state: FSMContext):

    data["comment"] = message.text
    data["meeting_id"] = data["meeting_date"].replace("-", "") + data["meeting_time"].replace(":", "")

    MEETING_DATA.append(data)
    update_mbot_data(MEETING_DATA)

    await bot.send_message(message["from"]["id"], f"Meeting has been created. \n {generate_meeting_message(data)}")

    await state.finish()

