from aiogram.fsm.state import StatesGroup, State


class SettingStates(StatesGroup):
    CHOOSE_WEAPON = State()
    CHOOSE_SKIN = State()
    CHOOSE_QUALITY = State()
    CHOOSE_STATTRAK = State()