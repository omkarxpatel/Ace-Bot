import discord
from utils import slash_util

class MyCog(slash_util.ApplicationCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot

    @slash_util.slash_command()  # sample slash command
    async def slash(self, ctx: slash_util.Context, number: int):
        await ctx.send(f"You selected #{number}!", ephemeral=True)
    
    @slash_util.message_command(name="Quote")  # sample command for message context menus
    async def quote(self, ctx: slash_util.Context, message: discord.Message):  # these commands may only have a single Message parameter
        await ctx.send(f'> {message.clean_content}\n- {message.author}')
    
    @slash_util.user_command(name='Bonk')  # sample command for user context menus
    async def bonk(self, ctx: slash_util.Context, user: discord.Member):  # these commands may only have a single Member parameter
        await ctx.send(f'{ctx.author} BONKS {user} :hammer:')

def setup(bot):
    bot.add_cog(MyCog(bot))