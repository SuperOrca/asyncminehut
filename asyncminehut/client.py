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
    def __init__(self, auth_token: str = None, session_id: str = None, session: Optional[aiohttp.ClientSession] = None,
                 loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self._loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()
        self._session: aiohttp.ClientSession = session or aiohttp.ClientSession(
            timeout=CLIENT_TIMEOUT,
            loop=self._loop,
            headers={'User-Agent': "AsyncMinehut v{} Python/{}.{} aiohttp/{}".format(
                __version__, sys.version_info[0], sys.version_info[1], aiohttp.__version__)}
        )
        self._http: HTTP = HTTP(
            self._session, auth_token=auth_token, session_id=session_id)

    async def get_server_by_id(self, server_id: str) -> Server:
        """A method that gets a server by an id.

        Args:
            server_id (str)

        Raises:
            ServerNotFound

        Returns:
            Server
        """
        data = await self._http.get(f'/server/{server_id}')
        if not data.get('ok', True):
            raise ServerNotFound(
                'Server with id "{}" was not found.'.format(server_id))
        return Server(self, data.get('server'))

    async def get_server_by_name(self, server_name: str) -> Server:
        """A method that gets a server by a name.

        Args:
            server_name (str)

        Raises:
            ServerNotFound

        Returns:
            Server
        """
        data = await self._http.get(f'/server/{server_name}?byName=true')
        if not data.get('ok', True):
            raise ServerNotFound(
                'Server with name "{}" was not found.'.format(server_name))
        return Server(self, data.get('server'))

    async def get_all_servers(self) -> AsyncGenerator[PartialServer, None]:
        """A method that gets all the online servers.

        Returns:
            AsyncGenerator[PartialServer, None]

        Yields:
            Iterator[AsyncGenerator[PartialServer, None]]
        """
        data = await self._http.get('/servers')
        for server in data.get('servers'):
            yield PartialServer(server)

    async def get_top_5_servers(self) -> AsyncGenerator[PartialServer, None]:
        """Get the top 5 servers.

        Returns:
            AsyncGenerator[PartialServer, None]

        Yields:
            Iterator[AsyncGenerator[PartialServer, None]]
        """
        data = await self._http.get('/network/top_servers')
        for server in data.get('servers'):
            yield PartialServer(server)

    async def get_plugin_by_id(self, plugin_id: str) -> Plugin:
        """A method that gets a plugin by an id.

        Args:
            plugin_id (str)

        Raises:
            PluginNotFound

        Returns:
            Plugin
        """
        if not hasattr(self, '__plugins'):
            self.__plugins = await self._http.get('/plugins_public')
        query = get(self.__plugins.get('all'), '_id', plugin_id)
        if not query:
            raise PluginNotFound(
                'Plugin with id "{}" was not found.'.format(plugin_id))
        return Plugin(query)

    async def get_plugin_by_name(self, plugin_name: str) -> Plugin:
        """A method that gets a plugin by a name.

        Args:
            plugin_name (str)

        Raises:
            PluginNotFound

        Returns:
            Plugin
        """
        if not hasattr(self, '__plugins'):
            self.__plugins = await self._http.get('/plugins_public')
        query = get(self.__plugins.get('all'), 'name', plugin_name)
        if not query:
            raise PluginNotFound(
                'Plugin with name "{}" was not found.'.format(plugin_name))
        return Plugin(query)

    async def get_all_plugins(self) -> AsyncGenerator[Plugin, None]:
        """A method that gets all the plugins.

        Returns:
            AsyncGenerator[Plugin, None]

        Yields:
            Iterator[AsyncGenerator[Plugin, None]]
        """
        if not hasattr(self, '__plugins'):
            self.__plugins = await self._http.get('/plugins_public')
        for plugin in self.__plugins.get('all'):
            yield Plugin(plugin)

    async def get_simple_stats(self) -> SimpleStats:
        """A method that gets the simple stats.

        Returns:
            SimpleStats
        """
        data = await self._http.get('/network/simple_stats')
        return SimpleStats(data)

    async def get_homepage_stats(self) -> HomepageStats:
        """A method that gets the homepage stats.

        Returns:
            HomepageStats
        """
        data = await self._http.get('/network/homepage_stats')
        return HomepageStats(data)

    async def get_player_distribution(self) -> PlayerDistribution:
        """A method that gets the player distribution.

        Returns:
            PlayerDistribution
        """
        data = await self._http.get('/network/players/distribution')
        return PlayerDistribution(data)

    async def close(self) -> None:
        """A method that closes the client."""
        await self._http.close()


__all__ = (
    "Client"
)
