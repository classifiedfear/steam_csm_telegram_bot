from __future__ import annotations
import dataclasses
from collections import defaultdict
from typing import List


class DataTreeFromSource:
    def __init__(self):
        self.all_weapons = defaultdict(WeaponFromSource)
        self.all_skins = defaultdict(SkinFromSource)
        self.all_qualities = defaultdict(QualityFromSource)
        self.all_relations = defaultdict(RelationFromSource)
        self._weapon_counter = 0
        self._skin_counter = 0
        self._quality_counter = 0

    def add_weapons(self, weapon_names: List[str]):
        return self._add_items(weapon_names, self.all_weapons, self._weapon_counter)

    def add_skins(self, skin_names: List[str]):
        return self._add_items(skin_names, self.all_skins, self._skin_counter)

    def add_qualities(self, quality_names: List[str]):
        return self._add_items(quality_names, self.all_qualities, self._quality_counter)

    @staticmethod
    def _add_items(names: List[str], dictionary_with_items, counter: int):
        items = []
        for name in names:
            item = dictionary_with_items[name]
            if not item.name:
                item.name = name
            if not item.id:
                counter += 1
                item.id = counter
            items.append(item)
        return items

    def add_relation(
            self, weapon: WeaponFromSource, skin: SkinFromSource, quality: QualityFromSource
    ):
        item = self.all_relations[(weapon.name, skin.name, quality.name)]
        item.weapon = weapon
        item.skin = skin
        item.quality = quality

    def to_dto(self):
        return WeaponsSkinsQualitiesDTO(
            list(self.all_weapons.values()),
            list(self.all_skins.values()),
            list(self.all_qualities.values()),
            list(self.all_relations.values())
        )


@dataclasses.dataclass
class WeaponFromSource:
    name: str = None
    id: int = 0


@dataclasses.dataclass
class SkinFromSource:
    name: str = None
    stattrak_existence: bool = False
    id: int = 0


@dataclasses.dataclass
class QualityFromSource:
    name: str = None
    id: int = 0


@dataclasses.dataclass
class RelationFromSource:
    weapon: WeaponFromSource = None
    skin: SkinFromSource = None
    quality: QualityFromSource = None

@dataclasses.dataclass
class WeaponsSkinsQualitiesDTO:
    weapons: List[WeaponFromSource]
    skins: List[SkinFromSource]
    qualities: List[QualityFromSource]
    relations: List[RelationFromSource]

