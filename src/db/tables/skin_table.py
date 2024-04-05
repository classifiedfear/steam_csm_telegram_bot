import typing

import sqlalchemy
from sqlalchemy.dialects import postgresql

from src.db.models import skins_models
from src.db.tables.table import Table


class SkinTable(Table):

    async def get(self, id: int) -> skins_models.Skin:
        stmt = sqlalchemy.select(skins_models.Skin).where(skins_models.Skin.id == id)
        return await self._session.scalar(stmt)

    async def get_by_name(self, name: str) -> skins_models.Skin:
        stmt = sqlalchemy.select(skins_models.Skin).where(skins_models.Skin.name == name)
        return await self._session.scalar(stmt)

    async def create(self, **values) -> int:
        insert_stmt = postgresql.insert(skins_models.Skin).values(**values)
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['name'], set_=values
        )
        returning_stmt = do_update_stmt.returning(skins_models.Skin.id)
        result = await self._session.execute(returning_stmt)
        await self._session.commit()
        return result.scalar()

    async def create_many(self, items_to_create: typing.List[typing.Dict[str, typing.Any]]):
        stmt = postgresql.insert(skins_models.Skin)
        on_confict_do_nothing_stmt = stmt.on_conflict_do_nothing()
        await self._session.execute(on_confict_do_nothing_stmt, items_to_create)
        await self._session.commit()

    async def delete(self, id: int) -> None:
        stmt = sqlalchemy.delete(skins_models.Skin).where(skins_models.Skin.id == id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_by_name(self, name: str) -> None:
        stmt = sqlalchemy.delete(skins_models.Skin).where(skins_models.Skin.name == name)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_many_by_name(self, names: typing.List[str]):
        delete_stmt = sqlalchemy.delete(skins_models.Skin)
        where_stmt = delete_stmt.where(skins_models.Skin.name.in_(names))
        await self._session.execute(where_stmt)
        await self._session.commit()

    async def update(self, id: int, **values):
        stmt = sqlalchemy.update(skins_models.Skin).where(skins_models.Skin.id == id).values(**values)
        await self._session.execute(stmt)
        await self._session.commit()

    async def update_by_name(self, name: str, **values):
        stmt = sqlalchemy.update(skins_models.Skin).where(skins_models.Skin.name == name).values(**values)
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_skins(self) -> sqlalchemy.ScalarResult[skins_models.Skin]:
        stmt = sqlalchemy.select(skins_models.Skin)
        return await self._session.scalars(stmt)

    async def get_stattrak_existence_for_skin(self, skin_name: str) -> bool:
        stmt = sqlalchemy.select(skins_models.Skin.stattrak_existence).where(skins_models.Skin.name == skin_name)
        return await self._session.scalar(stmt)

