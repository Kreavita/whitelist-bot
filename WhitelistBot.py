from discord import Client, Member, Message, User, Game
from discord.flags import Intents
from discord.guild import Guild

import config
from rconHandler import Command, whitelist
from data import dataInterface
from data.GuildEntry import GuildEntry


class WhitelistBot(Client):
    async def on_ready(self):
        await self.change_presence(activity=Game("whitelist yourself with /whitelist - Bot by @Kreavita"))
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message: Message):
        """ Handles Discord Messages Events
        """
        if message.author == self.user:
            # We dont need to handle this bot's messages
            return

        if not type(message.author) is Member:
            # Handle private messages (RCON) in a different function
            self.private_message(message)
            return

        if not message.content.startswith('/whitelist'):
            # in guild chat, only whitelist commands are allowed.
            # RCON config needs to be done in private messages (PRIVACY!)
            return

        author: Member = message.author
        params = (message.content.split(" ")[1:])

        if len(params) != 1:
            await message.channel.send(f'{author.mention} Usage: `/whitelist <Minecraft-Username>`')
            return

        guild: GuildEntry = dataInterface.get_guild(author.guild.id)

        if guild is None:
            await message.channel.send(f'{author.mention} WhitelistBot has not been configured on this server. If you think this is an error, contact this servers admins.')
            return

        if guild.player_by_id(author.id) == params[0].lower():
            await message.channel.send(f'{author.mention} You are already whitelisted, Nothing changed!')
            return

        if guild.id_by_player(params[0]) != None:
            await message.channel.send(f'{author.mention} The username `{params[0]}` has already been whitelisted by someone else! If you think this is an error, ask an Admin to manually whitelist you.')
            return

        if guild.players.get(author.id) != None:
            if not whitelist(Command.REMOVE, author.guild.id, author.id):
                await message.channel.send(f'{author.mention} An internal error occured while trying to whitelist your username, maybe a faulty RCON configuration?')
                return

            await message.channel.send(f'{author.mention} Your old minecraft account, `{guild.players.get(author.id)}`, is no longer whitelisted!')

        guild.set_player(author.id, params[0])

        if not whitelist(Command.ADD, author.guild.id, author.id):
            await message.channel.send(f'{author.mention} An internal error occured while trying to whitelist your username, maybe a faulty RCON configuration?')
            return

        await message.channel.send(f'{author.mention} Your minecraft account `{params[0]}` has been added to the Whitelist!')
        print(
            f"'{author.name}' whitelisted his name '{params[0]}' on '{guild.name}'")

    usage_string: str = 'Sorry, the command you entered was not correct.\n' +\
        'Bot Usage: \n' + \
        '`/ enable < Server-ID > <RCON-Host: Port > <RCON-password >` to enable the bot for your server or update the config\n' + \
        '`/ disable < Server-ID >` to remove the server from the whitelist. This will keep your whitelist, but delete the configuration on our servers.'

    async def private_message(self, message: Message):
        """ Handles Private Discord Messages.
            Gets Called by the on_message Event Handler, if the channel is a Private Message.
        """
        author: User = message.author
        message_content = (message.content.split(" ")[1:])

        if len(message_content) < 2:
            await message.channel.send(self.usage_string)
            return

        selectedGuild: Guild = 0

        for guild in self.guilds:
            if guild.id == int(message_content[1]):
                selectedGuild = guild.id
                break

        if selectedGuild == 0:
            await message.channel.send(f"Error - Server not found! Make sure I am added to this Server.")
            return

        member: Member = selectedGuild.get_member(author.id)

        if member == None or not member.guild_permissions.manage_guild():
            await message.channel.send(f"You need the 'Manage Server' permission on '{selectedGuild.name}' to manage the whitelist integration!")
            return

        if message_content[0] == "/disable" and len(message_content) >= 2:
            if dataInterface.delete_guild(selectedGuild.id):
                await message.channel.send(f"WhitelistBot has been successfully disabled for '{selectedGuild.name}'!")
                print(f"'{author.name}' deleted the whitelist for '{guild.name}'")
            else:
                await message.channel.send(f"WhitelistBot on '{guild.name}' is already disabled.")
            return

        if message_content[0] == "/enable" and len(message_content) >= 4:

            rcon_data = message_content[2].split(":")

            if len(rcon_data) != 2:
                await message.channel.send(f'{author.mention} Usage: `/enable <Server-ID> <RCON-Host:Port> <RCON-password>`')
                return

            rcon_address: str = rcon_data[0]

            try:
                rcon_port: int = int(rcon_data[1])
            except ValueError as e:
                await message.channel.send(f'{author.mention} Usage: `/enable <Server-ID> <RCON-Host:Port> <RCON-password>`')
                return

            rcon_password: str = "".join(message_content[3:])

            guildConfig: GuildEntry = dataInterface.get_guild(
                selectedGuild.id)

            if not guildConfig is None:
                guildConfig.rcon_address = rcon_address
                guildConfig.rcon_port = rcon_port
                guildConfig.rcon_password = rcon_password

                await message.channel.send(
                    f"Whitelist on '{guild.name}' is already enabled, RCON configuration has been updated!")
            else:
                dataInterface.set_guild(selectedGuild.id, GuildEntry(
                    selectedGuild.id, rcon_address, rcon_port, rcon_password))

                await message.channel.send(
                    f"Whitelist Listener on '{guild.name}' has been successfully enabled!")

            print(
                f"'{author.name}' set up WhitelistBot for '{guild.name}' listening on RCON Server '{message_content[2]}'")
            return

        # If we land here, no command has been executed, so we print the usage string
        await message.channel.send(self.usage_string)
        return

    async def on_member_leave(self, member: Member):
        """ Handles Members Leaving
        """
        guild: GuildEntry = dataInterface.get_guild(member.guild.id)

        if(not guild is None and guild.player_by_id(member.id) != None):
            whitelist(Command.REMOVE, member.guild.id, member.id)
            print(f"'{member.name}' left the guild '{member.guild.name}' and their minecraft account, '{guild.player_by_id(member.id)}', has been removed from the whitelist.")


if __name__ == "__main__":
    intents: Intents = Intents.default()
    intents.members = True

    client = WhitelistBot(intents=intents)
    client.run(config.BOT_TOKEN)
