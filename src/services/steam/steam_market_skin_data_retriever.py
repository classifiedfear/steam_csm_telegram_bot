import asyncio
from typing import List

import aiohttp
from fake_useragent import UserAgent

from src.services.misc.dto import SkinRequestDTO
from src.services.steam.resources.dto import SteamSkinResponseDTO, ParsedSteamSkinDTO
from src.services.steam.steam_market_skin_data_handler import SteamMarketSkinDataHandler
from src.services.steam.links.api_steam_market_skin_data_link import ApiSteamMarketSkinDataLink
from src.services.steam.steam_market_skin_data_parser import SteamMarketSkinDataParser


class SteamMarketSkinDataRetriever:
    def __init__(self):
        self._headers = {
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en,ru;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'steamcommunity.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Prototype-Version': '1.7',
            'X-Requested-With': 'XMLHttpRequest',
            'user-agent': f'{UserAgent.random}'
            }

    async def get_market_skins(
            self, skin_dto: SkinRequestDTO, *, start: int = 0, count: int = 10, currency: int = 1
    ) -> List[SteamSkinResponseDTO]:
        steam_skins = await self._get_steam_skins(skin_dto, start, count, currency)
        return await self._get_skins(steam_skins, skin_dto)

    async def _get_steam_skins(
            self, skin_dto: SkinRequestDTO, start: int, count: int, currency: int) -> List[ParsedSteamSkinDTO]:
        link = ApiSteamMarketSkinDataLink.create(skin_dto, start=start, count=count, currency=currency)
        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers=self._headers) as response:
                json_response = await response.json()
                return SteamMarketSkinDataParser.parse(json_response)

    async def _get_skins(
            self, steam_skins_info: List[ParsedSteamSkinDTO], skin_dto: SkinRequestDTO
    ) -> List[SteamSkinResponseDTO]:
        tasks = []
        for parsed_skin_dto in steam_skins_info:
            tasks.append(asyncio.create_task(self._get_skin(parsed_skin_dto, skin_dto)))
        return [skin for skin in await asyncio.gather(*tasks)]

    async def _get_skin(self, steam_skin_info: ParsedSteamSkinDTO, skin_dto: SkinRequestDTO) -> SteamSkinResponseDTO:
        inspect_link = SteamMarketSkinDataHandler.get_inspect_link(steam_skin_info)
        skin_info = await self._find_skin_info(inspect_link)
        buy_link = SteamMarketSkinDataHandler.get_buy_link(steam_skin_info, skin_dto)
        skin_price = SteamMarketSkinDataHandler.get_price(steam_skin_info)
        return SteamSkinResponseDTO(skin_info['full_item_name'], skin_price, buy_link, skin_info['floatvalue'])

    @staticmethod
    async def _find_skin_info(inspect_link: str):
        link = 'https://api.csfloat.com/?url=' + inspect_link
        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers={'Origin': 'https://csfloat.com'}) as response:
                response_json = await response.json()
                return response_json['iteminfo']
