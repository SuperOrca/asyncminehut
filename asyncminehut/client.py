import aiohttp
import asyncio
import sys
from typing import AsyncGenerator, Optional

from .constants import CLIENT_TIMEOUT
from .errors import ServerNotFound, PluginNotFound
from .http import HTTP
from .meta import __version__
from .models import Server, PartialServer, Plugin, SimpleStats, HomepageStats, PlayerDistribution
from .utils import get


class Client:
    def __init__(self, session: Optional[aiohttp.ClientSession] = None,
                 loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self._loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()
        self._session: aiohttp.ClientSession = session or aiohttp.ClientSession(
            timeout=CLIENT_TIMEOUT,
            loop=self._loop,
            headers={'User-Agent': "AsyncMinehut v{} Python/{}.{} aiohttp/{}".format(
                __version__, sys.version_info[0], sys.version_info[1], aiohttp.__version__)}
        )
        self._http: HTTP = HTTP(self._session)

    async def getServerByID(self, server_id: str) -> Server:
        data = await self._http.get(f'/server/{server_id}')
        if not data.get('ok', True):
            raise ServerNotFound(
                'Server with id "{}" was not found.'.format(server_id))
        return Server(self, data.get('server'))

    async def getServerByName(self, server_name: str) -> Server:
        data = await self._http.get(f'/server/{server_name}?byName=true')
        if not data.get('ok', True):
            raise ServerNotFound(
                'Server with name "{}" was not found.'.format(server_name))
        return Server(self, data.get('server'))

    async def getAllServers(self) -> AsyncGenerator[PartialServer, None]:
        data = await self._http.get('/servers')
        for server in data.get('servers'):
            yield PartialServer(server)

    async def getTop5Servers(self) -> AsyncGenerator[PartialServer, None]:
        data = await self._http.get('/network/top_servers')
        for server in data.get('servers'):
            yield PartialServer(server)

    async def getPluginByID(self, plugin_id: str) -> Plugin:
        if not hasattr(self, '__plugins'):
            self.__plugins = await self._http.get('/plugins_public')
        query = get(self.__plugins.get('all'), '_id', plugin_id)
        if not query:
            raise PluginNotFound(
                'Plugin with id "{}" was not found.'.format(plugin_id))
        return Plugin(query)

    async def getPluginByName(self, plugin_name: str) -> Plugin:
        if not hasattr(self, '__plugins'):
            self.__plugins = await self._http.get('/plugins_public')
        query = get(self.__plugins.get('all'), 'name', plugin_name)
        if not query:
            raise PluginNotFound(
                'Plugin with name "{}" was not found.'.format(plugin_name))
        return Plugin(query)

    async def getAllPlugins(self) -> AsyncGenerator[Plugin, None]:
        if not hasattr(self, '__plugins'):
            self.__plugins = await self._http.get('/plugins_public')
        for plugin in self.__plugins.get('all'):
            yield Plugin(plugin)

    async def getSimpleStats(self) -> SimpleStats:
        data = await self._http.get('/network/simple_stats')
        return SimpleStats(data)

    async def getHomepageStats(self) -> HomepageStats:
        data = await self._http.get('/network/homepage_stats')
        return HomepageStats(data)

    async def getPlayerDistribution(self) -> PlayerDistribution:
        data = await self._http.get('/network/players/distribution')
        return PlayerDistribution(data)

    async def close(self) -> None:
        await self._http.close()


__all__ = (
    "Client"
)
