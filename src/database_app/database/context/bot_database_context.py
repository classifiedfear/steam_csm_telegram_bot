from sqlalchemy.ext import asyncio as async_alchemy

from src.database_app.database.engine.bot_database_engine import BotDatabaseEngine
from src.database_app.database.tables.skin_tables.quality_table import QualityTable
from src.database_app.database.tables.skin_tables.skin_table import SkinTable
from src.database_app.database.tables.user_tables.user_table import UserTable
from src.database_app.database.tables.skin_tables.weapon_skin_quality_table import WeaponSkinQualityTable
from src.database_app.database.tables.skin_tables.weapon_table import WeaponTable


class BotDatabaseContext:
    def __init__(self, db_engine: BotDatabaseEngine):
        self._db_engine = db_engine
        self._session_maker = async_alchemy.async_sessionmaker(
            self._db_engine.engine, expire_on_commit=False, autocommit=False
        )

    async def __aenter__(self):
        self._session = self._session_maker()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.aclose()

    def get_weapon_table(self) -> WeaponTable:
        return WeaponTable(self._db_engine, self._session)

    def get_skin_table(self) -> SkinTable:
        return SkinTable(self._db_engine, self._session)

    def get_quality_table(self) -> QualityTable:
        return QualityTable(self._db_engine, self._session)

    def get_user_table(self) -> UserTable:
        return UserTable(self._db_engine, self._session)

    def get_weapon_skin_quality_table(self) -> WeaponSkinQualityTable:
        return WeaponSkinQualityTable(self._db_engine, self._session)





