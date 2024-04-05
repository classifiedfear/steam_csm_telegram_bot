from aiogram import Router, F
from aiogram.fsm import context

from aiogram import types
from aiogram.fsm.context import FSMContext
from apscheduler import AsyncScheduler, ScheduleLookupError
from apscheduler.triggers.interval import IntervalTrigger

from src.telegram_bot_app.handlers import TgMsgHandler
from src.telegram_bot_app import states
from src.telegram_bot_app.resources.constants import buttons_const

class OperationHandler(TgMsgHandler):
    def __init__(self, router: Router, scheduler: AsyncScheduler):
        self._router = router

    async def handle(self) -> None:
        @self._router.message(F.text == buttons_const.ADD_TO_TRACK)
        async def add_to_track(message: types.Message, state: FSMContext):
            await state.set_state(states.SettingStates.CHOOSE_WEAPON)
            await message.answer('Пожалуйста выберете оружие')


