import re
from typing import AsyncGenerator
import datetime


from .constants import URL_REGEX
from .http import HTTP
from .errors import APIError


class Model:
    def __repr__(self) -> str:
        value = ''.join(
            f' {attr}={getattr(self, attr)!r}' for attr in self.__slots__)
        return f'<{self.__class__.__name__}{value}>'

    def __str__(self) -> str:
        if hasattr(self, 'name'):
            return self.name
        return self.__repr__()

    @property
    def __dict__(self) -> dict:
        if hasattr(self, 'data') and isinstance(self.data, dict):
            return self.data
        return None


class PartialServer(Model):
    __slots__ = ('id', 'name')

    def __init__(self, data: dict) -> None:
        self.data: dict = data

        self.static = data.get('staticInfo', {})
        self.id = self.static.get('_id')
        self.plan = ServerPlan(self.static.get(
            'rawPlan'), self.static.get('planMaxPlayers'))
        self.service_start_date = datetime.datetime.fromtimestamp(
            (self.static.get('serviceStartDate'))/1000.0, tz=datetime.timezone.utc)

        self.max_players = data.get('maxPlayers')
        self.name = data.get('name')
        self.motd = data.get('motd')
        self.icon = data.get('icon')
        self.visibility = data.get('visibility')

        self.save = data.get('saveData', {})
        if (last_save := self.save.get('lastSave')) is not None:
            self.last_save = datetime.datetime.fromtimestamp(
                last_save/1000.0, tz=datetime.timezone.utc)

        self.player_data = data.get('playerData', {})
        self.player_count = self.player_data.get('playerCount')

        self.pod = Pod(data.get('podInfo', {}))


class ServerPlan(Model):
    __slots__ = ('name', 'max_players')

    def __init__(self, *args) -> None:
        self.data: tuple = tuple(args)

        self.name, self.max_players = self.data


class Pod(Model):
    __slots__ = ('instance', 'sidecar')

    def __init__(self, data: dict) -> None:
        self.data: dict = data

        self.instance = data.get('instance')
        self.sidecar = data.get('instance-sidecar')


class ServerProperties(Model):
    __slots__ = ()

    def __init__(self, data: dict) -> None:
        self.data: dict = data

        self.max_players = data.get('max_players')
        self.gamemode = data.get('gamemode')
        self.allow_flight = data.get('allow_flight')
        self.spawn_animals = data.get('spawn_animals')
        self.spawn_mobs = data.get('spawn_mobs')
        self.force_gamemode = data.get('force_gamemode')
        self.hardcore = data.get('hardcore')
        self.pvp = data.get('pvp')
        self.difficulty = data.get('difficulty')
        self.level_seed = data.get('level_seed')
        self.allow_nether = data.get('allow_nether')
        self.generate_structures = data.get('generate_structures')
        self.command_blocks = data.get('enable_command_block')
        self.announce_player_achievements = data.get(
            'annouce_player_achievements')
        self.level_type = data.get('level_type')
        self.level_name = data.get('level_name')
        self.generator_settings = data.get('generator_settings')
        self.resource_pack = data.get('resource_pack')
        self.resource_pack_sha1 = data.get('resource_pack_sha1')
        self.view_distance = data.get('view_distance')
        self.spawn_protection = data.get('spawn_protection')


class Plugin(Model):
    __slots__ = ('id', 'name')

    def __init__(self, data: dict) -> None:
        self.data: dict = data

        self.id = data.get('_id')
        self.name = data.get('name')
        self.credits = data.get('credits')
        self.platform = data.get('platform')
        self.description = data.get('desc')
        self.description_extended = data.get('desc_extended')
        self.version = data.get('version')
        self.disabled = data.get('disabled')
        self.file = data.get('file_name')
        self.created = datetime.datetime.fromtimestamp(
            (data.get('created'))/1000.0, tz=datetime.timezone.utc)
        self.last_updated = datetime.datetime.fromtimestamp(
            (data.get('last_updated'))/1000.0, tz=datetime.timezone.utc)
        self.html_description_extended = data.get('html_desc_extended')

        try:
            match = re.search(URL_REGEX, self.description_extended)
            self.link = match.groups()[0]
        except AttributeError:
            self.link = None


class SimpleStats(Model):
    __slots__ = ()

    def __init__(self, data: dict) -> None:
        self.data: dict = data

        self.player_count = data.get('player_count')
        self.server_count = data.get('server_count')
        self.server_max = data.get('server_max')
        self.ram_count = data.get('ram_count')
        self.ram_max = data.get('ram_max')


class HomepageStats(Model):
    __slots__ = ()

    def __init__(self, data: dict) -> None:
        self.data: dict = data

        self.server_count = data.get('server_count')
        self.user_count = data.get('user_count')


class PlayerDistribution(Model):
    __slots__ = ()

    def __init__(self, data: dict) -> None:
        self.data: dict = data

        self.bedrock_total = data.get('bedrockTotal')
        self.java_total = data.get('javaTotal')
        self.bedrock_lobby = data.get('bedrockLobby')
        self.bedrock_player_server = data.get('bedrockPlayerServer')
        self.java_lobby = data.get('javaLobby')
        self.java_player_server = data.get('javaPlayerServer')


