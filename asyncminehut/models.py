import re
from typing import AsyncGenerator


from .constants import URL_REGEX


class Model:
    def __repr__(self) -> str:
        value = ' '.join(
            f'{attr}={getattr(self, attr)!r}' for attr in self.__slots__)
        return f'<{self.__class__.__name__} {value}>'


class PartialServer(Model):
    __slots__ = ('id', 'name')

    def __init__(self, data: dict) -> None:
        self.data: dict = data

        self.static = data.get('staticInfo', {})
        self.id = self.static.get('_id')
        self.plan = ServerPlan(self.static.get(
            'rawPlan'), self.static.get('planMaxPlayers'))
        self.service_start_date = self.static.get(
            'serviceStartDate')  # datetime

        self.max_players = data.get('maxPlayers')
        self.name = data.get('name')
        self.motd = data.get('motd')
        self.icon = data.get('icon')
        self.visibility = data.get('visibility')

        self.save = data.get('saveData', {})
        self.last_save = self.save.get('lastSave')  # datetime

        self.player_data = data.get('playerData', {})
        self.player_count = self.player_data.get('playerCount')

        self.pod = Pod(data.get('podInfo', {}))

    def __str__(self) -> str:
        return self.name

    def __dict__(self) -> dict:
        return self.data


class ServerPlan(Model):
    __slots__ = ('name', 'max_players')

    def __init__(self, *args) -> None:
        self.data: tuple = tuple(args)

        self.name, self.max_players = self.data

    def __str__(self) -> str:
        return self.name


class Pod(Model):
    __slots__ = ('instance', 'sidecar')

    def __init__(self, data: dict) -> None:
        self.data: dict = data

        self.instance = data.get('instance')
        self.sidecar = data.get('instance-sidecar')

    def __str__(self) -> str:
        return self.name

    def __dict__(self) -> dict:
        return self.data


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

    def __dict__(self) -> dict:
        return self.data


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
        self.created = data.get('created')  # datetime
        self.last_updated = data.get('last_updated')  # datetime
        self.html_description_extended = data.get('html_desc_extended')

        try:
            match = re.search(URL_REGEX, self.description_extended)
            self.link = match.groups()[0]
        except AttributeError:
            self.link = None

    def __str__(self) -> str:
        return self.name

    def __dict__(self) -> dict:
        return self.data


class SimpleStats(Model):
    __slots__ = ()

    def __init__(self, data: dict) -> None:
        self.data: dict = data

        self.player_count = data.get('player_count')
        self.server_count = data.get('server_count')
        self.server_max = data.get('server_max')
        self.ram_count = data.get('ram_count')
        self.ram_max = data.get('ram_max')

    def __dict__(self) -> dict:
        return self.data


class HomepageStats(Model):
    __slots__ = ()

    def __init__(self, data: dict) -> None:
        self.data: dict = data

        self.server_count = data.get('server_count')
        self.user_count = data.get('user_count')

    def __dict__(self) -> dict:
        return self.data


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

    def __dict__(self) -> dict:
        return self.data


class Server(Model):
    __slots__ = ('id', 'name')

    def __init__(self, client, data: dict) -> None:
        self._client = client
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
        self.creation = data.get('creation')  # datetime
        self.credits_per_day = data.get('credits_per_day')
        self.last_online = data.get('last_online')  # datetime
        self.icon = data.get('icon')
        self.online = data.get('online')
        self.max_players = data.get('max_players')
        self.player_count = data.get('player_count')
        self.plan = ServerPlan(data.get(
            'rawPlan'), None)

    async def get_plugins(self) -> AsyncGenerator[Plugin, None]:
        for plugin in self.data.get('active_plugins'):
            yield await self._client.getPluginByID(plugin)

    def __str__(self) -> str:
        return self.name

    def __dict__(self) -> dict:
        return self.data


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
