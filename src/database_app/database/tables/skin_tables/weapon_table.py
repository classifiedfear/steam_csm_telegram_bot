import typing

import sqlalchemy
from sqlalchemy.dialects import postgresql

from src.database_app.database.models import skin_models
from src.database_app.database.models.skin_models import Weapon
from src.database_app.database.tables.abc_table.table import Table


class WeaponTable(Table):
    async def create(self, weapon_model_data: typing.Dict[str, typing.Any]) -> skin_models.Weapon:
        model = skin_models.Weapon(**weapon_model_data)
        await super().create(model)
        return model

    async def get_by_id(self, id: int) -> typing.Type[skin_models.Weapon] | None:
        return await self._session.get(skin_models.Weapon, id)

    async def update_by_id(self, id: int, **values) -> typing.Type[skin_models.Weapon] | None:
        update_stmt = sqlalchemy.update(skin_models.Weapon).values(**values)
        where_stmt = update_stmt.where(skin_models.Weapon.id == id)
        returning_stmt = where_stmt.returning(skin_models.Weapon)
        weapon = await self._session.scalar(returning_stmt)
        await self._session.flush()
        return weapon

    async def delete_by_id(self, id: int) -> bool:
        if (weapon := await self.get_by_id(id)) is None:
            return False
        await self._session.delete(weapon)
        await self._session.flush()
        return True

    async def create_many(self, weapon_models_data: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[Weapon]:
        models = [skin_models.Weapon(**weapon_model) for weapon_model in weapon_models_data]
        await super().create_many(models)
        return models

    async def get_many_by_id(self, ids: typing.List[int]):
        select_stmt = sqlalchemy.select(skin_models.Weapon)
        where_stmt = select_stmt.where(skin_models.Weapon.id.in_(ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name(self, names: typing.List[str]):
        select_stmt = sqlalchemy.select(skin_models.Weapon)
        where_stmt = select_stmt.where(skin_models.Weapon.name.in_(names))
        return await self._session.scalars(where_stmt)

    async def delete_many_by_id(self, ids: typing.List[int]) -> None:
        delete_stmt = sqlalchemy.delete(skin_models.Weapon)
        where_stmt = delete_stmt.where(skin_models.Weapon.id.in_(ids))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def delete_many_by_name(self, item_names: typing.List[str]):
        delete_stmt = sqlalchemy.delete(skin_models.Weapon)
        where_stmt = delete_stmt.where(skin_models.Weapon.name.in_(item_names))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def upsert(self, **values):
        stmt = postgresql.insert(skin_models.Weapon).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=['name'], set_=values)
        returning_stmt = do_update_stmt.returning(skin_models.Weapon)
        return await self._session.scalar(returning_stmt)

    async def get_by_name(self, item_name: str) -> skin_models.Weapon:
        stmt = sqlalchemy.select(skin_models.Weapon).where(skin_models.Weapon.name == item_name)
        return await self._session.scalar(stmt)

    async def update_by_name(self, weapon_name: str, **values):
        update_stmt = sqlalchemy.update(skin_models.Weapon).values(**values)
        where_stmt = update_stmt.where(skin_models.Weapon.name == weapon_name)
        returning_stmt = where_stmt.returning(skin_models.Weapon)
        weapon = await self._session.scalar(returning_stmt)
        await self._session.flush()
        return weapon

    async def delete_by_name(self, item_name: str) -> bool:
        if (weapon := await self.get_by_name(item_name)) is None:
            return False
        await self._session.delete(weapon)
        await self._session.flush()
        return True

    async def get_all(self) -> sqlalchemy.ScalarResult[skin_models.Weapon]:
        stmt = sqlalchemy.select(skin_models.Weapon)
        return await self._session.scalars(stmt)

    async def get_skins_for_weapon(self, weapon_name: str) -> sqlalchemy.ScalarResult[skin_models.Skin]:
        stmt = (
            sqlalchemy.select(skin_models.Skin)
            .join(skin_models.Skin.w_s_q)
            .join(skin_models.WeaponSkinQuality.weapon)
            .where(skin_models.Weapon.name == weapon_name)
        )
        without_duplicate_stmt = stmt.distinct()
        return await self._session.scalars(without_duplicate_stmt)
