from src.misc.constants import link_const

from src.misc.link_tools import LinkBuilder
from src.services.misc.dto import SkinRequestDTO


class SteamMarketSkinDataLink:
    @staticmethod
    def create(skin_dto: SkinRequestDTO) -> str:
        return (LinkBuilder(link_const.STEAM_MARKET_LINK_BASE_ROOT)
                .add_part_link(SteamMarketSkinDataLink._stattrak_link_part(skin_dto))
                .add_part_link(SteamMarketSkinDataLink._weapon_link_part(skin_dto))
                .add_part_link(SteamMarketSkinDataLink._skin_link_part(skin_dto))
                .add_part_link(SteamMarketSkinDataLink._quality_link_part(skin_dto))
                .build()
                )

    @staticmethod
    def _weapon_link_part(skin_dto: SkinRequestDTO):
        return '%20'.join(skin_dto.weapon.split()) + '%20%7C%20'

    @staticmethod
    def _skin_link_part(skin_dto: SkinRequestDTO):
        return '%20'.join(skin_dto.skin.split()) + '%20%28'

    @staticmethod
    def _quality_link_part(skin_dto: SkinRequestDTO):
        if ('Factory New' or 'Minimal Wear') in skin_dto.quality:
            return '%20'.join(skin_dto.quality.split()) + '%29'
        return skin_dto.quality + '%29'

    @staticmethod
    def _stattrak_link_part(skin_dto: SkinRequestDTO):
        return 'StatTrak\u2122%20' if skin_dto.stattrak else ''
