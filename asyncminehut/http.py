from aiohttp import ClientSession

from .constants import BASE_URL


class HTTP:
    def __init__(self, session):
        self.session = session

    async def get(self, url: str, **kwargs) -> dict:
        return await (await self.session.get(BASE_URL + url, **kwargs)).json()

    async def post(self, url: str, **kwargs) -> dict:
        return await (await self.session.post(BASE_URL + url, **kwargs)).json()
