import dataclasses


@dataclasses.dataclass
class SteamSkinResponseDTO:
    name: str
    price: float
    link: str
    skin_float: float


@dataclasses.dataclass
class ParsedSteamSkinDTO:
    asset_id: int
    listing_id: int
    app_id: int
    context_id: int
    inspect_skin_link: str
    converted_price_per_unit: str
    converted_fee_per_unit: str

