import typing

import sqlalchemy

from src.database_app.database.models import skin_models
from src.database_app.database.tables.abc_table.table import Table


class WeaponTable(Table):
    async def create(self, weapon: skin_models.Weapon) -> None:
        self._session.add(weapon)
        await self._session.commit()

    async def create_many(self, weapon_model_to_add: typing.List[skin_models.Weapon]):
        self._session.add_all(weapon_model_to_add)
        await self._session.commit()

    async def get(self, id: int) -> typing.Type[skin_models.Weapon] | None:
        return await self._session.get(skin_models.Weapon, id)

    async def get_by_name(self, name: str) -> skin_models.Weapon:
        stmt = sqlalchemy.select(skin_models.Weapon).where(skin_models.Weapon.name == name)
        return await self._session.scalar(stmt)

    async def delete(self, id: int) -> None:
        stmt = sqlalchemy.delete(skin_models.Weapon).where(skin_models.Weapon.id == id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_by_name(self, name: str) -> None:
        stmt = sqlalchemy.delete(skin_models.Weapon).where(skin_models.Weapon.name == name)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_many_by_id(self, ids: typing.List[int]) -> None:
        delete_stmt = sqlalchemy.delete(skin_models.Weapon)
        where_stmt = delete_stmt.where(skin_models.Weapon.id.in_(ids))
        await self._session.execute(where_stmt)

    async def delete_many_by_name(self, names: typing.List[str]):
        delete_stmt = sqlalchemy.delete(skin_models.Weapon)
        where_stmt = delete_stmt.where(skin_models.Weapon.name.in_(names))
        await self._session.execute(where_stmt)

    async def update(self, id: int, **values):
        stmt = sqlalchemy.update(skin_models.Weapon).where(skin_models.Weapon.id == id).values(**values)
        await self._session.execute(stmt)
        await self._session.commit()

    async def update_by_name(self, name: str, **values):
        stmt = sqlalchemy.update(skin_models.Weapon).where(skin_models.Weapon.name == name).values(**values)
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_all(self) -> sqlalchemy.ScalarResult[skin_models.Weapon]:
        stmt = sqlalchemy.select(skin_models.Weapon)
        return await self._session.scalars(stmt)

    async def get_skins_for_weapon(self, name: str) -> sqlalchemy.ScalarResult[skin_models.Skin]:
        stmt = (
            sqlalchemy.select(skin_models.Skin)
            .join(skin_models.Skin.w_s_q)
            .join(skin_models.WeaponSkinQuality.weapon)
            .where(skin_models.Weapon.name == name)
        )
        without_duplicate_stmt = stmt.distinct()
        return await self._session.scalars(without_duplicate_stmt)
