import typing

import sqlalchemy
from sqlalchemy.dialects import postgresql

from src.db.models import skins_models
from src.db.tables.table import Table


class WeaponTable(Table):
    async def create(self, **values) -> int:
        insert_stmt = postgresql.insert(skins_models.Weapon).values(**values)
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['name'], set_=values)
        returning_stmt = do_update_stmt.returning(skins_models.Weapon.id)
        result = await self._session.execute(returning_stmt)
        await self._session.commit()
        return result.scalar()

    async def create_many(self, weapons_to_add: typing.List[typing.Dict[str, typing.Any]]):
        stmt = postgresql.insert(skins_models.Weapon)
        do_nothing_stmt = stmt.on_conflict_do_nothing()
        await self._session.execute(do_nothing_stmt, weapons_to_add)
        await self._session.commit()

    async def get(self, id: int) -> skins_models.Weapon:
        stmt = sqlalchemy.select(skins_models.Weapon).where(skins_models.Weapon.id == id)
        return await self._session.scalar(stmt)

    async def get_by_name(self, name: str) -> skins_models.Weapon:
        stmt = sqlalchemy.select(skins_models.Weapon).where(skins_models.Weapon.name == name)
        return await self._session.scalar(stmt)

    async def delete(self, id: int) -> None:
        stmt = sqlalchemy.delete(skins_models.Weapon).where(skins_models.Weapon.id == id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_by_name(self, name: str) -> None:
        stmt = sqlalchemy.delete(skins_models.Weapon).where(skins_models.Weapon.name == name)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_many_by_name(self, names: typing.List[str]):
        delete_stmt = sqlalchemy.delete(skins_models.Weapon)
        where_stmt = delete_stmt.where(skins_models.Weapon.name.in_(names))
        await self._session.execute(where_stmt)

    async def update(self, id: int, **values):
        stmt = sqlalchemy.update(skins_models.Weapon).where(skins_models.Weapon.id == id).values(**values)
        await self._session.execute(stmt)
        await self._session.commit()

    async def update_by_name(self, name: str, **values):
        stmt = sqlalchemy.update(skins_models.Weapon).where(skins_models.Weapon.name == name).values(**values)
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_weapons(self) -> sqlalchemy.ScalarResult[skins_models.Weapon]:
        stmt = sqlalchemy.select(skins_models.Weapon)
        return await self._session.scalars(stmt)

    async def get_skins_for_weapon(self, name: str) -> sqlalchemy.ScalarResult[skins_models.Skin]:
        stmt = (
            sqlalchemy.select(skins_models.Skin)
            .join(skins_models.Skin.w_s_q)
            .join(skins_models.WeaponSkinQuality.weapon)
            .where(skins_models.Weapon.name == name)
        )
        without_duplicate_stmt = stmt.distinct()
        return await self._session.scalars(without_duplicate_stmt)
