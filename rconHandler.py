import enum
import os
from subprocess import STDOUT, check_output, CalledProcessError

from discord.guild import Guild

import config
from data import dataInterface
from data.GuildEntry import GuildEntry


def run_rcon_command(command: str, guild: GuildEntry) -> bool:
    """Connect to a Minecraft RCON server and execute a minecraft command using mrcon in the console: \n
        `mrcon -H rcon_address -P rcon_port -p rcon_password "command"`

    Attributes:
      - `command` A valid minecraft server command
      - `guild` A GuildEntry containing the rcon configuration of a guild
    """
    if guild == None:
        return False

    try:
        print(check_output([os.path.join(
            config.RCON_PATH, "mrcon"),
            "-H", guild.rcon_address,
            "-P", guild.rcon_port,
            "-p", guild.rcon_password,
            f'"{command}"'],
            stderr=STDOUT))
        return True

    except CalledProcessError as e:
        print(
            f"THE FOLLOWING ERROR OCCURED WHILE TRYING TO CALL MRCON: \n \n {e.stderr}")
        return False


class Command(enum.Enum):
    ADD = 0
    REMOVE = 1


def whitelist(command: Command, guild_id: int, user_id: int) -> bool:
    """Executes a whitelist command using rcon. \
        Can get a users status, add a user to the whitelist and remove a user from the whitelist.\
        Returns 'True' or the username if the command was successful, and 'False' if it wasnt.

    Attributes:
      - `command` A command from the available commands (ADD, REMOVE)
      - `user_id` The command senders Discord ID
      - `guild_id` The command senders Guild ID
    """

    if guild_id == None or user_id == None or command == None:
        print(
            f"whitelist - Invalid paramaters: {command}, {guild_id}, {user_id}")
        return False

    guild: GuildEntry = dataInterface.guild_by_id(guild_id)

    if guild.player_by_id(user_id) == None:
        # Discord User has not registered their username
        return False

    if command is Command.ADD:
        return run_rcon_command(f"whitelist add {guild.player_by_id(user_id)}", guild)

    if command is Command.REMOVE:
        return run_rcon_command(
            f"whitelist remove {guild.player_by_id(user_id)}", guild)
