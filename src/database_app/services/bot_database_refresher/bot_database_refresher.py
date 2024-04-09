import pickle
import typing
from collections import namedtuple
import brotli
from src.database_app.database.context.bot_database_context import BotDatabaseContext
from src.database_app.database.models import skin_models
from src.database_app.database.tables.skin_tables.quality_table import QualityTable
from src.database_app.database.tables.skin_tables.skin_table import SkinTable
from src.database_app.database.tables.skin_tables.weapon_table import WeaponTable
from src.scheduler_tasks.db_data_updater.dto.quality_dto import QualityDTO
from src.scheduler_tasks.db_data_updater.dto.received_data_from_tree_dto import ReceivedDataFromTreeDTO
from src.scheduler_tasks.db_data_updater.dto.relation_dto import RelationDTO
from src.scheduler_tasks.db_data_updater.dto.skin_dto import SkinDTO
from src.scheduler_tasks.db_data_updater.dto.weapon_dto import WeaponDTO


class BotDatabaseRefresher:
    def __init__(self, context: BotDatabaseContext):
        self._weapon_table = context.get_weapon_table()
        self._skin_table = context.get_skin_table()
        self._quality_table = context.get_quality_table()
        self._relations_table = context.get_weapon_skin_quality_table()

    async def refresh(self, request: bytes):
        db_dto = self._deserialize_request(request)
        await self._refresh_db(db_dto)

    @staticmethod
    def _deserialize_request(request: bytes):
        to_unpickle = brotli.decompress(request)
        return pickle.loads(to_unpickle)

    async def _refresh_db(self, db_dto: ReceivedDataFromTreeDTO):
        await self._update_weapons(db_dto.weapons)
        await self._update_skins(db_dto.skins)
        await self._update_qualities(db_dto.qualities)
        await self._update_relations(db_dto.relations)

    async def _update_weapons(self, weapons: typing.List[WeaponDTO]):
        weapons_dto_to_create, weapons_to_delete = await self._get_items_dto_to_create_and_names_to_delete(
            weapons, self._weapon_table
        )
        weapon_models_to_create = [skin_models.Weapon(name=item.name) for item in weapons_dto_to_create.values()]
        if weapons_to_delete:
            await self._weapon_table.delete_many_by_name(weapons_to_delete)
        if weapon_models_to_create:
            await self._weapon_table.create_many(weapon_models_to_create)

        self._correct_ids_for_items_dto_by_models(weapons_dto_to_create, weapon_models_to_create)

    async def _update_skins(self, skins: typing.List[SkinDTO]):
        skins_dto_to_create, skin_names_to_delete = await self._get_items_dto_to_create_and_names_to_delete(
            skins, self._skin_table
        )
        skin_models_to_create = [
            skin_models.Skin(name=item.name, stattrak_existence=item.stattrak_existence)
            for item in skins_dto_to_create.values()
        ]
        if skin_names_to_delete:
            await self._skin_table.delete_many_by_name(skin_names_to_delete)
        if skin_models_to_create:
            await self._skin_table.create_many(skin_models_to_create)

        self._correct_ids_for_items_dto_by_models(skins_dto_to_create, skin_models_to_create)

    async def _update_qualities(self, qualities: typing.List[QualityDTO]):
        qualities_dto_to_create, quality_names_to_delete = await self._get_items_dto_to_create_and_names_to_delete(
            qualities, self._quality_table
        )
        quality_model_to_create = [skin_models.Quality(name=item.name) for item in qualities_dto_to_create.values()]
        if quality_names_to_delete:
            await self._quality_table.delete_many_by_name(quality_names_to_delete)
        if qualities_dto_to_create:
            await self._quality_table.create_many(quality_model_to_create)

        self._correct_ids_for_items_dto_by_models(qualities_dto_to_create, quality_model_to_create)

    @staticmethod
    async def _get_items_dto_to_create_and_names_to_delete(
            items: typing.List[WeaponDTO | SkinDTO | QualityDTO],
            table: WeaponTable | SkinTable | QualityTable
    ):
        item_dto_to_create = {item.name: item for item in items}
        item_names_to_delete = []
        for item_db_model in await table.get_all():
            if item_dto := item_dto_to_create.pop(item_db_model.name, None):
                item_dto.id = item_db_model.id
            else:
                item_names_to_delete.append(item_db_model.name)
        return item_dto_to_create, item_names_to_delete

    @staticmethod
    def _correct_ids_for_items_dto_by_models(items_dto, items_models):
        for item_model in items_models:
            items_dto[item_model.name].id = item_model.id

    async def _update_relations(self, relations: typing.List[RelationDTO]):
        ids_relations_to_create, ids_relations_to_delete = await self._get_ids_relations_to_create_and_delete(relations)
        wsq_model_relations_to_create = [
            skin_models.WeaponSkinQuality(
                weapon_id=relation.weapon_id, skin_id=relation.skin_id, quality_id=relation.quality_id
            )
            for relation in ids_relations_to_create
        ]

        if ids_relations_to_delete:
            await self._relations_table.delete_many_by_id(ids_relations_to_delete)

        if wsq_model_relations_to_create:
            await self._relations_table.create_many(wsq_model_relations_to_create)

    async def _get_ids_relations_to_create_and_delete(self, relations: typing.List[RelationDTO]):
        relation_tuple = namedtuple('Relation', ['weapon_id', 'skin_id', 'quality_id'])
        ids_relations_to_create = {
            relation_tuple(relation.weapon.id, relation.skin.id, relation.quality.id) for relation in relations
        }
        ids_relations_to_delete = []
        for relation_db_model in await self._relations_table.get_all():
            if (relation_id_tuple := (
                    relation_db_model.weapon_id,
                    relation_db_model.skin_id,
                    relation_db_model.quality_id
            )) in ids_relations_to_create:
                ids_relations_to_create.remove(relation_id_tuple)
            else:
                ids_relations_to_delete.append(relation_id_tuple)
        return ids_relations_to_create, ids_relations_to_delete
