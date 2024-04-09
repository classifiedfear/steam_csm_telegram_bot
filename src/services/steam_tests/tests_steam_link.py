import pytest

from src.misc.constants import tests_const
from src.services.misc.dto import SkinRequestDTO
from src.services.steam.links.api_steam_market_skin_data_link import ApiSteamMarketSkinDataLink
from src.services.steam.links.steam_market_skin_data_link import SteamMarketSkinDataLink


@pytest.mark.parametrize(
    ('skin_dto', 'expected'),
    (
        (SkinRequestDTO('AK-47', 'Asiimov', 'Field-Tested', True), tests_const.RESULT_STEAM_AK_47_LINK),
        (SkinRequestDTO('Desert Eagle', 'Code Red', 'Field-Tested', False), tests_const.RESULT_STEAM_DESERT_EAGLE_LINK)
    )
)
def test_should_create_link_for_steam(skin_dto, expected):
    result = SteamMarketSkinDataLink.create(skin_dto)
    assert result == expected


@pytest.mark.parametrize(
    ('skin_dto', 'expected'),
    (
        (SkinRequestDTO('AK-47', 'Asiimov', 'Field-Tested', True), tests_const.RESULT_STEAM_API_AK_47_LINK),
        (SkinRequestDTO('Desert Eagle', 'Code Red', 'Field-Tested', False), tests_const.RESULT_STEAM_API_DESERT_EAGLE_LINK)
    )
)
def test_should_create_link_for_steam_api(skin_dto, expected):
    result = ApiSteamMarketSkinDataLink.create(skin_dto, count=100)
    assert result == expected

