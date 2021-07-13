class PartialServer:
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

    async def get_players(self):
        """Going to change this later."""
        for player in self.player_data.get('players'):
            yield player

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<PartialServer id={0.id} name={0.name}>'.format(self)

    def __dict__(self) -> dict:
        return self.data


class Server:
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

    async def get_plugins(self):
        for plugin in self.data.get('active_plugins'):
            yield await self._client.getPluginByID(plugin)

    async def get_players(self):
        """Going to change this later."""
        for player in self.player_data.get('players'):
            yield player

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<Server id={0.id} name={0.name}>'.format(self)

    def __dict__(self) -> dict:
        return self.data


class ServerPlan:
    def __init__(self, *args) -> None:
        self.data: tuple = tuple(args)

        self.name = self.data[0]
        self.max_players = self.data[1]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<Server name={0.name} max_players={0.max_players}>'.format(self)


class Pod:
    def __init__(self, data: dict) -> None:
        self.data: dict = data

        self.instance = data.get('instance')
        self.sidecar = data.get('instance-sidecar')

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<Pod>'

    def __dict__(self) -> dict:
        return self.data


class ServerProperties:
    def __init__(self, data: dict) -> None:
        self.data: dict = data

        for key, value in data.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return '<ServerProperties>'

    def __dict__(self) -> dict:
        return self.data


class Plugin:
    def __init__(self, data: dict):
        self.data: dict = data

        for key, value in data.items():
            if key != '_id':
                setattr(self, key, value)
            else:
                setattr(self, 'id', value)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<Plugin id={0.id} name={0.name}>'.format(self)

    def __dict__(self) -> dict:
        return self.data


class SimpleStats:
    def __init__(self, data: dict):
        self.data: dict = data

        self.player_count = data.get('player_count')
        self.server_count = data.get('server_count')
        self.server_max = data.get('server_max')
        self.ram_count = data.get('ram_count')
        self.ram_max = data.get('ram_max')

    def __repr__(self) -> str:
        return '<SimpleStats>'

    def __dict__(self) -> dict:
        return self.data


class HomepageStats:
    def __init__(self, data: dict):
        self.data: dict = data

        self.server_count = data.get('server_count')
        self.user_count = data.get('user_count')

    def __repr__(self) -> str:
        return '<HomepageStats>'

    def __dict__(self) -> dict:
        return self.data

class PlayerDistribution:
    def __init__(self, data: dict):
        self.data: dict = data

        self.bedrock_total = data.get('bedrockTotal')
        self.java_total = data.get('javaTotal')
        self.bedrock_lobby = data.get('bedrockLobby')
        self.bedrock_player_server = data.get('bedrockPlayerServer')
        self.java_lobby = data.get('javaLobby')
        self.java_player_server = data.get('javaPlayerServer')

    def __repr__(self) -> str:
        return '<PlayerDistribution>'

    def __dict__(self) -> dict:
        return self.data