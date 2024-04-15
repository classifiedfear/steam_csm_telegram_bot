import typing
from typing import Type

import sqlalchemy
from sqlalchemy import ScalarResult
from sqlalchemy.dialects import postgresql

from src.database_app.database.models import skin_models
from src.database_app.database.models.skin_models import WeaponSkinQuality
from src.database_app.database.tables.abc_table.table import Table


class WeaponSkinQualityTable(Table):
    async def create(self, relation_model_data: typing.Dict[str, typing.Any]) -> skin_models.WeaponSkinQuality:
        model = skin_models.WeaponSkinQuality(**relation_model_data)
        await super().create(model)
        return model

    async def create_many(self, relation_models_data: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[skin_models.WeaponSkinQuality]:
        models = [skin_models.WeaponSkinQuality(**relation_model_data) for relation_model_data in relation_models_data]
        await super().create_many(models)
        return models

    async def get_by_id(self, weapon_id: int, skin_id: int, quality_id: int) -> Type[WeaponSkinQuality] | None:
        return await self._session.get(skin_models.WeaponSkinQuality, {
            "weapon_id": weapon_id,
            "skin_id": skin_id,
            "quality_id": quality_id
        })

    async def get_all(self) -> ScalarResult[WeaponSkinQuality]:
        select_stmt = sqlalchemy.select(skin_models.WeaponSkinQuality)
        return await self._session.scalars(select_stmt)

    async def delete_by_id(self, weapon_id: int, skin_id: int, quality_id: int) -> None:
        del_stmt = sqlalchemy.delete(skin_models.WeaponSkinQuality)
        where_stmt = del_stmt.where(
            skin_models.WeaponSkinQuality.weapon_id == weapon_id,
            skin_models.WeaponSkinQuality.skin_id == skin_id,
            skin_models.WeaponSkinQuality.quality_id == quality_id
        )
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def delete_many_by_id(self, ids: typing.List[typing.Tuple[int, int, int]]) -> None:
        delete_stmt = sqlalchemy.delete(skin_models.WeaponSkinQuality)
        where_stmt = delete_stmt.where(
            sqlalchemy.tuple_(
                skin_models.WeaponSkinQuality.weapon_id,
                skin_models.WeaponSkinQuality.skin_id,
                skin_models.WeaponSkinQuality.quality_id
            ).in_(ids))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def update_by_id(self, weapon_id: int, skin_id: int, quality_id: int, **values):
        relation = await self.get_by_id(weapon_id, skin_id, quality_id)
        relation.weapon_id = id if (id := values.get('weapon_id')) else relation.weapon_id
        relation.skin_id = id if (id := values.get('skin_id')) else relation.skin_id
        relation.quality_id = id if (id := values.get('quality_id')) else relation.quality_id
        await self._session.flush()
        return relation

    async def upsert(self, **values):
        stmt = postgresql.insert(skin_models.WeaponSkinQuality).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=['name'], set_=values)
        returning_stmt = do_update_stmt.returning(skin_models.WeaponSkinQuality)
        return await self._session.scalar(returning_stmt)

    async def get_qualities_for_weapon_and_skin(self, weapon_id: int, skin_id: int):
        stmt = (
            sqlalchemy.select(skin_models.Quality)
            .join(skin_models.Quality.w_s_q)
            .join(skin_models.WeaponSkinQuality.weapon)
            .join(skin_models.WeaponSkinQuality.skin)
            .where(skin_models.Weapon.id == weapon_id, skin_models.Skin.id == skin_id)
        )
        return await self._session.scalars(stmt)

    async def get_random_weapon_from_db(self):
        stmt = (
            sqlalchemy.select(
                skin_models.Skin.name,
                skin_models.Weapon.name,
                skin_models.Quality.name,
                skin_models.Skin.stattrak_existence
            )
            .join(skin_models.Skin.w_s_q)
            .join(skin_models.WeaponSkinQuality.weapon)
            .join(skin_models.WeaponSkinQuality.quality)
            .order_by(sqlalchemy.func.random())
            .limit(1)
        )
        return await self._session.scalar(stmt)

