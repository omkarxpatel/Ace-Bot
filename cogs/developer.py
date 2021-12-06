from discord.ext import commands
import io
import re
import sys
import importlib
import asyncio
import typing
import discord
import datetime
import textwrap
import os
import traceback
from utils.buttons import ButtonPaginator
from contextlib import redirect_stdout

def setup(bot):
    bot.add_cog(DeveloperCog(bot))

class DeveloperCog(commands.Cog, name="<:developerdarkblue:915125525889036299> Developer", command_attrs=dict(alias=['dev', 'developer'], emoji="<:developerdarkblue:915125525889036299>"), description="Commands that only the developers of the bot can use\n`{prefix}help dev`\n`{prefix}help developer`"):
    """
    Commands that only the developers of the bot can use
    """
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')
        
    @commands.command(pass_context=True, hidden=True, name='eval')
    @commands.is_owner()
    async def eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(help="Reloads all extensions", aliases=['relall', 'rall'], usage="[silent|channel]")
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def reloadall(self, ctx, argument: typing.Optional[str]):
        self.bot.last_rall = datetime.datetime.utcnow()
        cogs_list = ""
        to_send = ""
        err = False
        first_reload_failed_extensions = []
        if argument == 'silent' or argument == 's':
            silent = True
        else:
            silent = False
        if argument == 'channel' or argument == 'c':
            channel = True
        else:
            channel = False

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                cogs_list = f"{cogs_list} \n<a:ading:910197216835158076> {filename[:-3]}"

        embed = discord.Embed(color=discord.Color.green(), description=cogs_list)
        message = await ctx.send(embed=embed)

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    self.bot.reload_extension("cogs.{}".format(filename[:-3]))
                    to_send = f"{to_send} \n<a:tick:912173533151514655> Loaded - `{filename[:-3]}`"
                except Exception:
                    first_reload_failed_extensions.append(filename)

        for filename in first_reload_failed_extensions:
            try:
                self.bot.reload_extension("cogs.{}".format(filename[:-3]))
                to_send = f"{to_send} \n<a:tick:912173533151514655> Loaded `{filename[:-3]}`"

            except discord.ext.commands.ExtensionNotLoaded:
                to_send = f"{to_send} \n<a:tickfalse:912178613258969098> Not loaded - `{filename[:-3]}`"
            except discord.ext.commands.ExtensionNotFound:
                to_send = f"{to_send} \n<a:tickfalse:912178613258969098>  Not found - `{filename[:-3]}`"
            except discord.ext.commands.NoEntryPointError:
                to_send = f"{to_send} \n<a:tickfalse:912178613258969098> No setup func - `{filename[:-3]}`"
            except discord.ext.commands.ExtensionFailed as e:
                traceback_string = "".join(traceback.format_exception(etype=None, value=e, tb=e.__traceback__))
                to_send = f"{to_send} \n<a:tickfalse:912178613258969098> Execution error - `{filename[:-3]}`"
                embed_error = f"\n<a:tickfalse:912178613258969098> Execution error - Traceback `{filename[:-3]}`" \
                              f"\n```py\n{traceback_string}\n```"
                if not silent:
                    target = ctx if channel else ctx.author
                    if len(embed_error) > 2000:
                        await target.send(file=io.StringIO(embed_error))
                    else:
                        await target.send(embed_error)

                err = True

        await asyncio.sleep(0.4)
        if err:
            if not silent:
                if not channel:
                    to_send = f"{to_send} \n\n📬 {ctx.author.mention}, I sent you all the tracebacks."
                else:
                    to_send = f"{to_send} \n\n📬 Sent all tracebacks here."
            if silent:
                to_send = f"{to_send} \n\n📭 silent, no tracebacks sent."
            embed = discord.Embed( title='Reloaded some extensions', description=to_send, color=discord.Color.green())
            await message.edit(embed=embed)
        else:
            embed = discord.Embed(title='Reloaded all extensions', description=to_send, color=discord.Color.green())
            await message.edit(embed=embed)
            channel = self.bot.get_channel(912234535758991380)
            await channel.send(embed=embed)     

    @commands.command(hidden=True)
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.group(name='reload', hidden=True, invoke_without_command=True)
    async def _reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    _GIT_PULL_REGEX = re.compile(r'\s*(?P<filename>.+?)\s*\|\s*[0-9]+\s*[+-]+')

    def find_modules_from_git(self, output):
        files = self._GIT_PULL_REGEX.findall(output)
        ret = []
        for file in files:
            root, ext = os.path.splitext(file)
            if ext != '.py':
                continue

            if root.startswith('cogs/'):

                ret.append((root.count('/') - 1, root.replace('/', '.')))

        ret.sort(reverse=True)
        return ret

    def reload_or_load_extension(self, module):
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionNotLoaded:
            self.bot.load_extension(module)

    @_reload.command(name='all', hidden=True)
    async def _reload_all(self, ctx):
        """Reloads all modules, while pulling from git."""

        async with ctx.typing():
            stdout, stderr = await self.run_process('git pull')

        if stdout.startswith('Already up-to-date.'):
            return await ctx.send(stdout)

        modules = self.find_modules_from_git(stdout)
        mods_text = '\n'.join(f'{index}. `{module}`' for index, (_, module) in enumerate(modules, start=1))
        prompt_text = f'This will update the following modules, are you sure?\n{mods_text}'
        confirm = await ctx.prompt(prompt_text, reacquire=False)
        if not confirm:
            return await ctx.send('Aborting.')

        statuses = []
        for is_submodule, module in modules:
            if is_submodule:
                try:
                    actual_module = sys.modules[module]
                except KeyError:
                    statuses.append((ctx.tick(None), module))
                else:
                    try:
                        importlib.reload(actual_module)
                    except Exception as e:
                        statuses.append((ctx.tick(False), module))
                    else:
                        statuses.append((ctx.tick(True), module))
            else:
                try:
                    self.reload_or_load_extension(module)
                except commands.ExtensionError:
                    statuses.append((ctx.tick(False), module))
                else:
                    statuses.append((ctx.tick(True), module))

        await ctx.send('\n'.join(f'{status}: `{module}`' for status, module in statuses))
    @commands.command()
    async def credits(self, ctx):
      embed = discord.Embed(title="Acknowledgements", description="`Squirrels#2499`\n╰ Owner\n`Rose🌹#1328`\n╰ Developer :)\n`DaPandaOfficial🐼#5684`\n╰ Helped with the music cog and parts of commands :)\n`Official DPY server`\n╰ Helped answer my dumb questions\n╰ `discord.gg/dpy`")
      await ctx.send(embed=embed)

    @commands.command(aliases=['sl'])
    @commands.is_owner()
    async def serverlist(self, ctx):
        embed_list = [] 
        guild_list = self.bot.guilds
        guild_seperated = [guild_list[i:i + 5] for i in range(0, len(guild_list), 5)]
        for guilds in guild_seperated:
            em = discord.Embed(title="Server List", description="")
            for guild in guilds:
                em.description += f"**__{guild.name}__**\nﾠ**Guild Information:**\nㅤ**Owner:** `{guild.owner}` <:owner:907296832642764822>\nㅤㅤ**Owner ID:** `{guild.owner.id}`\nㅤㅤ**Guild ID:** `{guild.id}`\n\n"
            embed_list.append(em)
        view = ButtonPaginator(another_list=embed_list, ctx=ctx)
        view.message = await ctx.send(embed=embed_list[0], view=view)