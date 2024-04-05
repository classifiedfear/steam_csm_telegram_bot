import dataclasses


@dataclasses.dataclass
class CsmSkinResponseDTO:
    name: str
    skin_float: float
    price: float
    price_with_float: float
    overpay_float: float
