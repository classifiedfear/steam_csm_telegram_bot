from src.misc.constants import link_const

from src.misc.link_tools import LinkBuilder
from src.services.misc.dto import SkinRequestDTO
from src.services.steam.links.steam_market_skin_data_link import SteamMarketSkinDataLink


class ApiSteamMarketSkinDataLink(SteamMarketSkinDataLink):
    @staticmethod
    def create(skin_dto: SkinRequestDTO, *, start: int = 0, count: int = 10, currency: int = 1) -> str:
        return (
            LinkBuilder(link_const.STEAM_MARKET_LINK_BASE_ROOT)
            .add_part_link(ApiSteamMarketSkinDataLink._stattrak_link_part(skin_dto))
            .add_part_link(ApiSteamMarketSkinDataLink._weapon_link_part(skin_dto))
            .add_part_link(ApiSteamMarketSkinDataLink._skin_link_part(skin_dto))
            .add_part_link(ApiSteamMarketSkinDataLink._quality_link_part(skin_dto))
            .add_part_link('/render/')
            .add_param('query', '')
            .add_param('start', str(start))
            .add_param('count', str(count))
            .add_param('currency', str(currency))
            .build()
        )

