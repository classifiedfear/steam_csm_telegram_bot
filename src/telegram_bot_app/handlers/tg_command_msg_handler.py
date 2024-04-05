import aiogram
from aiogram import types, Router
from aiogram import filters


from src.telegram_bot_app.handlers.handlers import TgMsgHandler
from src.telegram_bot_app.keyboard.keyboards import Keyboards
from src.telegram_bot_app.midlewares.register_check import RegisterCheck
from src.telegram_bot_app.resources import constants


class TgCommandMsgHandler(TgMsgHandler):
    def __init__(self, keyboards: Keyboards, middleware: RegisterCheck) -> None:
        self._router = Router()
        self._router.message.middleware(middleware)
        self._keyboards = keyboards

    async def handle(self):
        @self._router.message(filters.CommandStart())
        async def command_start(message: types.Message) -> None:
            await message.answer(
                text=f'Привет, {message.from_user.full_name}',
                reply_markup=self._keyboards.get_keyboard('main_menu')
            )