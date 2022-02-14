from aiogram.dispatcher import FSMContext

from aiogram.types import Message, CallbackQuery

from config import CHAT_ID
from data_loader import update_bot_data
from fsm.fsm_classes import FSMUserFillForm
from keyboards import cancel_form_keyboard, save_form_keyboard, approve_form_removal_keyboard
from loader import dp, bot, PROFILE_DATA, MESSAGE_DATA
from misc import Profile


async def find_profile(user_input, state: FSMContext):
    """
        Looks for profile which is owned by input sender. If such profile has not been found, create one.
    """
    for profile in PROFILE_DATA:
        if profile.data["user_id"] == user_input.from_user["id"]:
            return profile
    new_profile = Profile()
    new_profile.data["user_id"] = user_input.from_user["id"]
    new_profile.data["username"] = user_input.from_user["username"]
    PROFILE_DATA.append(new_profile)
    update_bot_data([[_profile.data, _profile.form] for _profile in PROFILE_DATA], "data/data_profiles.json")
    return new_profile


"""
    FSM scenario for meeting scheduling
    
    Form operation algorythm: start operation -> /ask question -> get answer -> load into Form dict/ ->
                                        (cycle until questions left, can be interrupted with cancel or edit command) 
                              -> load Form dict into json -> publish generated form message -> 
                              -> update Profile with member name, birth date and form message id
    Operation can be cancelled or redacted only by form owner. Form can be deleted only by form owner or admins.
"""


@dp.callback_query_handler(lambda c: c.data == "edit_form", state="*")
async def set_form_to_edit_mode(call: CallbackQuery, state: FSMContext, **kwargs):
    await FSMUserFillForm.scenario_form.set()
    profile = await find_profile(call, state)
    if profile.scenario_count == 0:
        await bot.send_message(call.from_user["id"], MESSAGE_DATA[f"msg_instructions_userform"])
    await bot.send_message(call.from_user["id"], MESSAGE_DATA[f"msg_userform_{profile.scenario_count}"],
                           reply_markup=cancel_form_keyboard)


@dp.message_handler(lambda m: m["from"]["id"] == m["chat"]["id"], state=FSMUserFillForm.scenario_form)
async def load_answer(message: Message, state: FSMContext, **kwargs):
    profile = await find_profile(message, state)
    if message.text.lower().replace('"', '') == "пропустить":
        profile.scenario_count += 1
    else:
        profile.fill_form_field(message.text)  # scenario_count += 1
    while profile.scenario_count <= len(profile.form_questions) - 1:
        await bot.send_message(message.from_user["id"],
                               f"{MESSAGE_DATA[f'msg_userform_{profile.scenario_count}']}\n"
                               f"\t{profile.get_current_answer() or 'Ответ еще не дан.'}",
                               reply_markup=cancel_form_keyboard)
        return

    # Move to "save form" stage if form goes out of unanswered questions
    await bot.send_message(message.from_user["id"], f"{profile.generate_form_message()}\n"
                                                    f"Хотите сохранить вашу анкету?",
                           reply_markup=save_form_keyboard)


@dp.callback_query_handler(lambda c: c.data == "save_send_form", state=FSMUserFillForm.scenario_form)
async def save_form(call: CallbackQuery, state: FSMContext, **kwargs):
    # Publish meeting
    profile = await find_profile(call, state)
    form_message = await bot.send_message(CHAT_ID, profile.generate_form_message())
    profile.data["form_id"] = form_message.from_user["id"]
    # Update file with meeting data
    update_bot_data([[_profile.data, _profile.form] for _profile in PROFILE_DATA], "data/data_profiles.json")
    # Send notification message
    await bot.send_message(call.from_user["id"], "Анкета была успешно сохранена.")
    # Finish scenario
    await state.finish()


"""
    FSM scenario for meeting removal
"""


@dp.callback_query_handler(lambda c: c.data == "remove_form", state="*")
async def start_removal_form(call: CallbackQuery, **kwargs):
    # Set FSM to removing state
    await FSMUserFillForm.scenario_removing_form.set()
    # Ask user to approve
    await bot.send_message(call.from_user["id"], "Вы уверены, что хотите стереть данные из вашей анкеты?",
                           reply_markup=approve_form_removal_keyboard)


@dp.callback_query_handler(lambda c: c.data == "remove_form_approved", state=FSMUserFillForm.scenario_removing_form)
async def remove_form(call: CallbackQuery, state: FSMContext, **kwargs):
    # Remove the form from form storage
    profile = await find_profile(call, state)
    if profile is not None:
        profile.erase_answers()
        update_bot_data([[_profile.data, _profile.form] for _profile in PROFILE_DATA], "data/data_profiles.json")
        # Send notification message
        await bot.send_message(call["from"]["id"], "Ваша анкета была очищена.")
        # Finish removal scenario
        await state.finish()


@dp.callback_query_handler(lambda c: c.data in ("cancel_removal", "cancel_form"),
                           state=FSMUserFillForm.scenario_removing_form)
async def cancel_operation(call: CallbackQuery, state: FSMContext, **kwargs):
    # Send notification message
    msg = {"cancel_removal": "Операция была отменена.", "cancel_form": "Заполнение анкеты было отложено."}
    await bot.send_message(call.from_user["id"], msg[call.data])
    # Finish scenario
    await state.finish()
