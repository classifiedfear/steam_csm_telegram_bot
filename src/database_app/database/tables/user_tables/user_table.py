import sqlalchemy
from sqlalchemy import delete
from sqlalchemy.dialects import postgresql

from src.database_app.database.tables.abc_table.table import Table
from src.database_app.database.models import user_models


class UserTable(Table):
    async def create(self, id: int, username: str, full_name: str):
        stmt = postgresql.insert(user_models.User).values(id=id, username=username, full_name=full_name)
        await self._session.execute(stmt)

    async def get_by_id(self, id: int) -> user_models.User:
        stmt = sqlalchemy.select(user_models.User).where(user_models.User.id == id)
        return await self._session.scalar(stmt)

    async def delete_by_id(self, id: int) -> None:
        stmt = delete(user_models.User).where(user_models.User.id == id)
        await self._session.execute(stmt)