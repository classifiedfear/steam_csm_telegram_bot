import abc
from typing import Self, List

from aiogram import Router


class TgMsgHandler(abc.ABC):
    _router: Router = None

    @abc.abstractmethod
    async def handle(self):
        pass

    @staticmethod
    def is_composite() -> bool:
        return False

    @property
    def router(self) -> Router:
        return self._router


class TgMsgCompositeHandler(TgMsgHandler):

    def __init__(self):
        self._handlers = set()

    @staticmethod
    def is_composite() -> bool:
        return True

    def add(self, handler: TgMsgHandler) -> Self:
        self._handlers.add(handler)
        return self

    def remove(self, handler: TgMsgHandler) -> Self:
        self._handlers.remove(handler)
        return self

    async def handle(self):
        for handler in self._handlers:
            await handler.handle()

    @property
    def router(self) -> List[Router]:
        return [handler.weapon_router for handler in self._handlers]

