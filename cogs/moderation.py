import discord
from discord.ext import commands
from typing import Union
import asyncio

def setup(bot):
    bot.add_cog(ModerationCog(bot))


class ModerationCog(commands.Cog, name="<:moderation:907802138296606740> Moderation", 
                    command_attrs=dict(alias=['mod', 'moderation'], emoji="<:moderation:907802138296606740>"), description="Moderation commands to moderate your server\n`{prefix}help mod`\n`{prefix}help moderation`"):
    """
    Moderation commands to moderate your server
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author == member:
            return await ctx.reply('You can\'t ban yourself...?')
        if ctx.author.top_role.position <= member.top_role.position:
            return await ctx.reply('You can\'t ban a member who has an equal or higher role than yourself')
        elif ctx.author.top_role.position > member.top_role.position and ctx.guild.me.top_role <= member.top_role.position:
            return await ctx.reply('I can\'t ban a member whose role position is higher than mine.')
        ban = discord.Embed(title=f":boom: Banned {member.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await member.send(embed=ban)
        await asyncio.sleep(0.2)
        await member.ban(reason=reason)
        await ctx.send(embed=ban)
      

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if ctx.author == member:
            return await ctx.reply('You can\'t ban yourself...?')
        if ctx.author.top_role.position <= member.top_role.position:
            return await ctx.reply('You can\'t ban a member who has an equal or higher role than yourself')
        elif ctx.author.top_role.position > member.top_role.position and ctx.guild.me.top_role <= member.top_role.position:
            return await ctx.reply('I can\'t ban a member whose role position is higher than mine.')
        kick = discord.Embed(title=f":boom: Kicked {member.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await member.send(embed=kick)
        await ctx.channel.send(embed=kick)
        await member.kick(reason=reason)   

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if ctx.author == member:
            return await ctx.reply('You can\'t ban yourself...?')
        if ctx.author.top_role.position <= member.top_role.position:
            return await ctx.reply('You can\'t ban a member who has an equal or higher role than yourself')
        elif ctx.author.top_role.position > member.top_role.position and ctx.guild.me.top_role <= member.top_role.position:
            return await ctx.reply('I can\'t ban a member whose role position is higher than mine.')
        ban = discord.Embed(title=f"Soft-Banned {member.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.author.send(embed=ban)
        await member.send(embed=ban)
        await ctx.message.delete()
        await ctx.channel.send(embed=ban)
        await member.ban(reason=reason)    
        await asyncio.sleep(1)
        await member.unban(reason="Soft unban")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, *, user: Union[discord.User, str] = None):
        if not user:
            await ctx.reply('You need to pass the ID of the user you want to unban')
        if isinstance(user, discord.User):
            try:
                await ctx.guild.unban(user, reason=f"Responsible Moderator: {ctx.author}")
                return await ctx.send(f"Successfully unbanned {user.mention}!")
            except discord.NotFound:
                return await ctx.reply('I couldn\'t find any such user in bans list')
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        ban_users = tuple(str(ban_entry.user) for ban_entry in await ctx.guild.bans())
        if user in ban_users:
            user = bans[ban_users.index(user)]
            await ctx.guild.unban(user, reason="Responsible moderator: "+ str(ctx.author))
        else:
            return await ctx.send("Could not find the user in bans list")
        await ctx.send(f"Successfully unbanned {user.mention}!")
        
    @commands.command(aliases=['tempmute'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member=None, time=None, *, reason=None):
        if not member:
            await ctx.send("You must mention a member to mute!")
            return
        elif not time:
            await ctx.send("You must mention a time!")
            return
        else:
            if not reason:
                reason="No reason given"
        try:
            time_interval = time[:-1] 
            duration = time[-1]
            if duration == "s":
                time_interval = time_interval * 1
            elif duration == "m":
                time_interval = time_interval * 60
            elif duration == "h":
                time_interval = time_interval * 60 * 60
            elif duration == "d":
                time_interval = time_interval * 86400
            else:
                await ctx.send("Invalid duration input")
                return
        except Exception as e:
            print(e)
            await ctx.send("Invalid time input")
            return
        guild = ctx.guild
        Muted = discord.utils.get(guild.roles, name="Muted")
        if not Muted:
            Muted = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(Muted, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        else:
            await member.add_roles(Muted, reason=reason)
            muted_embed = discord.Embed(title="Muted a user", description=f"{member.mention} Was muted\n**Moderator:** {ctx.author.mention}\n **Reason:** {reason}\n**Durtaion:** {time}")
            await ctx.send(embed=muted_embed)
            await asyncio.sleep(int(time_interval))
            await member.remove_roles(Muted)
            unmute_embed = discord.Embed(title='Mute over!', description=f'The mute on {member.mention} is over\n**Moderator:** {ctx.author.mention}\n**Reason:** {reason}\n**Duration:** {time}')
            await ctx.send(embed=unmute_embed)
            await member.send(embed=unmute_embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member, reason: str = None):
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(muted)
        await ctx.send(f"{member.mention} has been unmuted.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def slowmode(self, ctx, time=None):
        if not time:
            embed0 = discord.Embed(description='Slowmode disabled!')
            await ctx.send(embed=embed0)
            await ctx.channel.edit(slowmode_delay=0)
            return
        await ctx.channel.edit(slowmode_delay=time)
        embed = discord.Embed(description=f"Slowmode is now {time}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lock(self, ctx, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(description=f':lock: {channel} is now locked.')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed=discord.Embed(description=f':unlock: {channel} is now unlocked.')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, limit=5, member: discord.Member=None):
        await ctx.message.delete()
        msg = []
        try:
            limit = int(limit)
        except:
            return await ctx.send("Please pass in an integer as limit")
        if not member:
            await ctx.channel.purge(limit=limit)
            return await ctx.send(f"Purged {limit} messages", delete_after=3)
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)
        await ctx.channel.delete_messages(msg)
        await ctx.send(f"Purged {limit} messages of {member.mention}", delete_after=3)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def archive(self, ctx, channel : discord.TextChannel=None, reason="No reason provided"):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        embed=discord.Embed(title="Channel Archived", description=f"Channel name: #{channel}\nReason: {reason}")
        await ctx.send(embed=embed)
        await channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unarchive(self, ctx, channel : discord.TextChannel=None, reason="No reason provided"):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, view_channel=None)
        embed=discord.Embed(title="Channel Unarchived", description=f"Channel name: #{channel}\nReason: {reason}")
        await ctx.send(embed=embed)
        await channel.send(embed=embed)