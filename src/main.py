import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler import AsyncScheduler
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore

from redis import asyncio as aioredis

from src.database_app.database.context.bot_database_context import BotDatabaseContext
from src.redis_controller import RedisController
from src.telegram_bot_app import handlers
from src.telegram_bot_app.keyboard.keyboard_utils import KeyboardCreator
from src.telegram_bot_app.keyboard.keyboards import Keyboards
from src.telegram_bot_app.midlewares.register_check import RegisterCheck
from src.telegram_bot_app.resources.constants import buttons_const
from src.test_db import BotDatabase
def create_test_db():
    url = (
        f'postgresql+asyncpg://'
        f'{os.getenv('postgres_user')}:{os.getenv('postgres_password')}@{os.getenv('host')}:'
        f'{os.getenv('postgres_port')}/{os.getenv('postgres_db_name')}'
    )
    return BotDatabaseContext(url)

class Application:
    def __init__(self, database: BotDatabase, keyboard: Keyboards) -> None:
        self._redis = aioredis.Redis(host=os.getenv('host'), decode_responses=True)
        self._redis_controller = RedisController(self._redis)
        self._dp = Dispatcher(storage=RedisStorage(self._redis))
        self._bot = Bot(token=os.getenv('token'), parse_mode=ParseMode.HTML)
        self._keyboards = keyboard
        self._database = database
        self._construct_keyboard()

    def _construct_keyboard(self):
        keyboards = {
            'main_menu': KeyboardCreator.create_reply_keyboard(buttons_const.MAIN_MENU_KEYBOARD_TEXT_LIST),
            'back': KeyboardCreator.create_reply_keyboard([buttons_const.BACK]),
            'stattrak_settings': KeyboardCreator.create_reply_keyboard(buttons_const.STATTRAK_SETTING_LIST)
        }
        for name, keyboard in keyboards.items():
            self._keyboards.add_keyboard(name, keyboard)

    async def __init_handlers(self, scheduler: AsyncScheduler) -> handlers.TgMsgCompositeHandler:
        general_handler = handlers.TgMsgCompositeHandler()
        async with create_test_db() as db:
            db.get_weapon_table()
            settings_handler = handlers.SettingHandler(self._keyboards, self._database, self._redis_controller)
            command_handler = handlers.TgCommandMsgHandler(self._keyboards, RegisterCheck(self._redis_controller, self._database))
            general_handler.add(command_handler).add(settings_handler)
        return general_handler

    async def main(self) -> None:
        data_store = SQLAlchemyDataStore(engine=self._database.engine)
        async with AsyncScheduler(data_store=data_store) as scheduler:
            await self._database.proceed_schemas()
            general_handler = await self.__init_handlers(scheduler)
            await general_handler.handle()
            self._dp.include_routers(*general_handler.router)
            await scheduler.start_in_background()
            await self._dp.start_polling(self._bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    url = (
        f'postgresql+asyncpg://'
        f'{os.getenv('postgres_user')}:{os.getenv('postgres_password')}@{os.getenv('host')}:'
        f'{os.getenv('postgres_port')}/{os.getenv('postgres_db_name')}'
    )
    db = BotDatabase(url)
    kb = Keyboards()
    app = Application(db, kb)
    try:
        asyncio.run(app.main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped!')



