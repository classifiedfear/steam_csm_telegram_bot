from decimal import localcontext, Decimal
from typing import Dict, Any

from src.services.csm.resources.dto import CsmSkinResponseDTO


class CsmMarketSkinDataParser:
    @staticmethod
    def parse(response: Dict[str, Any]) -> CsmSkinResponseDTO:
        name = response['fullName']
        price = CsmMarketSkinDataParser._get_price(response['defaultPrice'])
        overpay_float = response['overpay']['float']
        price_with_float = CsmMarketSkinDataParser._get_overpay_float_price(price, overpay_float)
        skin_float = float(response['float'])
        return CsmSkinResponseDTO(name, skin_float, price, price_with_float, overpay_float)

    @staticmethod
    def _get_price(unhandled_price: float) -> float:
        with localcontext() as context:
            price_with_csm_percent = unhandled_price - (unhandled_price / 100 * 8)
            context.prec = 4
            return float(Decimal(price_with_csm_percent) * 1)

    @staticmethod
    def _get_overpay_float_price(default_price: float, overpay_float: float) -> float:
        with localcontext() as context:
            context.prec = 4
            return float(Decimal(default_price + overpay_float) * 1)

