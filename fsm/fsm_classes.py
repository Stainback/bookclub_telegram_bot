from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdminSchedule(StatesGroup):
    scenario_scheduling = State()


class FSMUserFillForm(StatesGroup):
    scenario_form = State()
    scenario_editing_form = State()
    scenario_removing_form = State()
