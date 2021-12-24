import os
from data.GuildEntry import GuildEntry, GuildEntry_from_JSON

guilds: dict[int, GuildEntry] = {}


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


def save_guild(guild_id: int) -> bool:
    """Saves the player database of a guild to the disk. Returns `True` if it was successful, or else `False`
    """

    global guilds

    if guild_id == None:
        return False

    if guilds.get(guild_id) == None:
        return False

    with open(os.path.join(os.path.dirname(__file__), f"guilds\{guild_id}.json"), "w") as file:
        file.write(guilds.get(guild_id).to_JSON())
    return True


def delete_guild(guild_id: int) -> bool:
    """Deletes the player database of a guild from the disk. Returns `True` if it was successful, or else `False`
    """

    global guilds

    if guild_id == None:
        return False

    if guilds.get(guild_id) == None:
        return False

    guilds[guild_id] = None

    if os.path.exists(os.path.join(os.path.dirname(
            __file__), f"guilds\{guild_id}.json")):
        os.remove(os.path.join(os.path.dirname(
            __file__), f"guilds\{guild_id}.json"))
        return True

    return False


def get_guild(guild_id: int) -> GuildEntry:
    """Returns the GuildEntry for a given `guild_id`.
        Returns None if `guild_id` is None

        Arguments:
            - `guild_id` ID of the requested Guild
    """

    global guilds

    if guild_id == None:
        return None

    return guilds.get(guild_id)


def set_guild(guild_id: int, guild: GuildEntry) -> bool:
    """Sets the GuildEntry for a given `guild_id`.
        Creates a new GuildEntry if the `guild_id` is not in the Guilds dict.
        Returns False if `guild_id` is None or `guild_id` is already set.

        Arguments:
            - `guild_id` ID of the requested Guild
            - `guild` GuildEntry that should be added to the guilds
    """

    global guilds

    if guild_id == None:
        return False

    if guilds.get(guild_id) != None:
        # return false, because this guild already has a configuration entry
        return False

    guilds[guild_id] = guild
    return True
