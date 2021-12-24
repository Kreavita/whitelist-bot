# whitelist-bot
A simple Discord Bot that allows discord users to whitelist themselves on their guilds minecraft servers, if the admins have added and configured the bot on their guild.

## Requirements
- Python 3 (Tested with Python 3.8 and 3.9 on Ubuntu 20.04)
- discord.py
- an `mcrcon` installation on your server

You need to create a `config.py` in the main directory that contains two variables:
- `RCON_PATH: str` path to the directory where the `mcrcon` executable is at
- `BOT_TOKEN: str` token for your Discord Application on [discord.com/developers/applications](https://discord.com/developers/applications)
