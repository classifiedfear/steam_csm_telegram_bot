import asyncio

from typing import List

from src.services.csm.links.csm_market_skin_asset_id_link import CsmMarketSkinAssetIdLink
from src.services.csm.links.csm_market_skin_data_link import CsmMarketSkinDataLink
from src.services.csm.parsers.csm_market_skin_asset_id_parser import CsmMarketSkinAssetIdParser
from src.services.csm.parsers.csm_market_skin_data_parser import CsmMarketSkinDataParser
from src.services.misc.common_request_executor import CommonRequestExecutor
from src.services.csm.resources.dto import CsmSkinResponseDTO
from src.services.misc.dto import SkinRequestDTO


class CsmMarketSkinDataRetriever:
    def __init__(self, request_executor: CommonRequestExecutor) -> None:
        self._request_executor = request_executor
        self._headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en,ru;q=0.9',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

    async def get_market_skins(self, skin_dto: SkinRequestDTO, *, offset: int = 0) -> List[CsmSkinResponseDTO]:
        """Parse 1 page from csm_tests"""
        asset_id_list = await self._get_asset_ids(skin_dto, offset)
        return await self._get_skins(asset_id_list)

    async def _get_asset_ids(self, skin_dto: SkinRequestDTO, offset: int) -> List[int]:
        link = CsmMarketSkinAssetIdLink.create(skin_dto, limit=60, offset=offset)
        response = await self._request_executor.get_response_json(link)
        return CsmMarketSkinAssetIdParser.parse(response)

    async def _get_skins(self, asset_id_list: List[int]) -> List[CsmSkinResponseDTO]:
        tasks = []
        for asset_id in asset_id_list:
            link = CsmMarketSkinDataLink.create(asset_id)
            tasks.append(asyncio.create_task(self._request_executor.get_response_json(link)))
        responses = await asyncio.gather(*tasks)
        return [CsmMarketSkinDataParser.parse(response) for response in responses]

