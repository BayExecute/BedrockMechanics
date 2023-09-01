import discord, time
from discord.ext import commands
from dislash import slash_commands, Type

prefix = "?"

Bot = commands.Bot(command_prefix=prefix, help_command=None)
slash = slash_commands.SlashClient(Bot)


class TimeCommand(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @slash.command(name="time", description="Returns the time as number.")
    async def skin(self, inter, name=None):
        await inter.reply(f"{int(time.time())}")


def setup(Bot):
    Bot.add_cog(TimeCommand(Bot))
