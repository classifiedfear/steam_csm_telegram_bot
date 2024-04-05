import typing

import sqlalchemy

from sqlalchemy.dialects import postgresql

from src.db.models import skins_models
from src.db.tables.table import Table


class QualityTable(Table):

    async def create(self, **values) -> int:
        insert_stmt = (postgresql.insert(skins_models.Quality).values(**values))
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['name'], set_=values
        )
        returning_stmt = do_update_stmt.returning(skins_models.Quality.id)
        result = await self._session.execute(returning_stmt)
        await self._session.commit()
        return result.scalar()

    async def create_many(self, qualities_to_create: typing.List[typing.Dict[str, typing.Any]]):
        insert_stmt = postgresql.insert(skins_models.Quality)
        do_nothing_stmt = insert_stmt.on_conflict_do_nothing()
        await self._session.execute(do_nothing_stmt, qualities_to_create)
        await self._session.commit()

    async def get(self, id: int) -> skins_models.Quality:
        stmt = sqlalchemy.select(skins_models.Quality).where(skins_models.Quality.id == id)
        return await self._session.scalar(stmt)

    async def get_by_name(self, name: str) -> skins_models.Quality:
        stmt = sqlalchemy.select(skins_models.Quality).where(skins_models.Quality.name == name)
        return await self._session.scalar(stmt)

    async def delete(self, id: int) -> None:
        stmt = sqlalchemy.delete(skins_models.Quality).where(skins_models.Quality.id == id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_by_name(self, name: str) -> None:
        stmt = sqlalchemy.delete(skins_models.Quality).where(skins_models.Quality.name == name)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_many_by_name(self, names: typing.List[str]):
        delete_stmt = sqlalchemy.delete(skins_models.Quality)
        where_stmt = delete_stmt.where(skins_models.Quality.name.in_(names))
        await self._session.execute(where_stmt)
        await self._session.commit()

    async def update(self, id: int, **values):
        stmt = sqlalchemy.update(skins_models.Quality).where(skins_models.Quality.id == id).values(**values)
        await self._session.execute(stmt)
        await self._session.commit()

    async def update_by_name(self, name: str, **values):
        stmt = sqlalchemy.update(skins_models.Quality).where(skins_models.Quality.name == name).values(**values)
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_qualities(self) -> sqlalchemy.ScalarResult[skins_models.Quality]:
        stmt = sqlalchemy.select(skins_models.Quality)
        return await self._session.scalars(stmt)


