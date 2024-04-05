import pickle
import typing
import logging

import brotli
import fastapi
from ..dependencies import db
from ...database_skins_filler.data_tree_from_source import WeaponsSkinsQualitiesDTO, WeaponFromSource, SkinFromSource, \
    QualityFromSource, RelationFromSource
from ...db.bot_database import BotDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

update_db_router = fastapi.APIRouter(
    prefix="/update_db",
    tags=["update_db"],
    dependencies=[fastapi.Depends(db.get_db_all_tables)]
)


class AppDbService:
    def __init__(self, tables: BotDatabase):
        self._weapon_table = tables.get_weapon_table()
        self._skin_table = tables.get_skin_table()
        self._quality_table = tables.get_quality_table()
        self._weapon_skin_quality_table = tables.get_weapon_skin_quality_table()

    async def refresh_db(self, request: bytes):
        logging.info(f"Refreshing database")
        db_dto = self._deserialize_request(request)
        await self._refresh_db(db_dto)

    @staticmethod
    def _deserialize_request(request: bytes):
        to_unpickle = brotli.decompress(request)
        return pickle.loads(to_unpickle)

    async def _refresh_db(self, db_dto: WeaponsSkinsQualitiesDTO):
        await self._update_weapons(db_dto.weapons)
        await self._update_skins(db_dto.skins)
        await self._update_qualities(db_dto.qualities)
        await self._update_relations(db_dto.relations)

    async def _update_weapons(self, weapons: typing.List[WeaponFromSource]):
        weapon_dto_to_create = {weapon.name: weapon for weapon in weapons}
        weapons_to_delete = []
        for weapon_db_model in await self._weapon_table.get_weapons():
            if weapon_dto := weapon_dto_to_create.pop(weapon_db_model.name, None):
                weapon_dto.id = weapon_db_model.id
            else:
                weapons_to_delete.append(weapon_db_model.name)
        if weapons_to_delete:
            await self._weapon_table.delete_many_by_name(weapons_to_delete)
        if weapon_dto_to_create:
            logging.info(len(weapon_dto_to_create))
            await self._weapon_table.create_many(
                [
                    {
                        #"id": item.id,
                        "name": item.name
                    }
                    for item in weapon_dto_to_create.values()
                ]
            )

    async def _update_skins(self, skins: typing.List[SkinFromSource]):
        skins_dto_to_create = {skin.name: skin for skin in skins}
        skins_to_delete = []
        for skin_db_model in await self._skin_table.get_skins():
            if skin_dto := skins_dto_to_create.pop(skin_db_model.name, None):
                skin_dto.id = skin_db_model.id
            else:
                skins_to_delete.append(skin_db_model.name)
        if skins_to_delete:
            await self._skin_table.delete_many_by_name(skins_to_delete)
        if skins_dto_to_create:
            logging.info(len(skins_dto_to_create))
            await self._skin_table.create_many(
                [
                    {
                        #"id": item.id,
                        "name": item.name,
                        "stattrak_existence": item.stattrak_existence
                    } for item in skins_dto_to_create.values()
                ]
            )

    async def _update_qualities(self, qualities: typing.List[QualityFromSource]):
        qualities_dto_to_create = {quality.name: quality for quality in qualities}
        qualities_to_delete = []
        for quality_db_model in await self._quality_table.get_qualities():
            if quality_dto := qualities_dto_to_create.pop(quality_db_model.name, None):
                quality_dto.id = quality_db_model.id
            else:
                qualities_to_delete.append(quality_db_model.name)
        if qualities_to_delete:
            await self._quality_table.delete_many_by_name(qualities_to_delete)
        if qualities_dto_to_create:
            await self._quality_table.create_many(
                [
                    {
                        #"id": item.id,
                        "name": item.name
                    } for item in qualities_dto_to_create.values()
                ]
            )

    async def _update_relations(self, relations: typing.List[RelationFromSource]):
        ids_relations_to_create = {(relation.weapon.id, relation.skin.id, relation.quality.id) for relation in relations}
        ids_relations_to_delete = []
        for relation_db_model in await self._weapon_skin_quality_table.get_relations():
            if (relation_id_tuple := (
                        relation_db_model.weapon_id,
                        relation_db_model.skin_id,
                        relation_db_model.quality_id
            )) in ids_relations_to_create:
                ids_relations_to_create.remove(relation_id_tuple)
            else:
                ids_relations_to_delete.append(relation_id_tuple)

        if ids_relations_to_delete:
            await self._weapon_skin_quality_table.delete_many_by_id(ids_relations_to_delete)

        if ids_relations_to_create:
            logging.info(len(ids_relations_to_create))
            await self._weapon_skin_quality_table.create_many(
                [
                    {
                        "weapon_id": weapon_id,
                        "skin_id": skin_id,
                        "quality_id": quality_id
                    } for weapon_id, skin_id, quality_id in ids_relations_to_create
                ]
            )


@update_db_router.post("")
async def update_db(request: fastapi.Request, tables: BotDatabase = fastapi.Depends(db.get_db_all_tables)):
    db_service = AppDbService(tables)
    await db_service.refresh_db(await request.body())



