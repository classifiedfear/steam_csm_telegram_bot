import json

from aiohttp import ClientSession
from fake_useragent import UserAgent

from src.services.cs_skins_data_retriever import links
from src.services.cs_skins_data_retriever.links.csm_wiki_link_creator import CsSkinDataLink
from src.services.cs_skins_data_retriever import parsers
from src.services.misc.common_request_executor import CommonRequestExecutor
from src.services.cs_skins_data_retriever.resources import graphql_queries


class CsInfoService:
    def __init__(self):
        self._headers = {'user-agent': f'{UserAgent.random}'}

    async def get_weapons(self):
        async with ClientSession() as session:
            async with session.get(links.CsWeaponsDataLink.create(), headers=self._headers) as response:
                response_text = await response.text()
                return parsers.WeaponsParser.parse(response_text)

    async def get_skins_for_weapon(self, weapon: str):
        if weapon[0] != "★":
            return await self._get_skins_for_weapon(weapon)
        else:
            return await self._get_skins_for_knife(weapon)

    async def _get_skins_for_weapon(self, weapon: str):
        async with ClientSession() as session:
            async with session.get(links.CsSkinsForWeaponkLink.create(weapon), headers=self._headers) as response:
                response_text = await response.text()
                return parsers.SkinsForWeaponParser.parse(response_text)

    async def _get_skins_for_knife(self, knife: str):
        async with ClientSession() as session:
            async with session.get(links.CsSkinsForWeaponkLink.create(knife[2:]), headers=self._headers) as response:
                response_text = await response.text()
                return parsers.SkinsForKnifeParser.parse(response_text)

    async def get_qualities_for_weapon_and_skin(self, weapon: str, skin: str):
        get_min_available = self._prep_query(weapon, skin)
        async with ClientSession() as session:
            async with session.post(links.CsSkinDataLink.create(), json=get_min_available) as response:
                response_text = await response.text()
                return parsers.QualitiesParser.parse(response_text)

    async def get_stattrak_existence_for_weapon_and_skin(self, weapon: str, skin: str):
        get_min_available = self._prep_query(weapon, skin)
        async with ClientSession() as session:
            async with session.post(links.CsSkinDataLink.create(), json=get_min_available) as response:
                response_text = await response.text()
                return parsers.StatTrakParser.parse(response_text)

    async def get_info_for_weapon_and_skin(self, weapon: str, skin: str):
        get_min_available = self._prep_query(weapon, skin)
        async with ClientSession() as session:
            async with session.post(links.CsSkinDataLink.create(), json=get_min_available) as response:
                response_text = await response.text()
                stattrak_existence = parsers.StatTrakParser.parse(response_text)
                qualities = parsers.QualitiesParser.parse(response_text)
                return stattrak_existence, qualities

    @staticmethod
    def _prep_query(weapon: str, skin: str):
        get_min_available = graphql_queries.get_min_available
        get_min_available['variables']['name'] = f'{weapon} | {skin}'
        return get_min_available

