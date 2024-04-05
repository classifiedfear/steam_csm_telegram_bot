import sqlalchemy
from sqlalchemy import delete
from sqlalchemy.dialects import postgresql


from src.db.models import users_models
from src.db.tables.table import Table


class UserTable(Table):
    async def create(self, id: int, username: str, full_name: str):
        stmt = postgresql.insert(users_models.User).values(id=id, username=username, full_name=full_name)
        await self._session.execute(stmt)

    async def get(self, id: int) -> users_models.User:
        stmt = sqlalchemy.select(users_models.User).where(users_models.User.id == id)
        return await self._session.scalar(stmt)

    async def delete(self, id: int) -> None:
        stmt = delete(users_models.User).where(users_models.User.id == id)
        await self._session.execute(stmt)