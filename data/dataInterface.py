from data.GuildEntry import GuildEntry

guilds: dict = {}

def save_guildconfig() -> None:
    """Saves the current guild configuration to the disk.
    """

def save_all() -> None:
    

def get_guild_by_ID(guild_id: str) -> GuildEntry:
    """Returns the GuildEntry for a given `guild_id`
    """
    if guilds.get(guild_id) == None:
        return GuildEntry(guild_id, "")

    return guilds.get(guild_id)

def set_guild(guild_id: str, guild: GuildEntry) -> bool:
    if 
