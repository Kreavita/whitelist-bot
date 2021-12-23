import enum
import subprocess


class Command(enum.Enum):
    GET = 0
    ADD = 1
    REMOVE = 2


def whitelist(command: Command, user_id: str, guild_id: str) -> bool:
    """Executes a whitelist command using rcon. \
        Can get a users status, add a user to the whitelist and remove a user from the whitelist.\
        Returns 'True' if the command was successful, and 'False' if it wasnt.

    Attributes:
      command, user_id guild_id
    """
    if user_id == None or guild_id == None or command == None:
        print(
            f"whitelist - Invalid paramaters: {command}, {guild_id}, {user_id}")
        return False

    return True


def set_ingame_name(user_id: str, guild_id: str, username: str) -> bool:
    """Sets the users ingame name for a specific guild. \
        Returns 'True' if it was successful and 'False' otherwise.

    Attributes:
      user_id guild_id username
    """
    if user_id == None or guild_id == None or username == None:
        print(
            f"set_ingame_name - Invalid paramaters: {user_id}, {guild_id}, {username}")
        return False

    return True
