import dataclasses

from src.scheduler_tasks.db_data_updater.dto.quality_dto import QualityDTO
from src.scheduler_tasks.db_data_updater.dto.skin_dto import SkinDTO
from src.scheduler_tasks.db_data_updater.dto.weapon_dto import WeaponDTO


@dataclasses.dataclass
class RelationDTO:
    weapon: WeaponDTO = None
    skin: SkinDTO = None
    quality: QualityDTO = None
