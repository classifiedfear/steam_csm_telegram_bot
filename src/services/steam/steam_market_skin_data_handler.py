from src.services.misc.dto import SkinRequestDTO
from src.services.steam.links.steam_market_skin_data_link import SteamMarketSkinDataLink
from src.services.steam.steam_market_skin_data_parser import ParsedSteamSkinDTO


class SteamMarketSkinDataHandler:
    @staticmethod
    def get_buy_link(parsed: ParsedSteamSkinDTO, skin_dto: SkinRequestDTO) -> str:
        base_root = SteamMarketSkinDataLink().create(skin_dto)
        return (base_root + f'?filter=#buylisting|'
                            f'{parsed.listing_id}|'
                            f'{parsed.app_id}|'
                            f'{parsed.context_id}|'
                            f'{parsed.asset_id}'
                )

    @staticmethod
    def get_price(parsed: ParsedSteamSkinDTO) -> float:
        price = str(parsed.converted_price_per_unit + parsed.converted_fee_per_unit)
        price = price[0:-2] + '.' + price[-2:]
        return float(price)

    @staticmethod
    def get_inspect_link(parsed: ParsedSteamSkinDTO) -> str:
        return (
            parsed.inspect_skin_link
            .replace("%listingid%", str(parsed.listing_id))
            .replace('%assetid%', str(parsed.asset_id))
        )

