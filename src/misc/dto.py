import dataclasses





@dataclasses.dataclass
class CsmSteamMatchedSkin:
    steam_skin_dto: SteamSkinResponseDTO
    csm_skin_dto: CsmSkinResponseDTO
    price_percent: int

