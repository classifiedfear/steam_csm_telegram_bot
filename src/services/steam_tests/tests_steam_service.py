
import json
from typing import List

import pytest

from src.services.misc.dto import SkinRequestDTO
from src.services.steam.resources.dto import SteamSkinResponseDTO

from src.misc.link_tools import Pager
from src.services.steam.steam_market_skin_data_retriever import SteamMarketSkinDataRetriever


@pytest.fixture()
def m4a1_s_skin_dto():
    return SkinRequestDTO('M4A1-S', 'Hyper Beast', 'Field-Tested', False)


def return_value():
    with open('mocked_m4a4_data.json', 'r') as file:
        return json.load(file)


@pytest.fixture()
def service():
    service = SteamMarketSkinDataRetriever()
    return service

@pytest.mark.asyncio
#@patch.object(CommonRequestExecutor, 'get_response_json', return_value=return_value())
async def test_should_get_skin_data_from_api_steam_service(m4a1_s_skin_dto, service):
    result = await service.get_market_skins(m4a1_s_skin_dto)
    _should_equal_tuple_with_steam_skin_dto_instances(result)

@pytest.mark.skip
@pytest.mark.asyncio
async def test_should_get_skins_from_service_more_than_one_page(m4a1_s_skin_dto, service):
    for _ in range(3):
        result = await service.get_market_skins(m4a1_s_skin_dto)
        _should_equal_tuple_with_steam_skin_dto_instances(result)
@pytest.mark.skip
@pytest.mark.asyncio
async def test_should_get_skins_from_service_with_offset_100(m4a1_s_skin_dto, service):
    pager = Pager(100)
    result = await service.get_market_skins(m4a1_s_skin_dto, start=pager.offset, count=pager.get_next_offset())
    _should_equal_tuple_with_steam_skin_dto_instances(result)


def _should_equal_tuple_with_steam_skin_dto_instances(result: List[SteamSkinResponseDTO]):
    for skin in result:
        assert isinstance(skin, SteamSkinResponseDTO)
        assert skin.name == 'M4A1-S | Hyper Beast (Field-Tested)'
        assert isinstance(skin.price, float)
        assert skin.link.startswith(
            'https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Hyper%20Beast%20%28Field-Tested%29?'
        )
        assert isinstance(skin.skin_float, float)

