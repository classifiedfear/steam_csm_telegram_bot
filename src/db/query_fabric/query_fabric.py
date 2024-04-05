from sqlalchemy.ext import asyncio as async_alchemy

from src.db.tables.quality_table import QualityTable
from src.db.tables.skin_table import SkinTable
from src.db.tables.user_table import UserTable
from src.db.tables.weapon_skin_quality_table import WeaponSkinQualityTable
from src.db.tables.weapon_table import WeaponTable


class QueryFabric:
    def __init__(self, engine: async_alchemy.AsyncEngine, session_maker: async_alchemy.AsyncSession):
        self._engine = engine
        self._session_maker = session_maker

    def get_weapon_table(self) -> WeaponTable:
        return WeaponTable(self._engine, self._session_maker)

    def get_skin_table(self) -> SkinTable:
        return SkinTable(self._engine, self._session_maker)

    def get_quality_table(self) -> QualityTable:
        return QualityTable(self._engine, self._session_maker)

    def get_user_table(self) -> UserTable:
        return UserTable(self._engine, self._session_maker)

    def get_weapon_skin_quality_table(self) -> WeaponSkinQualityTable:
        return WeaponSkinQualityTable(self._engine, self._session_maker)
