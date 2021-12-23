import json
from dataclasses import dataclass, field, asdict


@dataclass
class GuildEntry:
    """Represents a discord guild. Contains the RCON Configuration and the player database

        Attributes:
        - `guild_id` ID of the discord guild
        - `rcon_address` RCON address of the guilds minecraft server
        - `rcon_port` RCON port of the guilds minecraft server
        - `players` Player dict {user_id : ingame_name}
    """
    guild_id: str
    rcon_address: str
    rcon_port: int = 25575
    players: dict[str, str] = field(default_factory=dict)

    def __init__(self, guild_id: str, rcon_address: str, rcon_port: int = 25575, players: dict[str, str] = {}):
        self.guild_id = guild_id
        self.rcon_address = rcon_address
        self.rcon_port = rcon_port
        self.players = players

    def get_username_by_id(self, user_id: str) -> str:
        return self.players.get(user_id)

    def set_player(self, user_id: str, ingame_name: str) -> None:
        self.players[user_id] = ingame_name

    def to_JSON(self) -> str:
        """Returns a JSON Representation of this dataclass
        """
        return json.dumps(asdict(self), indent=2)


def GuildEntry_from_JSON(json_data: str) -> GuildEntry:
    """Parses a Guild Entry JSON String and returns the GuildEntry Object
    """

    json_dict: dict = json.loads(json_data)
    return GuildEntry(json_dict["guild_id"], json_dict["rcon_address"], json_dict["rcon_port"], json_dict["players"])
