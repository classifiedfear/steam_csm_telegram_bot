import contextlib

import aiohttp
from aiohttp import ClientResponse
from fake_useragent import UserAgent


class CommonRequestExecutor:
    def __init__(self) -> None:
        self._headers = {'user-agent': f'{UserAgent.random}'}

    async def get_response_json(self, link: str, *, headers: dict = None) -> dict:
        async with self._get(link, headers) as response:
            return await response.json(content_type=None)

    async def get_response_text(self, link: str, *, headers: dict = None) -> str:
        async with self._get(link, headers) as response:
            return await response.text(encoding='utf-8')

    async def post_response_text(self, link: str, json: dict):
        async with self._post(link, json) as response:
            return await response.text()

    @contextlib.asynccontextmanager
    async def _post(self, link: str, json: dict):
        session = aiohttp.ClientSession()
        response = await session.post(link, json=json)
        try:
            yield response
        finally:
            response.close()
            await session.close()

    @contextlib.asynccontextmanager
    async def _get(self, link: str, headers: dict) -> ClientResponse:
        headers = self._update_headers_if_necessary(headers)
        session = aiohttp.ClientSession()
        response = await session.get(link, headers=headers)
        try:
            yield response
        finally:
            response.close()
            await session.close()

    def _update_headers_if_necessary(self, headers: dict = None):
        if headers:
            headers.update(self._headers)
            return headers
        return self._headers

