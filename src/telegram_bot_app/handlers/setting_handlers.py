from __future__ import annotations

import types

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram import types

from src.db.bot_database import BotDatabase
from src.redis_controller import RedisController
from src.telegram_bot_app.handlers import TgMsgHandler
from src.telegram_bot_app.keyboard.keyboards import Keyboards
from src.telegram_bot_app import states
from src.telegram_bot_app.resources import constants


class SettingHandler(TgMsgHandler):
    def __init__(
            self, keyboards: Keyboards, database: BotDatabase, redis_controller: RedisController
    ) -> None:
        self._router = Router()
        self._database = database
        self._keyboards = keyboards
        self._redis_controller = redis_controller

    async def handle(self) -> None:
        @self._router.message(F.text == constants.buttons_const.ADD_TO_TRACK)
        async def add_to_track(message: types.Message, state: FSMContext):
            await state.set_state(states.SettingStates.CHOOSE_WEAPON)
            weapons = await self._database.get_weapons()
            weapon_string = self._construct_setting_message('оружие', weapons)
            await message.answer(weapon_string, reply_markup=self._keyboards.get_keyboard('back'))

        @self._router.message(states.SettingStates.CHOOSE_WEAPON, lambda message: message.text.isdigit())
        async def add_to_track_weapon(message: types.Message, state: FSMContext):
            weapon_id = int(message.text)
            await state.set_data({"weapon_id": weapon_id})
            await state.set_state(states.SettingStates.CHOOSE_SKIN)
            skins = await self._database.get_skins_for_weapon(weapon_id)
            skin_string = self._construct_setting_message('скин', set(skins))
            await message.answer(skin_string, reply_markup=self._keyboards.get_keyboard('back'))

        @self._router.message(states.SettingStates.CHOOSE_SKIN, lambda message: message.text.isdigit())
        async def add_to_track_skin(message: types.Message, state: FSMContext):
            await state.update_data(skin_id=int(message.text))
            data = await state.get_data()
            await state.set_state(states.SettingStates.CHOOSE_QUALITY)
            qualities = await self._database.get_qualities_for_weapon(data['weapon_id'], data['skin_id'])
            quality_string = self._construct_setting_message('качество', qualities)
            await message.answer(quality_string, reply_markup=self._keyboards.get_keyboard('back'))

        @self._router.message(states.SettingStates.CHOOSE_QUALITY, lambda message: message.text.isdigit())
        async def add_to_track_quality(message: types.Message, state: FSMContext):
            await state.update_data(quality_id=int(message.text))
            data = await state.get_data()
            await state.set_state(states.SettingStates.CHOOSE_STATTRAK)
            stattrak = await self._database.get_stattrak_for_skin(data['skin_id'])
            if stattrak:
                await state.set_state(states.SettingStates.CHOOSE_STATTRAK)
                await message.answer('Какой вариант скина искать?', reply_markup=self._keyboards.get_keyboard('stattrak_settings'))
            else:
                await self._database.subscribe_weapon_to_user(
                    message.from_user.id, data['weapon_id'], data['skin_id'], data['quality_id'], stattrak
                )

        @self._router.message(states.SettingStates.CHOOSE_STATTRAK, lambda message: message.text in constants.buttons_const.STATTRAK_SETTING_LIST)
        async def add_to_track_stattrak(message: types.Message, state: FSMContext):
            stattrak = constants.buttons_const.STATTRAK_SETTING_LIST.index(message.text)
            await state.update_data({"stattrak": bool(stattrak) if stattrak != 2 else None})
            data = await state.get_data()
            await self._database.subscribe_weapon_to_user(message.from_user.id, data['weapon_id'], data['skin_id'], data['quality_id'], data['stattrak'])
            await state.clear()
            await message.answer('Скин добавлен', reply_markup=self._keyboards.get_keyboard('main_menu'))

    @staticmethod
    def _construct_setting_message(weapon_part: str, items):
        setting_message = f"Выберите {weapon_part} и введите его число!\n"
        for item in items:
            setting_message += f"{item.id}) {item.name}\n"
        return setting_message








