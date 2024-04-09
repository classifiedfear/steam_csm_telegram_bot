import typing

import sqlalchemy
from sqlalchemy.dialects import postgresql

from src.database_app.database.models import skin_models
from src.database_app.database.tables.abc_table.table import Table


class SkinTable(Table):

    async def get(self, id: int) -> skin_models.Skin:
        stmt = sqlalchemy.select(skin_models.Skin).where(skin_models.Skin.id == id)
        return await self._session.scalar(stmt)

    async def get_by_name(self, name: str) -> skin_models.Skin:
        stmt = sqlalchemy.select(skin_models.Skin).where(skin_models.Skin.name == name)
        return await self._session.scalar(stmt)

    async def create(self, **values) -> int:
        insert_stmt = postgresql.insert(skin_models.Skin).values(**values)
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['name'], set_=values
        )
        returning_stmt = do_update_stmt.returning(skin_models.Skin.id)
        result = await self._session.execute(returning_stmt)
        await self._session.commit()
        return result.scalar()

    async def create_many(self, skins_to_add: typing.List[skin_models.Skin]):
        self._session.add_all(skins_to_add)
        await self._session.commit()

    async def delete(self, id: int) -> None:
        stmt = sqlalchemy.delete(skin_models.Skin).where(skin_models.Skin.id == id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_by_name(self, name: str) -> None:
        stmt = sqlalchemy.delete(skin_models.Skin).where(skin_models.Skin.name == name)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_many_by_name(self, names: typing.List[str]):
        delete_stmt = sqlalchemy.delete(skin_models.Skin)
        where_stmt = delete_stmt.where(skin_models.Skin.name.in_(names))
        await self._session.execute(where_stmt)
        await self._session.commit()

    async def update(self, id: int, **values):
        stmt = sqlalchemy.update(skin_models.Skin).where(skin_models.Skin.id == id).values(**values)
        await self._session.execute(stmt)
        await self._session.commit()

    async def update_by_name(self, name: str, **values):
        stmt = sqlalchemy.update(skin_models.Skin).where(skin_models.Skin.name == name).values(**values)
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_all(self) -> sqlalchemy.ScalarResult[skin_models.Skin]:
        stmt = sqlalchemy.select(skin_models.Skin)
        return await self._session.scalars(stmt)

    async def get_stattrak_existence_for_skin(self, skin_name: str) -> bool:
        stmt = sqlalchemy.select(skin_models.Skin.stattrak_existence).where(skin_models.Skin.name == skin_name)
        return await self._session.scalar(stmt)

