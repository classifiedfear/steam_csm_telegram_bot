import typing

import sqlalchemy
from sqlalchemy.dialects import postgresql

from src.database_app.database.models import skin_models
from src.database_app.database.tables.abc_table.table import Table


class SkinTable(Table):

    async def create(self, skin_model_data: typing.Dict[str, typing.Any]) -> skin_models.Skin:
        skin_model = skin_models.Skin()
        await super().create(skin_model)
        return skin_model

    async def get_by_id(self, id: int) -> typing.Type[skin_models.Skin] | None:
        return await self._session.get(skin_models.Skin, id)

    async def update_by_id(self, id: int, **values) -> typing.Type[skin_models.Skin] | None:
        update_stmt = sqlalchemy.update(skin_models.Skin).values(**values)
        where_stmt = update_stmt.where(skin_models.Skin.id == id)
        returning_stmt = where_stmt.returning(skin_models.Skin)
        skin = await self._session.scalar(returning_stmt)
        await self._session.flush()
        return skin

    async def delete_by_id(self, id: int) -> bool:
        if (skin := await self.get_by_id(id)) is None:
            return False
        await self._session.delete(skin)
        await self._session.flush()
        return True

    async def create_many(self, skin_models_data: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[skin_models.Skin]:
        models = [skin_models.Skin(**skin_model_data) for skin_model_data in skin_models_data]
        await super().create_many(models)
        return models

    async def get_many_by_id(self, ids: typing.List[int]):
        select_stmt = sqlalchemy.select(skin_models.Skin)
        where_stmt = select_stmt.where(skin_models.Skin.id.in_(ids))
        return await self._session.scalars(where_stmt)

    async def get_many_by_name(self, names: typing.List[str]):
        select_stmt = sqlalchemy.select(skin_models.Skin)
        where_stmt = select_stmt.where(skin_models.Skin.name.in_(names))
        return await self._session.scalars(where_stmt)

    async def delete_many_by_id(self, ids: typing.List[int]):
        delete_stmt = sqlalchemy.delete(skin_models.Skin)
        where_stmt = delete_stmt.where(skin_models.Skin.id.in_(ids))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def delete_many_by_name(self, item_names: typing.List[str]):
        delete_stmt = sqlalchemy.delete(skin_models.Skin)
        where_stmt = delete_stmt.where(skin_models.Skin.name.in_(item_names))
        await self._session.execute(where_stmt)
        await self._session.flush()

    async def upsert(self, **values):
        stmt = postgresql.insert(skin_models.Skin).values(**values)
        do_update_stmt = stmt.on_conflict_do_update(index_elements=['name'], set_=values)
        returning_stmt = do_update_stmt.returning(skin_models.Skin)
        return await self._session.scalar(returning_stmt)

    async def get_by_name(self, name: str) -> typing.Type[skin_models.Skin] | None:
        stmt = sqlalchemy.select(skin_models.Skin).where(skin_models.Skin.name == name)
        return await self._session.scalar(stmt)

    async def update_by_name(self, name: str, **values) -> typing.Type[skin_models.Skin] | None:
        update_stmt = sqlalchemy.update(skin_models.Skin).values(**values)
        where_stmt = update_stmt.where(skin_models.Skin.name == name)
        returning_stmt = where_stmt.returning(skin_models.Skin)
        skin = await self._session.scalar(returning_stmt)
        await self._session.flush()
        return skin

    async def delete_by_name(self, skin_name: str) -> bool:
        if (skin := await self.get_by_name(skin_name)) is None:
            return False
        await self._session.delete(skin)
        await self._session.flush()
        return True

    async def get_all(self) -> sqlalchemy.ScalarResult[skin_models.Skin]:
        stmt = sqlalchemy.select(skin_models.Skin)
        return await self._session.scalars(stmt)

    async def get_stattrak_existence_for_skin(self, skin_name: str) -> bool:
        stmt = sqlalchemy.select(skin_models.Skin.stattrak_existence).where(skin_models.Skin.name == skin_name)
        return await self._session.scalar(stmt)

