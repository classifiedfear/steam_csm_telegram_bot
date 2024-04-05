import typing

import sqlalchemy
from sqlalchemy.dialects import postgresql

from src.db.models import skins_models
from src.db.tables.table import Table


class WeaponSkinQualityTable(Table):
    async def create(self, weapon_id: int, skin_id: int, quality_id: int) -> None:
        insert_stmt = postgresql.insert(skins_models.WeaponSkinQuality).values(
            weapon_id=weapon_id, skin_id=skin_id, quality_id=quality_id
        )
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['weapon_id', 'skin_id', 'quality_id'], set_=dict(
                weapon_id=weapon_id, skin_id=skin_id, quality_id=quality_id
            )
        )
        await self._session.execute(do_update_stmt)
        await self._session.commit()

    async def create_many(self, relations_to_add: typing.List[typing.Dict[str, typing.Any]]) -> None:
        insert_stmt = postgresql.insert(skins_models.WeaponSkinQuality)
        on_conflict_stmt = insert_stmt.on_conflict_do_nothing()
        await self._session.execute(on_conflict_stmt, relations_to_add)
        await self._session.commit()

    async def get(self, weapon_id: int, skin_id: int, quality_id: int) -> skins_models.WeaponSkinQuality:
        stmt = sqlalchemy.select(skins_models.WeaponSkinQuality).where(
            skins_models.WeaponSkinQuality.weapon_id == weapon_id,
            skins_models.WeaponSkinQuality.skin_id == skin_id,
            skins_models.WeaponSkinQuality.quality_id == quality_id
        )
        return await self._session.scalar(stmt)

    async def get_relations(self):
        select_stmt = sqlalchemy.select(skins_models.WeaponSkinQuality)
        return await self._session.scalars(select_stmt)

    async def delete(self, weapon_id: int, skin_id: int, quality_id: int) -> None:
        stmt = sqlalchemy.delete(skins_models.WeaponSkinQuality).where(
            skins_models.WeaponSkinQuality.weapon_id == weapon_id,
            skins_models.WeaponSkinQuality.skin_id == skin_id,
            skins_models.WeaponSkinQuality.quality_id == quality_id
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_many_by_id(self, ids: typing.List[typing.Tuple[int, int, int]]) -> None:
        delete_stmt = sqlalchemy.delete(skins_models.WeaponSkinQuality)
        where_stmt = delete_stmt.where(
            sqlalchemy.tuple_(
                skins_models.WeaponSkinQuality.weapon_id,
                skins_models.WeaponSkinQuality.skin_id,
                skins_models.WeaponSkinQuality.quality_id
            ).in_(ids))
        await self._session.execute(where_stmt)
        await self._session.commit()

    async def update(self, *args, **kwargs):
        pass

    async def get_qualities_for_weapon_and_skin(self, weapon_id: int, skin_id: int):
        stmt = (
            sqlalchemy.select(skins_models.Quality)
            .join(skins_models.Quality.w_s_q)
            .join(skins_models.WeaponSkinQuality.weapon)
            .join(skins_models.WeaponSkinQuality.skin)
            .where(skins_models.Weapon.id == weapon_id, skins_models.Skin.id == skin_id)
        )
        return await self._session.scalars(stmt)

    async def get_random_weapon_from_db(self):
        stmt = (
            sqlalchemy.select(
                skins_models.Skin.name,
                skins_models.Weapon.name,
                skins_models.Quality.name,
                skins_models.Skin.stattrak_existence
            )
            .join(skins_models.Skin.w_s_q)
            .join(skins_models.WeaponSkinQuality.weapon)
            .join(skins_models.WeaponSkinQuality.quality)
            .order_by(sqlalchemy.func.random())
            .limit(1)
        )
        return await self._session.scalar(stmt)

