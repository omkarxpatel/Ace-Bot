#imports
import os
import sys
import aiohttp
import discord
import warnings
import traceback
from utils import slash_util
from pathlib import Path
from colorama import Fore
from discord.ext import commands
from keep_alive import keep_alive
from motor.motor_asyncio import AsyncIOMotorClient as MotorClient

warnings.filterwarnings("ignore", category=DeprecationWarning)
#defines the restart_bot
def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)


async def get_prefix(bot, message: discord.Message) -> list:
    try:
        prefix = bot.prefix[message.guild.id]
    except KeyError:
        request = await bot.db.prefix.find_one({'guild_id': message.guild.id})
        if request is None:
            prefix =  ['ace.', 'Ace.']
        else:
            bot.prefix[request['guild_id']] = [request['prefix']]
            prefix = [request['prefix']]
    except AttributeError:
        prefix =  ['ace.', 'Ace.', 'I needed a prefix where no one else used it so then there would be less spam.']
    return prefix

class MyBot(slash_util.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bot_session = aiohttp.ClientSession()
        self.webhook = discord.SyncWebhook.from_url('https://discord.com/api/webhooks/916082535119847464/XX2dhZGAgSNgY67wBJLoKdWO800QvlNLsmdjPmrVWjfmoWc-XXLQBb_qBh1yr66HPGQ2')

    # jishaku environment variables  
    os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
    os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
    os.environ["JISHAKU_HIDE"] = "True"
    os.environ["JISHAKU_RETAIN"] = "True"

    def __str__(self):
        return bot.user.name

    @property
    def session(self):
        return self.bot_session
  
    # on ready event
    async def on_ready(self):
        await bot.wait_until_ready()
        print(Fore.MAGENTA + "========[" + bot.user.name +
              " is Online! ]========" + Fore.RESET)
        print(Fore.RED + "========[ Discord Version: " + discord.__version__ +
              " ]========")
        embed = discord.Embed(title=f'{bot.user.name} Is Now Online',
                              timestamp=discord.utils.utcnow(),
                              color=discord.Color.green())
        self.webhook.send(embed=embed)
        

    

#defines bot
bot = MyBot(command_prefix=get_prefix,
                   intents=discord.Intents.all(),
                   activity=discord.Activity(
                       type=discord.ActivityType.listening, name="ace.help"),
                    owner_ids=[706242014056022027, 914596711010287698, 801190526350786560],
                    help_command=None)

mongo = MotorClient(os.environ['MONGO']) 
bot.db = mongo.discord
bot.load_extension('jishaku')
bot.prefix = {}



#loading all files
for file in Path('cogs').glob('**/*.py'):
    *tree, _ = file.parts
    try:
        bot.load_extension(f"{'.'.join(tree)}.{file.stem}")
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)

#restarts the bot
@bot.command()
@commands.is_owner()
async def restart(ctx):
    embed = discord.Embed(title="Restarting The Bot",
                          description=f'Developer: {ctx.author.mention}',
                          color=discord.Color.blue())
    await ctx.send(embed=embed)
    restart_bot()

#host for bot
keep_alive()
#token
try:
    token = os.environ["TOKEN"]
    bot.run(token, reconnect=True)

#offline cmd
finally:
    webhook = discord.SyncWebhook.from_url('https://discord.com/api/webhooks/916082535119847464/XX2dhZGAgSNgY67wBJLoKdWO800QvlNLsmdjPmrVWjfmoWc-XXLQBb_qBh1yr66HPGQ2')
    webhook.send(content='Ace Bot is Now Offline 🛑')