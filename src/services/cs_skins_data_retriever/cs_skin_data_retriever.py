import json

from src.services.cs_skins_data_retriever import links
from src.services.cs_skins_data_retriever.links.csm_wiki_link_creator import CsSkinDataLink
from src.services.cs_skins_data_retriever import parsers
from src.services.misc.common_request_executor import CommonRequestExecutor
from src.services.cs_skins_data_retriever.resources import graphql_queries


class CsInfoService:
    def __init__(self, common_request_executor: CommonRequestExecutor):
        self._common_request_executor = common_request_executor

    async def get_weapons(self):
        response = await self._common_request_executor.get_response_text(
            links.CsWeaponsDataLink.create()
        )
        return parsers.WeaponsParser.parse(response)

    async def get_skins_for_weapon(self, weapon: str):
        if weapon[0] != "★":
            return await self._get_skins_for_weapon(weapon)
        else:
            return await self._get_skins_for_knife(weapon)

    async def _get_skins_for_weapon(self, weapon: str):
        response = await self._common_request_executor.get_response_text(
            links.CsSkinsForWeaponkLink.create(weapon)
        )
        return parsers.SkinsForWeaponParser.parse(response)

    async def _get_skins_for_knife(self, knife: str):
        response = await self._common_request_executor.get_response_text(
            links.CsSkinsForWeaponkLink.create(knife[2:])
        )
        return parsers.SkinsForKnifeParser.parse(response)

    async def get_qualities_for_weapon_and_skin(self, weapon: str, skin: str):
        get_min_available = self._prep_query(weapon, skin)
        response = await self._common_request_executor.post_response_text(
            CsSkinDataLink.create(), get_min_available
        )
        return parsers.QualitiesParser.parse(response)

    async def get_stattrak_existence_for_weapon_and_skin(self, weapon: str, skin: str):
        get_min_available = self._prep_query(weapon, skin)
        response = await self._common_request_executor.post_response_text(
            CsSkinDataLink.create(), get_min_available
        )
        return parsers.StatTrakParser.parse(response)

    async def get_info_for_weapon_and_skin(self, weapon: str, skin: str):
        get_min_available = self._prep_query(weapon, skin)
        response = await self._common_request_executor.post_response_text(
            CsSkinDataLink.create(), get_min_available
        )
        stattrak_existence = parsers.StatTrakParser.parse(response)
        qualities = parsers.QualitiesParser.parse(response)
        return stattrak_existence, qualities

    @staticmethod
    def _prep_query(weapon: str, skin: str):
        get_min_available = graphql_queries.get_min_available
        get_min_available['variables']['name'] = f'{weapon} | {skin}'
        return get_min_available

