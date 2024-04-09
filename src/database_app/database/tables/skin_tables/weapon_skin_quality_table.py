import typing

import sqlalchemy
from sqlalchemy.dialects import postgresql

from src.database_app.database.models import skin_models
from src.database_app.database.tables.abc_table.table import Table


class WeaponSkinQualityTable(Table):
    async def create(self, weapon_id: int, skin_id: int, quality_id: int) -> None:
        insert_stmt = postgresql.insert(skin_models.WeaponSkinQuality).values(
            weapon_id=weapon_id, skin_id=skin_id, quality_id=quality_id
        )
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['weapon_id', 'skin_id', 'quality_id'], set_=dict(
                weapon_id=weapon_id, skin_id=skin_id, quality_id=quality_id
            )
        )
        await self._session.execute(do_update_stmt)
        await self._session.commit()

    async def create_many(self, relations_to_add: typing.List[skin_models.WeaponSkinQuality]) -> None:
        self._session.add_all(relations_to_add)
        await self._session.commit()

    async def get(self, weapon_id: int, skin_id: int, quality_id: int) -> skin_models.WeaponSkinQuality:
        stmt = sqlalchemy.select(skin_models.WeaponSkinQuality).where(
            skin_models.WeaponSkinQuality.weapon_id == weapon_id,
            skin_models.WeaponSkinQuality.skin_id == skin_id,
            skin_models.WeaponSkinQuality.quality_id == quality_id
        )
        return await self._session.scalar(stmt)

    async def get_all(self):
        select_stmt = sqlalchemy.select(skin_models.WeaponSkinQuality)
        return await self._session.scalars(select_stmt)

    async def delete(self, weapon_id: int, skin_id: int, quality_id: int) -> None:
        stmt = sqlalchemy.delete(skin_models.WeaponSkinQuality).where(
            skin_models.WeaponSkinQuality.weapon_id == weapon_id,
            skin_models.WeaponSkinQuality.skin_id == skin_id,
            skin_models.WeaponSkinQuality.quality_id == quality_id
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_many_by_id(self, ids: typing.List[typing.Tuple[int, int, int]]) -> None:
        delete_stmt = sqlalchemy.delete(skin_models.WeaponSkinQuality)
        where_stmt = delete_stmt.where(
            sqlalchemy.tuple_(
                skin_models.WeaponSkinQuality.weapon_id,
                skin_models.WeaponSkinQuality.skin_id,
                skin_models.WeaponSkinQuality.quality_id
            ).in_(ids))
        await self._session.execute(where_stmt)
        await self._session.commit()

    async def update(self, *args, **kwargs):
        pass

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

