import asyncio
import discord
import random
from utils import buttons
from discord.ext import commands
from utils import functions


def setup(bot):
    bot.add_cog(FunClass(bot))



class FunClass(commands.Cog, name="<:controller:915124129257111582> Fun", description="Fun commands to use around the server\n`{prefix}help fun`\n`{prefix}help games`", command_attrs=dict(alias=['games', 'fun'], emoji="<:controller:915124129257111582>")):
    """
    Fun commands to use around the server
    """
    def __init__(self, bot):
        self.bot = bot

    async def reddit(self, subreddit: str, title: bool = False, embed_type: str = 'IMAGE') -> discord.Embed:
        try:
            subreddit = await self.bot.reddit.subreddit(subreddit)
            post = await subreddit.random()

            if embed_type == 'IMAGE':
                while 'i.redd.it' not in post.url or post.over_18:
                    post = await subreddit.random()
                embed = discord.Embed(color=discord.Color.random(),
                                      description=f"🌐 [Post](https://reddit.com{post.permalink}) • "
                                                  f":arrow_up: {post.score} ({post.upvote_ratio * 100}%) "
                                                  f"• from [r/{subreddit}](https://reddit.com/r/{subreddit})")
                embed.title = post.title if title is True else None
                embed.set_image(url=post.url)
                return embed
            if embed_type == 'POLL':
                while not hasattr(post, 'poll_data') or not post.poll_data or post.over_18:
                    post = await (await self.bot.reddit.subreddit(subreddit)).random()

                iterations: int = 1
                options = []
                emojis = []
                for option in post.poll_data.options:
                    num = f"{iterations}\U0000fe0f\U000020e3"
                    options.append(f"{num} {option.text}")
                    emojis.append(num)
                    iterations += 1
                    if iterations > 9:
                        iterations = 1

                embed = discord.Embed(color=discord.Color.random(),
                                      description='\n'.join(options))
                embed.title = post.title if title is True else None
                return embed, emojis
        except Exception as error:
            print(error)
            return discord.Embed(description='Whoops! An unexpected error occurred')

    @commands.command()
    async def guess(self, ctx: commands.Context, number: int = 100):
        guesses = range(number)
        answer = random.choice(guesses)
        await ctx.send(f"A random number has been selected from 0 - {number}")
        condition = True
        counter = 0
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        while condition:
            try:
                message = await self.bot.wait_for('message', check=check)
            except asyncio.TimeoutError:
                embedtimeout = discord.Embed(title="You didnt respond on time!", description=f'The correct number was {answer}\n You guessed {counter} times')
                return await ctx.send(embed=embedtimeout)
            else:
                if message.content.lower() in ['end', 'cancel']:
                    embedcancel = discord.Embed(title='Canceled the game', description=f'Dont worry! You will get it next time.\n The correct number was {answer}\nYou guessed {counter} times')
                    return await ctx.send(embed=embedcancel)
                if message.content.isdigit():
                    if int(message.content) > answer:
                        message_reply = "That's incorrect! You can keep trying or type `cancel` to end the game\n**Hint:** `guess lower`"
                    elif int(message.content) < answer:
                        message_reply = "That's incorrect! You can keep trying or type `cancel` to end the game\n**Hint:** `guess higher`"
                    if int(message.content) == answer:
                        counter += 1
                        embedwin = discord.Embed(title='Correct!', description=f'You guessed the correct number!\nThe number was `{answer}`\nYou guessed in `{counter}` tries')
                        return await ctx.send(embed=embedwin)
                    else:
                        counter += 1
                        await ctx.send(message_reply)
                
    @commands.command()
    async def roll(self, ctx, integer: int =1000):
        await ctx.reply(str(random.randint(1, int(integer))), mention_author=False)

    @commands.command(aliases=['8ball'])
    async def ball(self, ctx, *, question: str):
        responses =['As I see it, yes.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    'Don\'t count on it.',
                    'It is certain.',
                    'It is decidedly so.',
                    'Most likely.',
                    'My reply is no.',
                    'My sources say no.',
                    'Outlook not so good.',
                    'Outlook good.',
                    'Reply hazy, try again.',
                    'Signs point to yes.',
                    'Very doubtful.',
                    'Without a doubt.',
                    'Yes.',
                    'Yes - definitely.',
                    'You may rely on it.']
        responce = random.choice(responses)
        await ctx.send("<a:8ball:911281003702665297> Shaking the 8ball", delete_after=2)
        await asyncio.sleep(2)
        embed = discord.Embed(title="Magic 8ball", description=f"\U0001f3b1 Your Question: {question}\n\U0001f3b1 8ball's Answer: {responce}")
        await ctx.send(embed=embed)


    @commands.command(aliases=['sp'])
    @commands.cooldown(5, 60.0, type=commands.BucketType.user)
    async def spotify(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        async with ctx.typing():
            spotify = functions.Spotify(bot=self.bot, member=member)
            embed = await spotify.get_embed()
            if not embed:
                if member == ctx.author:
                    return await ctx.send(f"You are currently not listening to spotify!", mention_author=False)
                return await ctx.reply(f"{member.mention} is not listening to Spotify", mention_author=False, allowed_mentions=discord.AllowedMentions(users=False))
            await ctx.send(embed=embed[0], file=embed[1])

    @commands.command()
    async def poll(self, ctx, *, question: str):
        embed=discord.Embed(title=f"{question}", description="React to this message with ✅ for yes, ❌ for no.",  color=0xd10a07)
        message = await ctx.channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")

    @commands.max_concurrency(1, commands.BucketType.user, wait=False)
    @commands.command(aliases=['ttt', 'tic'])
    async def tictactoe(self, ctx: commands.context):
        """Starts a tic-tac-toe game."""
        embed = discord.Embed(description=f'🔎 | {ctx.author.mention}'
                                        f'\n👀 |  A member is looking for someone to play **Tic-Tac-Toe**')
        embed.set_thumbnail(url='https://i.imgur.com/DZhQwnD.gif')
        embed.set_author(name='Tic-Tac-Toe', icon_url='https://i.imgur.com/RTwo0om.png')
        player1 = ctx.author
        view = buttons.LookingToPlay(timeout=120)
        view.ctx = ctx
        view.message = await ctx.send(embed=embed,
                                    view=view)
        await view.wait()
        player2 = view.value
        if player2:
            starter = random.choice([player1, player2])
            ttt = buttons.TicTacToe(ctx, player1, player2, starter=starter)
            ttt.message = await view.message.edit(view=ttt, embed=discord.Embed(title='Tic Tac Toe',description=f'{starter.mention} goes first',color=embed.color))

    @commands.command(aliases=['penis'])
    async def pp(self, ctx, member: discord.Member):
        await ctx.send(":eggplant: Looking in your pants ...", delete_after=2)
        await asyncio.sleep(2)
        sizes = "="*random.randint(1,12)
        pp = random.choice(sizes)
        embed = discord.Embed(title="Penis size", description=f"{member.mention}\'s penis size is:\n8{pp}D")
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
      await ctx.send('My uptime is: `147 days, 23 hours, and 12 minutes`')

    @commands.max_concurrency(1, commands.BucketType.user, wait=True)
    @commands.command()
    async def meme(self, ctx: commands.Context) -> discord.Message:
        """
        Sends a random meme from r/memes
        """
        async with ctx.typing():
            return await ctx.send(embed=await self.reddit(random.choice(['memes', 'dankmemes'])))