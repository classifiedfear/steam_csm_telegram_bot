import asyncio
import pickle

import aiohttp
import brotli

from src.services.cs_skins_data_retriever.cs_skin_data_retriever import CsInfoService
from src.database_skins_filler.data_tree_from_source import DataTreeFromSource, WeaponsSkinsQualitiesDTO, \
    WeaponFromSource, SkinFromSource


class DBFiller:
    def __init__(self, csgo_database_service_parser: CsInfoService):
        self._csgo_database_service_parser = csgo_database_service_parser
        self._first_source_semaphore = asyncio.Semaphore(20)
        self._second_source_semaphore = asyncio.Semaphore(30)

    async def seed(self):
        tasks = []
        data_tree = DataTreeFromSource()
        weapons = data_tree.add_weapons(await self._csgo_database_service_parser.get_weapons())
        for weapon in weapons:
            tasks.append(asyncio.create_task(self._parse_skins(weapon, data_tree)))
        await asyncio.gather(*tasks)
        print(len(data_tree.all_skins))
        print(len(data_tree.all_relations))
        await self._send_update_to_db(data_tree.to_dto())

    async def _parse_skins(self, weapon: WeaponFromSource, data_tree: DataTreeFromSource):
        async with self._first_source_semaphore:
            tasks = []
            skins = data_tree.add_skins(
                await self._csgo_database_service_parser.get_skins_for_weapon(weapon.name)
            )
            for skin in skins:
                tasks.append(asyncio.create_task(self._parse_qualities(weapon, skin, data_tree)))
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _parse_qualities(self, weapon: WeaponFromSource, skin: SkinFromSource, data_tree: DataTreeFromSource):
        async with self._second_source_semaphore:
            stattrak_existance, qualities = await self._csgo_database_service_parser.get_info_for_weapon_and_skin(
                weapon.name, skin.name,
            )
            qualities = data_tree.add_qualities(qualities)
            skin.stattrak_existence = stattrak_existance
            for quality in qualities:
                data_tree.add_relation(weapon, skin, quality)

    @staticmethod
    async def _send_update_to_db(db_dto: WeaponsSkinsQualitiesDTO):
        async with aiohttp.ClientSession() as session:
            bytes_db_dto = pickle.dumps(db_dto)
            compressed_db_dto = brotli.compress(bytes_db_dto)
            async with session.post('http://127.0.0.1:8000/update_db', data=compressed_db_dto) as response:
                assert response.status == 200







