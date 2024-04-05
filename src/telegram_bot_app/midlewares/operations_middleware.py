from typing import Callable, Dict, Any, Awaitable

from redis.asyncio import Redis
from aiogram import BaseMiddleware
from aiogram.types import Message

from src.redis_controller import RedisController


class GetterDefaultSettings(BaseMiddleware):
    def __init__(self, redis_controller: RedisController) -> None:
        super().__init__()
        self._redis_controller = redis_controller

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if weapons := await self._redis_controller.get_list('weapons'):
            data['weapons'] = weapons
            return await handler(event, data)

        return await handler(event, data)
