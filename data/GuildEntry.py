import json
from dataclasses import dataclass, field, asdict
from typing import Union


@dataclass
class GuildEntry:
    """Represents a discord guild. Contains the RCON Configuration and the player database

        Attributes:
        - `guild_id` ID of the discord guild
        - `rcon_address` RCON address for the RCON connection to the guild's minecraft server
        - `rcon_port` RCON port for the RCON connection to the guild's minecraft server
        - `rcon_password` RCON password for the RCON connection to the guild's minecraft server
        - `players` Player storage dict, associates their discord ids to their ingame snames
    """
    guild_id: int
    rcon_address: str
    rcon_port: int
    rcon_password: str
    players: dict[int, str] = field(default_factory=dict)

    def __init__(self, guild_id: int, rcon_address: str, rcon_port: int, rcon_password: str, players: dict[str, str] = {}):
        self.guild_id = guild_id
        self.rcon_address = rcon_address
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password
        self.players = players

    def player_by_id(self, user_id: int) -> Union[str, None]:
        """ Get the minecraft username associated with the Discord ID `user_id` and return it, or return `None`
        """
        return self.players.get(user_id)

    def id_by_player(self, player_name: str) -> Union[int, None]:
        """ Get the Discord ID associated with a minecraft username `player_name` and return it, or return `None`
        """
        for id, key in self.players:
            if key == player_name.lower():
                return id
        return None

    def set_player(self, user_id: int, ingame_name: str) -> None:
        """Sets the username of a players
        """
        if ingame_name is None:
            self.players[user_id] = None
        else:
            self.players[user_id] = ingame_name.lower()

    def to_JSON(self) -> str:
        """Returns a JSON Representation of this GuildEntry
        """
        return json.dumps(asdict(self), indent=2)


def GuildEntry_from_JSON(json_data: str) -> GuildEntry:
    """Parses a Guild Entry JSON String and returns the GuildEntry Object
    """

    json_dict: dict = json.loads(json_data)
    return GuildEntry(json_dict["guild_id"], json_dict["rcon_address"], json_dict["rcon_port"], json_dict["players"])
