import logging

from aiogram.dispatcher import FSMContext

from aiogram.types import Message, CallbackQuery

from config import CHAT_ID
from fsm.fsm_classes import FSMUserFillForm
from keyboards import manage_form_keyboard, question_keyboard, publish_form_keyboard
from loader import dp, bot
from data_loader import collection_profiles, get_message_prompt
from misc import Profile, BotContainer

PROFILE_STORAGE = BotContainer("p")


"""
    FSM scenario for user form management   
"""


@dp.callback_query_handler(lambda c: c.data == "edit_form", state=None)
async def user_set_to_editing(call: CallbackQuery):
    # Create Profile object and add it to container
    profile = Profile(call.from_user["id"])
    try:
        PROFILE_STORAGE.add_object(profile)
    except ValueError as err:
        logging.warning(f"{__name__} - {user_set_to_editing.__name__} - {err}")
    # Check if user profile exists in db
    if collection_profiles.find_one({"_id": call.from_user["id"]}) is None:
        profile.create_empty_profile()
    # Send message with user management interface
    await bot.send_message(call.from_user["id"], get_message_prompt("msg_manual_userform"),
                           reply_markup=manage_form_keyboard)           # start_editing, clear_data, stop_editing


@dp.callback_query_handler(lambda c: c.data == "start_editing", state=None)
async def user_start_editing(call: CallbackQuery):
    # Set FSM to editing state
    FSMUserFillForm.scenario_form.set()
    # Send message with first question to user
    await bot.send_message(call.from_user["id"], get_message_prompt("msg_userform_0"),
                           reply_markup=question_keyboard)             # skip_question, stop_editing


async def process_user_response(text: str, message):
    try:
        # Find profile in container
        profile = PROFILE_STORAGE.find_object(message.from_user["id"])
        # Process response
        if text != "skip_question":
            profile.edit_form_field(message.text)
        profile.cursor += 1
        # Send message with next question
        next_question = profile.form[f"msg_userform_{profile.cursor}"]
        await bot.send_message(message.from_user["id"], next_question,
                               reply_markup=question_keyboard)          # skip_question, stop_editing
    except ValueError as err:
        logging.warning(f"{__name__} - {process_user_response.__name__} - {err}")
    except KeyError:
        profile = PROFILE_STORAGE.find_object(message.from_user["id"])
        await bot.send_message(message.from_user["id"], profile.generate_form_text(),
                               reply_markup=publish_form_keyboard)


@dp.message_handler(lambda m: m["from"]["id"] == m["chat"]["id"], state=FSMUserFillForm.scenario_form)
async def user_receive_response(message: Message):
    await process_user_response(message.text, message)


@dp.callback_query_handler(lambda c: c.data == "skip_question", state=FSMUserFillForm.scenario_form)
async def user_skip_question(call: CallbackQuery):
    await process_user_response(call.data, call)


@dp.callback_query_handler(lambda c: c.data == "clear_form_data", state=None)
async def user_clear_form_data(call: CallbackQuery):
    try:
        profile = PROFILE_STORAGE.find_object(call.from_user["id"])
        collection_profiles.delete_one({"_id": call.from_user["id"]})
        profile.create_empty_profile()
        logging.info(f"Profile data {profile.id_num} has been cleared.")
        # Send notification message
        await bot.send_message(call.from_user["id"], get_message_prompt("msg_clear_userform"),
                               reply_markup=manage_form_keyboard)  # start_editing, clear_data, stop_editing
    except ValueError as err:
        logging.warning(f"{__name__} - {user_clear_form_data.__name__} - {err}")


@dp.callback_query_handler(lambda c: c.data == "stop_editing", state="*")
async def user_stop_editing(call: CallbackQuery, state: FSMContext):
    try:
        profile = PROFILE_STORAGE.find_object(call.from_user["id"])
        PROFILE_STORAGE.remove_object(profile)
        # Send notification message
        await bot.send_message(call.from_user["id"], get_message_prompt("msg_stop_userform"))
        # Close FSM
        await state.finish()
    except ValueError as err:
        logging.warning(f"{__name__} - {user_stop_editing.__name__} - {err}")


@dp.callback_query_handler(lambda c: c.data == "publish_form", state=FSMUserFillForm.scenario_form)
async def publish_form(call: CallbackQuery, state: FSMContext):
    profile = PROFILE_STORAGE.find_object(call.from_user["id"])
    profile_msg = await bot.send_message(CHAT_ID, profile.generate_form_text())
    # Write form message id to db
    collection_profiles.update_one({"_id": profile.id_num}, {"$set": {"form": {"form_id": profile_msg["id"]}}})
    logging.info(f"Profile form {profile.id_num} has been published.")
    await user_stop_editing(call, state)

