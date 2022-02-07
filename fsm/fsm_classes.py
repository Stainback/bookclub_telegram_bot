from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdminSchedule(StatesGroup):
    scenario_scheduling = State()


class FSMAdminRemove(StatesGroup):
    scenario_removing = State()
