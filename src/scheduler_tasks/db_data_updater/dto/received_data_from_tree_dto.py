import dataclasses
import typing

from src.scheduler_tasks.db_data_updater.dto.quality_dto import QualityDTO
from src.scheduler_tasks.db_data_updater.dto.relation_dto import RelationDTO
from src.scheduler_tasks.db_data_updater.dto.skin_dto import SkinDTO
from src.scheduler_tasks.db_data_updater.dto.weapon_dto import WeaponDTO


@dataclasses.dataclass
class ReceivedDataFromTreeDTO:
    weapons: typing.List[WeaponDTO]
    skins: typing.List[SkinDTO]
    qualities: typing.List[QualityDTO]
    relations: typing.List[RelationDTO]
