import sys
import io
import traceback
import discord
import humanize
from datetime import datetime as dt
from utils.errors import OnCooldown
from discord.ext import commands

class ServerInvite(discord.ui.View):
    def __init__(self ,bot):
        super().__init__()
        self.add_item(discord.ui.Button(emoji='<:addinvite:907296700127911976>', label='Support Server', url='https://discord.gg/7pETYGfQ'))

def setup(bot):
    bot.add_cog(ErrorHandler(bot))

class ErrorHandler(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.error_channel = 912205104919240714

    @commands.Cog.listener('on_command_error') 
    async def on_command_error(self, ctx, error): 
        if isinstance(error, OnCooldown):
          time = humanize.precisedelta(dt.utcnow() - error.time)
          em = discord.Embed(title="Command is currently on cooldown!", description=f"Try again in `{time}`")
          return await ctx.send(embed=em) 
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"One or more of the arguments given was invalid. Please try again")
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        if isinstance(error, discord.ext.commands.CheckAnyFailure):
            for e in error.errors:
                if not isinstance(error, commands.NotOwner):
                    error = e
                    break
        if isinstance(error, commands.BotMissingPermissions):
            missing = [(e.replace('_', ' ').replace('guild', 'server')).title() for e in error.missing_permissions]
            perms_formatted = ", ".join(missing[:-2] + [" and ".join(missing[-2:])])
            return await ctx.send(f"I'm missing **{perms_formatted}** permissions!")
        if isinstance(error, discord.ext.commands.BadUnionArgument):
            if error.errors:
                error = error.errors[0]
        if isinstance(error, commands.NotOwner):
            return await ctx.send(embed=discord.Embed(title='Error occured',description=f"You must own `{ctx.me.display_name}` to use `{ctx.command}`"))
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            missing = f"{error.param.name}"
            command = f"{ctx.clean_prefix}{ctx.command} {ctx.command.signature}"
            separator = (' ' * (len([item[::-1] for item in command[::-1].split(missing[::-1], 1)][::-1][0]) - 1))
            indicator = ('^' * (len(missing) + 2))
            desc = (f"```diff\n+ {command}\n- {separator}{indicator}\n- {missing} "
                                  f"is a required argument that is missing.\n```")
                    
            return await ctx.send(embed=discord.Embed(title='Missing Arguments !', description=desc, color=discord.Color.red()))
        if isinstance(error, commands.TooManyArguments):
            return await ctx.send(embed=discord.Embed(title='Error occured',description=f"Too many arguments passed to the command!"))
        if isinstance(error, discord.ext.commands.MissingPermissions):
            missing = [(e.replace('_', ' ').replace('guild', 'server')).title() for e in error.missing_permissions]
            perms_formatted = ", ".join(missing[:-2] + [" and ".join(missing[-2:])])
            return await ctx.send(embed=discord.Embed(title='Error occured',description=f"You're missing **{perms_formatted}** permissions!"))
        else:
            error_channel = self.bot.get_channel(self.error_channel)

            traceback_string = "".join(traceback.format_exception(
                etype=None, value=error, tb=error.__traceback__))

            if ctx.guild:
                command_data = f"Invoked By: {ctx.author.display_name} ({ctx.author.name}#{ctx.author.discriminator})" \
                            f"\nCommand Name: {ctx.message.content[0:1700]}" \
                            f"\nGuild: Name: {ctx.guild.name}" \
                            f"\nGuild ID: {ctx.guild.id}" \
                            f"\nGuild Owner: {ctx.guild.owner.display_name} ({ctx.guild.owner.name}#{ctx.guild.owner.discriminator})" \
                            f"\nChannel: {ctx.channel.name} ({ctx.channel.id})"
            else:
                command_data = f"command: {ctx.message.content[0:1700]}" \
                            f"\nCommand executed in DMs"

            to_send = f"```yaml\n{command_data}``````py\n{ctx.command} " \
                    f"command raised an error:\n{traceback_string}\n```"
            if len(to_send) < 2000:
                try:
                    sent_error = await error_channel.send(to_send)

                except (discord.Forbidden, discord.HTTPException):
                    sent_error = await error_channel.send(f"```yaml\n{command_data}``````py Command: {ctx.command}"
                                                        f"Raised the following error:\n```",
                                                        file=discord.File(io.StringIO(traceback_string),
                                                                            filename='traceback.py'))
            else:
                sent_error = await error_channel.send(f"```yaml\n{command_data}``````py Command: {ctx.command}"
                                                    f"Raised the following error:\n```",
                                                    file=discord.File(io.StringIO(traceback_string),
                                                                        filename='traceback.py'))
            try:
                await sent_error.add_reaction('🗑')
            except (discord.HTTPException, discord.Forbidden):
                pass
            raise error
            
    @commands.Cog.listener('on_raw_reaction_add')
    async def wastebasket(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id == self.error_channel and await \
                self.bot.is_owner(payload.member) and str(payload.emoji == '🗑'):
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if not message.author == self.bot.user:
                return
            error = '```py\n' + '\n'.join(message.content.split('\n')[7:])
            await message.edit(content=f"{error}```fix\n✅ Marked as fixed by the developers.```")
            await message.clear_reactions()