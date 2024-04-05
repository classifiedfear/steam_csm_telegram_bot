import dataclasses


@dataclasses.dataclass
class SkinRequestDTO:
    weapon: str
    skin: str
    quality: str
    stattrak: bool