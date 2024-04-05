import logging

from typing import List, Dict, Any

from src.services.steam.exceptions import RequestException
from src.services.steam.resources.dto import ParsedSteamSkinDTO

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)


class SteamMarketSkinDataParser:
    @staticmethod
    def parse(response: Dict[str, Any]) -> List[ParsedSteamSkinDTO]:
        SteamMarketSkinDataParser._check_response(response)
        return SteamMarketSkinDataParser._find_skins_data(response['listinginfo'])

    @staticmethod
    def _check_response(response: Dict[str, Any]):
        if (response is None) or (not response['listinginfo']):
            raise RequestException('To many request')

    @staticmethod
    def _find_skins_data(listing: Dict[str, Any]) -> List[ParsedSteamSkinDTO]:
        return [SteamMarketSkinDataParser._find_skin(skin) for skin in listing.values()]

    @staticmethod
    def _find_skin(item: Dict[str, Any]) -> ParsedSteamSkinDTO:
        asset = item['asset']
        return ParsedSteamSkinDTO(
            int(asset['id']),
            int(item['listingid']),
            int(asset['appid']),
            int(asset['contextid']),
            asset['market_actions'][0]['link'],
            item['converted_price_per_unit'],
            item['converted_fee_per_unit'],
        )
