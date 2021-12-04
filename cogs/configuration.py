import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(ConfigCog(bot))

class ConfigCog(commands.Cog, command_attrs=dict(alias=["config", "configuration"]),name= "<:utility:908438154841849927> Config Help", description="Commands to configureate the bot to the servers needs\n`{prefix}help config`\n`{prefix}help configuration`"):
    def __init__(self, bot):
        self.bot = bot