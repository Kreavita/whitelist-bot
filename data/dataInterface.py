import os
from data.GuildEntry import GuildEntry, GuildEntry_from_JSON

guilds: dict[str, GuildEntry] = {}


def load_guilds() -> None:
    """Should be called on initialization. Loads all stored guild configurations and populates the `guilds` dict.
    """
    for file_name in os.listdir(os.path.join(os.path.dirname(__file__), "guilds")):
        if not file_name.endswith(".json"):
            continue

        raw_string: str = ""

        with open(os.path.join(os.path.dirname(__file__), "guilds", file_name), "r") as file:
            for line in file.readlines():
                raw_string += line

        guild: GuildEntry = GuildEntry_from_JSON(raw_string)
        guilds[guild.guild_id] = guild


def save_all() -> None:
    """Saves and overwrites everything to the disk, should be called periodically and before application shutdown.
    """

    global guilds

    for guild_id in guilds:
        save_guild(guild_id)


def save_guild(guild_id: str) -> bool:
    """Saves the player database of a guild to the disk. Returns `True` if it was successful, or else `False`
    """

    global guilds

    if guild_id == None:
        return False

    if guilds.get(guild_id) == None:
        return False

    with open(os.path.join(os.path.dirname(__file__), f"guilds\{guild_id}.json"), "w") as file:
        file.write(guilds.get(guild_id).to_JSON())


def guild_by_id(guild_id: str) -> GuildEntry:
    """Returns the GuildEntry for a given `guild_id`. \
        Creates a new GuildEntry if the `guild_id` is not in the Guilds dict. \
        Returns None if `guild_id` is None

        Arguments:
            - `guild_id` ID of the requested Guild
    """

    global guilds

    if guild_id == None:
        return None

    if guilds.get(guild_id) == None:
        # returns a new GuildEntry if the guild_id has none yet
        guilds[guild_id] = GuildEntry(guild_id, "")
        return guilds[guild_id]

    return guilds.get(guild_id)


def set_guild(guild_id: str, guild: GuildEntry) -> bool:
    """Returns the GuildEntry for a given `guild_id`. \
        Creates a new GuildEntry if the `guild_id` is not in the Guilds dict. \
        Returns None if `guild_id` is None

        Arguments:
            - `guild_id` ID of the requested Guild
            - `guild` GuildEntry that should be added to the guilds
    """

    global guilds

    if guild_id == None:
        return None

    if guilds.get(guild_id) != None:
        # return false, because this guild already has a configuration entry
        return False

    guilds[guild_id] = guild
    return True
