import discord
from discord.ext import commands
from utils import buttons


def setup(bot):
    bot.add_cog(Ticket(bot))
    
class Ticket(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx: commands.Context):
        view = buttons.TButton()
        embed1=discord.Embed(title="Create a ticket?", description="Confirm if you would like to create this ticket.")
        await ctx.send(embed=embed1, view=view)
        await view.wait()
        if view.value is None:
            await ctx.send('Timed out...', delete_after=2)
        elif view.value:
            ticket_channel = await ctx.guild.create_text_channel("ticket-{}".format(ctx.author.name))
            await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
            await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
            embed = discord.Embed(title='New Ticket!',description='Please be patient, help will arive shortly.')
            await ticket_channel.send(embed=embed)
            await ticket_channel.send(f"{ctx.author.mention}")
            embed = discord.Embed(description=f'{ctx.author.mention}, your ticket has been created: {ticket_channel.mention}')
            await ctx.send(embed=embed, delete_after=60)

    @commands.command()
    async def close(self, ctx: commands.Context):
        embed = discord.Embed(title="Ace Bot Tickets", description="Are you sure you want to close this ticket?", color=0x00a8ff)
        view = buttons.Close()
        await ctx.send(embed=embed, view=view)
        if view.value:
          await ctx.channel.set_permissions(ctx.author, read_messages=False)
        else:
          await ctx.send("Canceled...", delete_after=2)