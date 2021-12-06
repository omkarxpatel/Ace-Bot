import discord
import inspect
from discord.ext import commands


def setup(bot):
    bot.add_cog(ConfigCog(bot))

class ConfigCog(commands.Cog, command_attrs=dict(alias=["config", "configuration"], emoji="<:utility:908438154841849927"),name= "<:utility:908438154841849927> Configuration", description="Commands to configureate the bot to the servers needs\n`{prefix}help config`\n`{prefix}help configuration`"):
    def __init__(self, bot):
        self.bot = bot
        self.cache = {}

    @commands.command(brief="Change prefix for your server")
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx, prefix: str = None):
        """
        Change prefix of the bot for server-to-server
        """
        request = await self.bot.db.prefix.find_one({'guild_id': ctx.guild.id})
        if prefix is None and request is not None:
            del self.bot.prefix[ctx.guild.id]
            await self.bot.db.prefix.delete_one({'guild_id': ctx.guild.id})
            default_pre = await self.bot.command_prefix(self.bot, ctx.message)
            return await ctx.send(f"Switched back the prefix to default: {default_pre}")
        elif prefix is None and request is None:
            param = inspect.Parameter('prefix', inspect.Parameter.POSITIONAL_OR_KEYWORD,default=inspect.Parameter.empty, annotation=inspect.Parameter.empty)
            raise commands.MissingRequiredArgument(param)
        if len(prefix) > 15:
            return await ctx.send("too big for a prefix, please keep it less than 15 characters!")
        elif prefix is not None and request is None:
            document = {'guild_id': ctx.guild.id, 'prefix': prefix}
            await self.bot.db.prefix.insert_one(document)
            return await ctx.send(f"Successfully set the new prefix to: `{prefix}`")
        elif prefix is not None and request is not None:
            document = {'prefix': prefix}
            self.bot.prefix[ctx.guild.id] = str(prefix)
            await self.bot.db.prefix.update_one({'guild_id': ctx.guild.id}, {'$set': document})
            return await ctx.send(f"Successfully set the new prefix to: `{prefix}`")

    @commands.group(invoke_without_command=True)
    async def setlog(self, ctx):
        return await ctx.send_help(ctx.command)

    @setlog.group(invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def role(self, ctx):
        request = await self.bot.db.logging.find_one({'_id': ctx.guild.id})
        if not request:
            role_create = "`None`"
            role_delete = "`None`"
        else:
            role_create = "`None`" if not request.get('role_create_log_channel') else ctx.guild.get_channel(request.get('role_create_log_channel'))
            role_delete = "`None`" if not request.get('role_delete_log_channel') else ctx.guild.get_channel(request.get('role_delete_log_channel'))
            if isinstance(role_create, discord.TextChannel):
                role_create = role_create.mention
            if isinstance(role_delete, discord.TextChannel):
                role_delete = role_delete.mention
        embed = discord.Embed(title="Your current configuration", description=f"**Role Create Log**: {role_create}\n**Role Delete Log**: {role_delete}")
        embed.set_footer(text=f'Use {ctx.prefix}setlog role create/delete to set logging channel', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @role.command(name="create")
    @commands.has_permissions(manage_guild=True)
    async def _create(self, ctx: commands.Context, channel: discord.TextChannel):
        embed = discord.Embed(title="Role Create channel has been set!", description=f"{channel.mention} has been set as role create logging channel")
        try:
            self.cache[ctx.guild.id]['role_create_channel']
        except KeyError:        
            request = await self.bot.db.logging.find_one({'_id': ctx.guild.id})
            if not request:
                document = {'_id': ctx.guild.id, 'role_create_log_channel': channel.id}
                await self.bot.db.logging.insert_one(document)
                try:
                    self.cache[ctx.guild.id]['role_create_channel'] = channel.id 
                except KeyError:
                    self.cache[ctx.guild.id] = {}
                    self.cache[ctx.guild.id]['role_create_channel'] = channel.id
                return await ctx.send(embed=embed)
            print(request)
            self.cache[ctx.guild.id] = {}
            self.cache[ctx.guild.id]['role_create_channel'] = channel.id
            document = {'role_create_log_channel': channel.id}
            await self.bot.db.logging.update_one({'_id': ctx.guild.id}, {'$set': document})
            return await ctx.send(embed=embed)
        self.cache[ctx.guild.id]['role_create_channel'] = channel.id
        document = {'role_create_log_channel': channel.id}
        await self.bot.db.logging.update_one({'_id': ctx.guild.id}, {'$set': document})
        return await ctx.send(embed=embed)             

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        try:
            cached_channel = self.cache[role.guild.id]['role_create_log_channel']
            if cached_channel is None:
                return
        except KeyError:
            request = await self.bot.db.logging.find_one({'_id': role.guild.id})
            if not request:
                self.cache[role.guild.id] = None
                return
            self.cache[role.guild.id] = {}
            self.cache[role.guild.id]['role_create_channel'] = request['role_create_log_channel']
            cached_channel = request['role_create_log_channel']
        guild = self.bot.get_guild(role.guild.id)
        channel = guild.get_channel(cached_channel)
        if not channel:
            document = {'role_create_log_Channel': 1}
            await self.bot.db.logging.update_one({'_id': role.guild.id}, {'$unset': document})
            self.cache[role.guild.id]['role_create_channel'] = None    
            return
        audits = await guild.audit_logs(limit=2, action = discord.AuditLogAction.role_create).flatten()
        new = [x for x in audits if x.target == role][0]
        user = new.user
        role_list = guild.roles[-5 if role.position > 5 else 0:5]
        role_integration = '\n'.join([(f'{position}. > {role}' if mrole == role else f'{position}.   {mrole}') for (position, mrole) in enumerate(role_list)])
        embed = discord.Embed(title="A Role has been created", description=f"**Role**: {role.mention}\n**ID**: {role.id}\n**Position:**\n```py\n{role_integration}\n```", timestamp=role.created_at)
        embed.set_footer(text=f"Created By: {user} | {user.id}")
        await channel.send(embed=embed)
        
