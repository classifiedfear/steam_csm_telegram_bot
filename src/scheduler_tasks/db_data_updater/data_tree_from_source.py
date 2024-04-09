from __future__ import annotations
import typing
from collections import defaultdict
from typing import List

from src.scheduler_tasks.db_data_updater.dto.quality_dto import QualityDTO
from src.scheduler_tasks.db_data_updater.dto.received_data_from_tree_dto import ReceivedDataFromTreeDTO
from src.scheduler_tasks.db_data_updater.dto.relation_dto import RelationDTO
from src.scheduler_tasks.db_data_updater.dto.skin_dto import SkinDTO
from src.scheduler_tasks.db_data_updater.dto.weapon_dto import WeaponDTO


class DataTreeFromSource:
    def __init__(self):
        self._all_weapons = defaultdict(WeaponDTO)
        self._all_skins = defaultdict(SkinDTO)
        self._all_qualities = defaultdict(QualityDTO)
        self._all_relations = defaultdict(RelationDTO)

    def add_weapons(self, weapon_names: List[str]) -> typing.List[WeaponDTO]:
        return self._add_items(weapon_names, self._all_weapons)

    def add_skins(self, skin_names: List[str]) -> typing.List[SkinDTO]:
        return self._add_items(skin_names, self._all_skins)

    def add_qualities(self, quality_names: List[str]) -> typing.List[QualityDTO]:
        return self._add_items(quality_names, self._all_qualities)

    @staticmethod
    def _add_items(
            names: List[str],
            dictionary_with_items: typing.Dict[str, WeaponDTO | SkinDTO | QualityDTO]
    ) -> typing.List[WeaponDTO | SkinDTO | QualityDTO]:
        items = []
        for name in names:
            item = dictionary_with_items[name]
            if not item.name:
                item.name = name
            items.append(item)
        return items

    def add_relation(
            self, weapon: WeaponDTO, skin: SkinDTO, quality: QualityDTO
    ) -> None:
        relation = self._all_relations[(weapon.name, skin.name, quality.name)]
        relation.weapon = weapon
        relation.skin = skin
        relation.quality = quality

    def to_dto(self) -> ReceivedDataFromTreeDTO:
        return ReceivedDataFromTreeDTO(
            list(self._all_weapons.values()),
            list(self._all_skins.values()),
            list(self._all_qualities.values()),
            list(self._all_relations.values())
        )
