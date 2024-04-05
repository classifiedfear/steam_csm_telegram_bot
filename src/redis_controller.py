from redis import asyncio as aioredis


class RedisController:
    def __init__(self, redis: aioredis.Redis) -> None:
        self._redis = redis

    async def add_user(self, user_id: int) -> None:
        await self._redis.set(name=str(user_id), value=1)

    async def remove_user(self, user_id: int) -> None:
        await self._redis.delete(str(user_id))

    async def is_user_exists(self, user_id: int) -> bool:
        return True if await self._redis.get(name=str(user_id)) else False

    async def subscribe_skin_to_user(self, user_id: int) -> None:
        await self._redis.hset(f'{user_id}', 'subscribe', )

    async def set_quality(self, user_id: int, value: str) -> None:
        await self._redis.hset(f'{user_id}_settings', 'quality', value=value)

    async def set_stattrak(self, user_id: int, value: bool) -> None:
        await self._redis.hset(f'{user_id}_settings', 'stattrak', value='1' if value else '0')

    async def set_search(self, user_id: int, value: bool) -> None:
        await self._redis.hset(f'{user_id}_settings', 'search', value='1' if value else '0')
