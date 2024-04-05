import abc

from sqlalchemy.ext import asyncio as async_alchemy

from src.db.bot_database import BotDatabaseEngine


class Table(abc.ABC):
    def __init__(self, db_engine: BotDatabaseEngine, session: async_alchemy.AsyncSession):
        self._db_engine = db_engine
        self._session = session

    @abc.abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    async def delete(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    async def get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    async def update(self, *args, **kwargs):
        pass
