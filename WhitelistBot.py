import os, json
import discord

import config

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


if __name__ == "__main__":
    client.run(config.BOT_TOKEN)