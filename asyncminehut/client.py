import aiohttp
import asyncio
import sys
from typing import Optional, Generator

from .constants import CLIENT_TIMEOUT
from .errors import *
from .http import HTTP
from .meta import __version__
from .objects import Server, PartialServer, Plugin


class HTTPClient:
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
        return Server(self._http, data)

    async def getServerByName(self, server_name: str) -> Server:
        data = await self._http.get(f'/server/{server_name}?byName=true')
        if not data.get('ok', True):
            raise ServerNotFound(
                'Server with name "{}" was not found.'.format(server_name))
        return Server(self._http, data)

    async def getAllServers(self):
        data = await self._http.get('/servers')
        for server in data['servers']:
            yield PartialServer(server)

    async def getPluginByID(self, plugin_id: str) -> Plugin:
        if not hasattr(self, '__plugins'):
            self.__plugins = await self._http.get('/plugins_public')
        query = [plugin for plugin in self._plugins if plugin["_id"] == plugin_id]
        if query == []:
            raise PluginNotFound(
                'Plugin with id "{}" was not found.'.format(plugin_id))
        return Plugin(self, query[0])

    async def getPluginByName(self, plugin_name: str) -> Plugin:
        if not hasattr(self, '__plugins'):
            self.__plugins = await self._http.get('/plugins_public')
        query = [plugin for plugin in self._plugins if plugin["name"] == plugin_name]
        if query == []:
            raise PluginNotFound(
                'Plugin with name "{}" was not found.'.format(plugin_name))
        return Plugin(self, query[0])

    async def getAllPlugins(self):
        if not hasattr(self, '__plugins'):
            self.__plugins = await self._http.get('/plugins_public')
        for plugin in self.__plugins['all']:
            yield Plugin(self, plugin)

    async def close(self):
        await self.session.close()
