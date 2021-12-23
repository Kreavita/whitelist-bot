import data
from dataclasses import dataclass

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
    players: dict = {}

    def __init__(self, guild_id: str, rcon_address: str, rcon_port: int = 25575):
        self.guild_id = guild_id
        self.rcon_address = rcon_address
        self.rcon_port = rcon_port
    
    def get_username_by_id(self, user_id: str) -> str:
        return self.players.get(user_id)

    def set_player(self, user_id: str, ingame_name: str) -> None:
        self.players[user_id] = ingame_name