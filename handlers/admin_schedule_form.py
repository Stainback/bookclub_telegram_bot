from aiogram.dispatcher import FSMContext

from aiogram.types import Message, CallbackQuery

from data_loader import update_mbot_data
from fsm.fsm_classes import FSMAdminSchedule
from keyboards import admin_cscheduling_keyboard
from loader import dp, bot, MESSAGE_DATA, MEETING_DATA
from misc.misc_classes import Meeting
from misc.misc_functions import admin_check, generate_meeting_message


# FSM scenario for meeting scheduling
@dp.callback_query_handler(lambda c: c.data == "schedule_meeting", state=None)
@admin_check
async def start_meeting_scheduling(call: CallbackQuery, **kwargs):

    # Instantiate an FSM
    await FSMAdminSchedule.scenario_scheduling.set()

    # Instantiate a new meeting and add it to MEETING_DATA
    MEETING_DATA.append(Meeting())
    print(MEETING_DATA)

    # Send information message in personal chat
    await bot.send_message(call.from_user["id"], MESSAGE_DATA["msg_schedule_00"+str(MEETING_DATA[-1].scenario_count + 1)],
                           reply_markup=admin_cscheduling_keyboard)


@dp.message_handler(state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def load_meeting_property(message: Message, state: FSMContext, **kwargs):
    """
       Function triggers every time when comes message from admin with active scheduling scenario FSM state.

       Meeting object has scenario stage counter. On each of stages (ending with 5th stage) bot is waiting for
       a response from admin with corresponding data. On 5th stage admin should put a comment or skip this stage using
       "cancel" function.
    """
    print(MEETING_DATA[-1])

    if MEETING_DATA[-1].scenario_count < 4:

        MEETING_DATA[-1].fill_property(message.text)

        await bot.send_message(message.from_user["id"],
                               MESSAGE_DATA["msg_schedule_00"+str(MEETING_DATA[-1].scenario_count + 1)],
                               reply_markup=admin_cscheduling_keyboard)

    elif MEETING_DATA[-1].scenario_count == 4:

        MEETING_DATA[-1].fill_property(message.text)
        MEETING_DATA[-1].generate_meeting_id()
        update_mbot_data(MEETING_DATA)

        await bot.send_message(message.from_user["id"], f"Meeting has been created. \n"
                                                        f" {generate_meeting_message(MEETING_DATA[-1].data)}")
        await state.finish()


@dp.callback_query_handler(lambda c: c.data == "admin_cancel_scheduling", state=FSMAdminSchedule.scenario_scheduling)
@admin_check
async def cancel_schedule_operation(call: CallbackQuery, state: FSMContext, **kwargs):
    if MEETING_DATA[-1].scenario_count < 4:

        MEETING_DATA.pop(-1)
        await bot.send_message(call.from_user["id"], "Operation has been canceled.")
        print(MEETING_DATA)

    elif MEETING_DATA[-1].scenario_count == 4:

        MEETING_DATA[-1].fill_property("")
        MEETING_DATA[-1].generate_meeting_id()
        update_mbot_data(MEETING_DATA)

        await bot.send_message(call.from_user["id"], f"Meeting has been created. \n"
                                                     f" {generate_meeting_message(MEETING_DATA[-1].data)}")
    await state.finish()
