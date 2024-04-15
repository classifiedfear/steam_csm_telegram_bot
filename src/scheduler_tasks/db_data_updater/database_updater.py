import asyncio
import pickle

import aiohttp
import brotli

from src.scheduler_tasks.db_data_updater.dto.received_data_from_tree_dto import ReceivedDataFromTreeDTO
from src.scheduler_tasks.db_data_updater.dto.skin_dto import SkinDTO
from src.scheduler_tasks.db_data_updater.dto.weapon_dto import WeaponDTO
from src.services.cs_skins_data_retriever.cs_skin_data_retriever import CsInfoService
from src.scheduler_tasks.db_data_updater.data_tree_from_source import DataTreeFromSource


class DbUpdater:
    def __init__(self, csgo_database_service_parser: CsInfoService):
        self._csgo_database_service_parser = csgo_database_service_parser
        self._first_source_semaphore = asyncio.Semaphore(20)
        self._second_source_semaphore = asyncio.Semaphore(30)

    async def update(self):
        datatree = DataTreeFromSource()
        await self._process_datatree(datatree)
        await self._send_update_to_db(datatree.to_dto())

    async def _process_datatree(self, datatree: DataTreeFromSource):
        tasks = []
        weapons = datatree.add_weapons(await self._csgo_database_service_parser.get_weapons())
        for weapon in weapons:
            task = asyncio.create_task(self._process_weapon_in_datatree(datatree, weapon))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def _process_weapon_in_datatree(self, datatree: DataTreeFromSource, weapon: WeaponDTO):
        async with self._first_source_semaphore:
            tasks = []
            skins = datatree.add_skins(
                await self._csgo_database_service_parser.get_skins_for_weapon(weapon.name)
            )
            for skin in skins:
                task = asyncio.create_task(self._process_weapon_skin_in_datatree(datatree, weapon, skin))
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _process_weapon_skin_in_datatree(
            self, datatree: DataTreeFromSource, weapon: WeaponDTO, skin: SkinDTO,
    ):
        async with self._second_source_semaphore:
            stattrak_existence, qualities = await self._csgo_database_service_parser.get_info_for_weapon_and_skin(
                weapon.name, skin.name,
            )
            qualities = datatree.add_qualities(qualities)
            skin.stattrak_existence = stattrak_existence
            for quality in qualities:
                datatree.add_relation(weapon, skin, quality)

    @staticmethod
    async def _send_update_to_db(db_dto: ReceivedDataFromTreeDTO):
        async with aiohttp.ClientSession() as session:
            bytes_db_dto = pickle.dumps(db_dto)
            compressed_db_dto = brotli.compress(bytes_db_dto)
            async with session.post('http://127.0.0.1:8000/services/update_db', data=compressed_db_dto) as response:
                assert response.status == 200