class Server(Model):
    __slots__ = ('id', 'name')

    def __init__(self, http: HTTP, data: dict) -> None:
        self._http = http
        self.data: dict = data

        self.server_properties = ServerProperties(
            data.get('server_properties', {}))
        self.categories = data.get('categories')
        self.purchased_icons = data.get('purchased_icons')
        self.backup_slots = data.get('backup_slots')
        self.suspended = data.get('suspended')
        self.installed_content_packs = data.get('installed_content_packs')
        self.version_type = data.get('server_version_type')
        self.id = data.get('_id')
        self.motd = data.get('motd')
        self.visibility = data.get('visibility')
        self.storage_node = data.get('storage_node')
        self.owner = data.get('owner')
        self.name = data.get('name')
        self.creation = datetime.datetime.fromtimestamp(
            (data.get('creation'))/1000.0, tz=datetime.timezone.utc)
        self.credits_per_day = data.get('credits_per_day')
        self.last_online = datetime.datetime.fromtimestamp(
            (data.get('last_online'))/1000.0, tz=datetime.timezone.utc)
        self.icon = data.get('icon')
        self.online = data.get('online')
        self.max_players = data.get('max_players')
        self.player_count = data.get('player_count')
        self.plan = ServerPlan(data.get(
            'rawPlan'), None)

    async def get_plugins(self) -> AsyncGenerator[Plugin, None]:
        """A method that yields the plugins of the server."""
        for plugin in self.data.get('active_plugins'):
            yield plugin

    async def start(self) -> bool:
        """A method that starts the server. Requires authentication."""
        try:
            await self._http.post(f'/server/{self.id}/start_service')
            await self._http.post(f'/server/{self.id}/start')
            return True
        except APIError:
            return False

    async def stop(self) -> bool:
        """A method that starts the server. Requires authentication."""
        try:
            await self._http.post(f'/server/{self.id}/destroy_service')
            await self._http.post(f'/server/{self.id}/shutdown')
            return True
        except APIError:
            return False

    async def restart(self) -> bool:
        """A method that starts the server. Requires authentication."""
        await self._http.post(f'/server/{self.id}/restart')
        return True

    async def set_visibility(self, visibility: bool) -> bool:
        """A method that sets the visibility of the server. Requires authentication."""
        await self._http.post(f'/server/{self.id}/visibility', data={"visibility": visibility})
        return True

    async def send_command(self, command: str) -> bool:
        """A method that sends a command to the server. Requires authentication."""
        await self._http.post(f'/server/{self.id}/command', data={"command": command})
        return True

    async def change_icon(self, icon: str) -> bool:
        """A method that changes the icon of the server. Requires authentication."""
        await self._http.post(f'/server/{self.id}/icon/equip', data={"icon_id": icon})
        return True

    async def rename(self, name: str = None) -> bool:
        """A method that renames the server. Requires authentication."""
        await self._http.post(f'/server/{self.id}/change_name', data={"name": name})
        return True

    async def edit_properties(self, field: str, value: str) -> bool:
        """A method that edits the properties of the server. Requires authentication."""
        await self._http.post(f'/server/{self.id}/edit_server_properties', data={"field": field, "value": value})
        return True

    async def install_plugin(self, plugin: Plugin) -> bool:
        """A method that installs a plugin. Requires authentication."""
        await self._http.post(f'/server/{self.id}/install_plugin', data={"plugin": plugin.id})
        return True

    async def uninstall_plugin(self, plugin: Plugin) -> bool:
        """A method that uninstalls a plugin. Requires authentication."""
        await self._http.post(f'/server/{self.id}/remove_plugin', data={"plugin": plugin.id})
        return True

    async def reset_plugin_config(self, plugin: Plugin) -> bool:
        """A method that resets the configuration of a plugin. Requires authentication."""
        await self._http.post(f'/server/{self.id}/remove_plugin_data', data={"plugin": plugin.id})
        return True

    async def save_world(self) -> bool:
        """A method that saves the world. Requires authentication."""
        await self._http.post(f'/server/{self.id}/save')
        return True

    async def reset_world(self) -> bool:
        """A method that resets the world. Requires authentication."""
        await self._http.post(f'/server/{self.id}/reset_world')
        return True

    async def reset(self) -> bool:
        """A method that resets the server. Requires authentication."""
        await self._http.post(f'/server/{self.id}/reset_all')
        return True

    async def repair(self) -> bool:
        """A method that repairs the server. Requires authentication."""
        await self._http.post(f'/server/{self.id}/repair_files')
        return True


__all__ = (
    "PartialServer",
    "ServerPlan",
    "Pod",
    "ServerProperties",
    "Plugin",
    "SimpleStats",
    "HomepageStats",
    "PlayerDistribution",
    "Server"
)
