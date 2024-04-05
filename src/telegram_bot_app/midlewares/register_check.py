from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.db.bot_database import BotDatabase
from src.redis_controller import RedisController

from src.db.tables import users_queries


class RegisterCheck(BaseMiddleware):
    def __init__(self, redis_controller: RedisController, database: BotDatabase) -> None:
        super().__init__()
        self._redis_controller = redis_controller
        self._database = database

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        await self._redis_controller.remove_user(event.from_user.id)
        if await self._redis_controller.is_user_exists(event.from_user.id):
            return await handler(event, data)
        if not await self._database.is_user_exists(event.from_user.id):
            await self._database.add_user(
                event.from_user.id,
                event.from_user.username,
                event.from_user.full_name
            )
            await self._redis_controller.add_user(event.from_user.id)
        return await handler(event, data)
