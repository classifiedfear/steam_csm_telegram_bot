import typing
from typing import Type

import sqlalchemy

from sqlalchemy.dialects import postgresql

from src.database_app.database.models import skin_models
from src.database_app.database.models.skin_models import Quality
from src.database_app.database.tables.abc_table.table import Table


class QualityTable(Table):

    async def create(self, quality_model_data: typing.Dict[str, typing.Any]) -> skin_models.Quality:
        model = skin_models.Quality()
        await super().create(model)
        return model

    async def get_by_id(self, id: int) -> Type[Quality] | None:
        return await self._session.get(skin_models.Quality, id)

    async def update_by_id(self, id: int, **values):
        update_stmt = sqlalchemy.update(skin_models.Quality).values(**values)
        where_stmt = update_stmt.where(skin_models.Quality.id == id)
        returning_stmt = where_stmt.returning(skin_models.Quality)
        quality = await self._session.scalar(returning_stmt)
        await self._session.flush()
        return quality

    async def delete_by_id(self, id: int) -> bool:
        if (quality := await self.get_by_id(id)) is None:
            return False
        await self._session.delete(quality)
        await self._session.flush()
        return True

    async def create_many(self, quality_models_data: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[skin_models.Quality]:
        models = [skin_models.Quality()]
        await super().create_many(models)
        return models

    async def get_many_by_id(self, ids: typing.List[int]):
        select_stmt = sqlalchemy.select(skin_models.Quality)
        where_stmt = select_stmt.where(skin_models.Quality.id.in_(ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name(self, names: typing.List[str]):
        select_stmt = sqlalchemy.select(skin_models.Quality)
        where_stmt = select_stmt.where(skin_models.Quality.name.in_(names))
        return await self._session.scalars(where_stmt)

    async def delete_many_by_id(self, ids: typing.List[int]) -> None:
        delete_stmt = sqlalchemy.delete(skin_models.Quality)
        where_stmt = delete_stmt.where(skin_models.Quality.id.in_(ids))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def delete_many_by_name(self, item_names: typing.List[str]):
        delete_stmt = sqlalchemy.delete(skin_models.Quality)
        where_stmt = delete_stmt.where(skin_models.Quality.name.in_(item_names))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def upsert(self, **values):
        stmt = postgresql.insert(skin_models.Quality).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=['name'], set_=values)
        returning_stmt = do_update_stmt.returning(skin_models.Quality)
        return await self._session.scalar(returning_stmt)

    async def get_by_name(self, name: str) -> Type[Quality] | None:
        stmt = sqlalchemy.select(skin_models.Quality).where(skin_models.Quality.name == name)
        return await self._session.scalar(stmt)

    async def update_by_name(self, quality_name: str, **values):
        update_stmt = sqlalchemy.update(skin_models.Quality).values(**values)
        where_stmt = update_stmt.where(skin_models.Quality.name == quality_name)
        returning_stmt = where_stmt.returning(skin_models.Quality)
        weapon = await self._session.scalar(returning_stmt)
        await self._session.flush()
        return weapon

    async def delete_by_name(self, quality_name: str) -> bool:
        if (quality_model := await self.get_by_name(quality_name)) is None:
            return False
        await self._session.delete(quality_model)
        await self._session.flush()
        return True


    async def get_all(self) -> sqlalchemy.ScalarResult[skin_models.Quality]:
        stmt = sqlalchemy.select(skin_models.Quality)
        return await self._session.scalars(stmt)


