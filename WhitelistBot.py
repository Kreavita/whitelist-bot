import os, json
import discord

import secrets

guild_config = []

def whitelist_bot():
    global serverData
    with open('guildConfigs.json') as file:
        servers = json.load(file)


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


if __name__ == "__main__":
    client.run(secrets.BOT_TOKEN)
    whitelist_bot()