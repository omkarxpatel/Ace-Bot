import discord
import typing
import random
import requests
import string
from discord.ext import commands
from utils import buttons, functions

# from discord.utils import paginator
# from consts import consts

api_key = "41d5adae37d50b9cb1cdc8f9d6eea94b"
base_url = "http://api.openweathermap.org/data/2.5/weather?"


def setup(bot):
    bot.add_cog(Utility(bot))
    
      
class Utility(commands.Cog, name="<:users:907302669922738187> Utility Help", command_attrs=dict(alias=['utility', 'info']), description="Statistic/misc commands to look stats and more\n`{prefix}help info`\n`{prefix}help utility`"):
    def __init__(self, bot):
        self.bot = bot
        self.random = random.SystemRandom()
        self._alpha_list = list(string.ascii_letters + string.digits)
        self.banned = '{}`><%'
        self.url = "https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png"

    async def get_email(self):
      superb = self.random.choices(self._alpha_list, k=self.random.randint(7,11))
      domains = ['@yahoo.com', '@gmail.com', '@netease.com', '@outlook.com']
      email = "".join(superb) + self.random.choice(domains)
      return email

    async def get_pass(self, n: int = None):
      num = n or self.random.randint(12, 42)
      new = list(string.punctuation) + [x for x in self._alpha_list if x not in self.banned]
      pass_chars = self.random.choices(new, k=num)
      return ''.join(pass_chars)

        
    @commands.command(aliases=['av', 'pfp'])
    async def avatar(self, ctx: commands.Context, member: typing.Union[discord.Member, discord.User] = None):
        """Displays a user's avatar"""
        user = member or ctx.author
        embed = discord.Embed(title='Showing avatar for {}'.format(user.name))
        embed.set_image(url=user.display_avatar.replace(size=1024).url)
        animated = ['png', 'jpg', 'jpeg', 'webp']
        if user.avatar.is_animated():
            animated.append('gif')
            embed.description = " | ".join([f"[{x.upper()}]({user.display_avatar.replace(format=x, size=1024).url})" for x in animated])
        else:
            embed.description = " | ".join([f"[{x.upper()}]({user.display_avatar.replace(format=x, size=1024).url})" for x in animated])
        await ctx.send(embed=embed)


    @commands.command(aliases=['si'])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        thread_channels = len(ctx.guild.threads)
        # stages = len(ctx.guild.stages)
        embed = discord.Embed(title=f"{ctx.guild.name} Info")
        embed.add_field(name=f"General  Info", value = f"<:id:915110710516793384> ID: `{ctx.guild.id}`\n<:owner:907296832642764822> Owner: `{ctx.guild.owner}`\n<:join:915110675800555542> Created: {discord.utils.format_dt(ctx.guild.created_at, 'F')} ({discord.utils.format_dt(ctx.guild.created_at, 'R')})\n<:afadsfs:909537820790620230> Role amount: {len(ctx.guild.roles)}", inline = False)
        total = ctx.guild.member_count
        new_list = [(0 if str(x.status) == 'online' else 1 if str(x.status) == 'idle' else 2 if str(x.status) == 'dnd' else 3) for x in ctx.guild.members]
        online, idle, dnd, offline = [new_list.count(x) for x in range(4)]
        another_list = [(0 if x.bot else 1) for x in ctx.guild.members]
        bots, humans = [another_list.count(x) for x in range(2)]
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
            animated = ['png', 'jpg', 'jpeg', 'webp']
            if ctx.guild.icon.is_animated():
                animated.append('gif')
                icon = " | ".join([f"[{x.upper()}]({ctx.guild.icon.replace(format=x, size=1024).url})" for x in animated])
            else:
                icon = " | ".join([f"[{x.upper()}]({ctx.guild.icon.replace(format=x, size=1024).url})" for x in animated])
            
            embed.add_field(name="<:afadsfs:909537820790620230> Server Icon",
                            value=(f"\n╰ {icon}"),inline=False)
        embed.add_field(name="<:afadsfs:909537820790620230> Channels:", value=f"<:chan:915110447454224415> Channels: {text_channels}\n<:thread:915112100777574420> Threads: {thread_channels}\n<:vsc:915111893725765703> Voice: {voice_channels}\n <:channels:915110435273973770> Categories: {categories}\n <:stage:915112474682990654> Stages: stages", inline = False)
        embed.add_field(name="<:members:907302642542325771> Member Info", value=f"╰ Total Members: {total}\n:bust_in_silhouette: Total Humans: {humans}\n:robot: Total Bots: {bots}\n<:online:907296805040062465> Online: {online}\n<:offline:915110878691598366> Offline: {offline}\n<:idle:915110894596399124> Idle: {idle}\n<:dnd:915110652958363668> DND: {dnd}", inline=False)
        last_boost = max(ctx.guild.members, key=lambda m: m.premium_since or ctx.guild.created_at)
        if last_boost.premium_since is not None:
            boost = f"\n{last_boost}" \
                    f"\n╰ {discord.utils.format_dt(last_boost.premium_since, style='R')}"
        else:
            boost = "\n╰ No active boosters"
        embed.add_field(name="<:booster:907296708269064212> Boosts:", value = f"Level: {ctx.guild.premium_tier}\n╰ Amount: {ctx.guild.premium_subscription_count}\n<:booster:907296708269064212> **Last booster:** {boost}")
        embed.add_field(name=f"<:emojis:915110958832160779> Emojis:", value=f"Static: {len([e for e in ctx.guild.emojis if not e.animated])}/{ctx.guild.emoji_limit}\nAnimated: {len([e for e in ctx.guild.emojis if e.animated])}/{ctx.guild.emoji_limit}", inline=False)
      
        await ctx.send(embed=embed)
    @commands.command(aliases=['whois', 'ui'])
    async def userinfo(self, ctx, member: typing.Optional[discord.Member]):
        member = member or ctx.author
        fetched_user = await self.bot.fetch_user(member.id)
        embed = discord.Embed(title='Showing info for {}'.format(fetched_user.name), color=member.color)   
        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(name="ℹ️ General Information",
                        value=f"\n╰ **ID:** `{member.id}`"
                              f"\n╰ **Username:** `{fetched_user.name}`"
                              f"\n╰ **Discriminator:** `#{fetched_user.discriminator}`"
                              f"\n╰ **Nickname:** {member.nick}"
                              f"\n╰ **Mention:** {member.mention}")

        embed.add_field(name="<:members:907302642542325771> User Info",
                        value=f"\n╰ **Created:** {discord.utils.format_dt(member.created_at, style='f')} ({discord.utils.format_dt(member.created_at, style='R')})"
                        ,inline=False)
        joined = sorted(ctx.guild.members, key=lambda mem: mem.joined_at)
        pos = joined.index(member)
        more = joined[pos-5 if pos >= 5 else 0:pos+5]
        join_pos = '\n'.join([(f"{pos+1}. > {x} ({x.joined_at.strftime('%m/%d/%Y')})" if x == member else f"{joined.index(x)+1}.   {x} ({x.joined_at.strftime('%m/%d/%Y')})") for x in more])
        if member.premium_since:
            embed.add_field(name="<:booster:907296708269064212> Boosting since:",
                            value=f"╰ **Date:** {discord.utils.format_dt(member.premium_since, style='f')} ({discord.utils.format_dt(member.premium_since, style='R')})"
                            ,inline=False)
        animated = ['png', 'jpg', 'jpeg', 'webp']
        if fetched_user.display_avatar.is_animated():
            animated.append('gif')
            avatar = " | ".join([f"[{x.upper()}]({fetched_user.display_avatar.replace(format=x, size=1024).url})" for x in animated])
        
        else:
            avatar = " | ".join([f"[{x.upper()}]({fetched_user.display_avatar.replace(format=x, size=1024).url})" for x in animated])

        animated = ['png', 'jpg', 'jpeg', 'webp']
        if fetched_user.banner:
            if fetched_user.banner.is_animated():
                banner = " | ".join([f"[{x.upper()}]({fetched_user.banner.replace(format=x, size=1024).url})" for x in animated])
            else:
                banner = " | ".join([f"[{x.upper()}]({fetched_user.banner.replace(format=x, size=1024).url})" for x in animated])
        if member.avatar:
            embed.add_field(name="<:afadsfs:909537820790620230> Avatar",
                            value=(
                                f"\n╰ {avatar}"
                            ),inline=False)

        if fetched_user.banner:
            embed.add_field(name="<:afadsfs:909537820790620230> Banner",
                            value=(
                                f"\n╰ {banner}"
                            ),inline=True) 
        embed.add_field(name="<:join:915110675800555542> Join Info",
                value=(
                    f"\n╰ **Joined:** {discord.utils.format_dt(member.joined_at, style='f')} ({discord.utils.format_dt(member.joined_at, style='R')})"
                    f"\n╰ **Join Position:**"
                    f"\n```python"
                    f"\n{join_pos}"
                    f"\n```"
                ),inline=False)  
        roles = [r.mention for r in member.roles if r != ctx.guild.default_role]
        if roles:
            if len(roles) < 10 and len(roles) > 1:
                embed.add_field(name="<:role:915122941165981747> Top Role",
                                value=member.top_role.mention, inline=False)
                
                embed.add_field(name="<:role:915122941165981747> Roles",
                                value=" ".join(roles[::-1]), inline=False)
            else:
                embed.add_field(name="<:role:915122941165981747> Top Role",
                                value=member.top_role.mention, inline=False)  
        await ctx.send(embed=embed)


    @commands.command(aliases=['e', 'emojis'])
    @commands.has_permissions(manage_emojis_and_stickers=True)
    @commands.bot_has_permissions(manage_emojis_and_stickers=True)
    async def em(self, ctx):
        listt = [f"{emoji} -- `<{'a' if emoji.animated else ''}:{emoji.name}:{emoji.id}>`" for emoji in ctx.guild.emojis]
        lista = [listt[x:x+10] for x in range(0, len(listt), 10)]
        for listb in lista:
          msg = "\n".join(listb)
          embed=discord.Embed(description=f"{msg}")
          await ctx.send(embed=embed)

    @commands.command(aliases=['source'])
    async def invite(self, ctx):
        view=discord.ui.View()
        style=discord.ButtonStyle.gray
        item=discord.ui.Button(style=style,label=f"Invite Me",url=f"https://discord.com/api/oauth2/authorize?client_id=912142196231245844&permissions=8&scope=bot")
        support=discord.ui.Button(style=style,label=f"Support Server",url=f"https://discord.gg/7pETYGfQ")
        embed = discord.Embed(title="**Useful Links**", description="[Invite Me](https://discord.com/api/oauth2/authorize?client_id=912142196231245844&permissions=8&scope=bot \"Hovertext\") | [Support Server](https://discord.gg/7pETYGfQ \"Hovertext\") | [Source Code](https://www.youtube.com/watch?v=dQw4w9WgXcQ \"Hovertext\")")
        source=discord.ui.Button(style=style,label=f"Source Code",url=f"https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        view.add_item(item=item)
        view.add_item(item=support)
        view.add_item(item=source)
        await ctx.send(embed=embed,view=view)

    @commands.command()
    async def google(self, ctx: commands.Context, *, query: str):
        embed = discord.Embed(description=f"<:google:913559123730255963> Google Result for `{query}`")
        await ctx.reply(embed = embed, view=buttons.Google(query))

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        embedp = discord.Embed(
          color = 0xaf1aff
        )
        embedp.add_field(name="**Current ping of bot**", value=f"> :ping_pong: {round(self.bot.latency * 1000)}ms")
        await ctx.send(embed=embedp)

    @commands.command(aliases=['owner', 'botinfo'])
    async def info(self, ctx): 
        embed = discord.Embed(title=f"{self.bot.user.name}\'s Info!", color = discord.Color.green())
        embed.add_field(name="<:developerdarkblue:915125525889036299> **Developer:**", value=f"[Squirrels#2499](https://www.youtube.com/watch?v=dQw4w9WgXcQ \"Hovertext\")", inline=True)
        embed.add_field(name="<:server:907301216743207002> **Guilds:**", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="<:members:907302642542325771>** Members:**", value=f"{len(self.bot.users):,}", inline = True)
        embed.add_field (name="<:commands:907319588033802240> **Commands:**", value = len(self.bot.commands), inline = True)
        embed.add_field(name=f"\U0001f3d3 **  Ping:**", value= f"{round(self.bot.latency * 1000)} ms", inline=True)
        embed.add_field(name="<:online:907296805040062465> **Uptime:**", value=f".", inline=True)
        embed.add_field(name="<:python:907294675147321434>** Python Version:**", value=f"[3.10.0](https://www.python.org/downloads/release/python-3100/ \"Hovertext\")", inline = True)
        embed.add_field(name=f"<:dpyversion:907296882966036530> **DPY Version:**", value = "[2.0](https://github.com/Rapptz/discord.py/projects/3 \"Hovertext\")", inline=True)
        embed.add_field(name="<:invite:907296700127911976> **Invite me:**", value="[Click Here](https://discord.com/api/oauth2/authorize?client_id=912142196231245844&permissions=8&scope=bot \"Hovertext\")", inline=True)
        embed.set_footer(text=f'Requested by {ctx.message.author} | ID-{ctx.message.author.id}')
        view=discord.ui.View()
        style=discord.ButtonStyle.gray
        item=discord.ui.Button(style=style,label=f"Invite Me",url=f"https://discord.com/api/oauth2/authorize?client_id=912142196231245844&permissions=8&scope=bot")
        support=discord.ui.Button(style=style,label=f"Support Server",url=f"https://discord.gg/K5NDA6CY")
        source=discord.ui.Button(style=style,label=f"Source Code",url=f"https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        view.add_item(item=item)
        view.add_item(item=support)
        view.add_item(item=source)
        await ctx.send(embed=embed,view=view)


    @commands.command(aliases=['gmail'])
    async def email(self, ctx):
      email = self.random.choice([await self.get_email() for x in range(10)])
      await ctx.send(f'Your generated email is: `{email}`')

    @commands.command(aliases=['pass'])
    async def password(self, ctx):
      email = self.random.choice([await self.get_pass() for x in range(10)])
      await ctx.send(f'Your generated password is: `{email}`')


    @commands.command(help="Shows the weather in a city.", aliases=['temp', 'temperature'])
    async def weather(self, ctx, *, city: str):
            city_name = city
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            channel = ctx.message.channel

            if x["cod"] != "404":

                    y = x["main"]
                    current_temperature = y["temp"]
                    current_temperature_celsiuis = str(round(current_temperature - 273.15))
                    current_pressure = y["pressure"]
                    current_humidity = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    embed = discord.Embed(
                        title=f"**:white_sun_cloud:Current Weather in {city_name}**", description=f"**Description:** {weather_description} \n**Temperature(C):** {current_temperature_celsiuis} \n**Humidity(%):** {current_humidity} \n**Atmospheric Pressure(hPa):** {current_pressure}",
                        color=0x7289DA,
                        timestamp=ctx.message.created_at,)
                    embed.set_thumbnail(url='https://i.ibb.co/CMrsxdX/weather.png')
                    embed.set_footer(text=f"Requested by {ctx.author.name}")
                    await channel.send(embed=embed)

            else:
                    await channel.send(
                        f"There was no results about this place!")
    @commands.command()
    async def afk(self, ctx, duration=None, *, reason="No reason provided"):
        user = ctx.author 
        if not duration:
          await ctx.send("Please enter an afk time")
          return
        embed = discord.Embed(title=f":zzz: Member AFK", description=f"{ctx.author.mention} has gone AFK")
        embed.add_field(name="**AFK note:**", value=f"{reason}", inline = False)
        embed.add_field(name="**Duration:**", value=f"{duration}", inline = False)
        embed.set_author(name=str(user), icon_url=user.avatar.url)
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['addmewhen'])
    async def addthisbotwhen(self, ctx):
      view=discord.ui.View()
      embed = discord.Embed(title='Add me when?', description = f'[Invite Me](https://discord.com/api/oauth2/authorize?client_id=912142196231245844&permissions=8&scope=bot \"Hovertext\") | I wanna get verified :weary:\nCurrent guild count: {str(len(self.bot.guilds))}')
      style=discord.ButtonStyle.gray
      item=discord.ui.Button(style=style,label=f"Invite Me",url=f"https://discord.com/api/oauth2/authorize?client_id=912142196231245844&permissions=8&scope=bot")
      view.add_item(item=item)
      await ctx.send(embed=embed,view=view)

    async def say_permissions(self, ctx, member, channel):
        permissions = channel.permissions_for(member)
        e = discord.Embed(colour=member.colour)
        avatar = member.display_avatar.with_static_format('png')
        e.set_author(name=str(member), url=avatar)
        allowed, denied = [], []
        for name, value in permissions:
            name = name.replace('_', ' ').replace('guild', 'server').title()
            if value:
                allowed.append(name)
            else:
                denied.append(name)

        e.add_field(name='<a:tick:912173533151514655> Allowed', value='\n'.join(allowed))
        e.add_field(name='<a:tickfalse:912178613258969098> Denied ', value='\n'.join(denied))
        await ctx.send(embed=e)

    @commands.command(aliases=['perms'])
    @commands.guild_only()
    async def permissions(self, ctx, member: discord.Member = None, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        if member is None:
            member = ctx.author

        await self.say_permissions(ctx, member, channel)
    @commands.command()
    async def urban(self, ctx, *, search_term):
        '''Searches for a term in Urban Dictionary'''
        try:
            definition_number = int(search_term.split(" ")[-1])-1
        except:
            definition_number = 0
        try:
            term = await self.urban_client.get_term(search_term)
        except LookupError:
            return await ctx.send("Term does not exist!")
        definition = term[definition_number]
        em = discord.Embed(title=definition.word, description=definition.definition, color=0x181818)
        em.add_field(name="Example", value=definition.example)
        em.add_field(name="Popularity", value=f"{definition.upvotes} 👍 {definition.downvotes} 👎")
        em.add_field(name="Author", value=definition.author)
        em.add_field(name="Permalink", value=f"[Click here!]({definition.permalink})")
        await ctx.send(embed=em)
    
    @commands.command(aliases=['calculator', 'calc'])
    async def calculate(self, ctx):
        view = buttons.InteractiveView()
        await ctx.send(f"{ctx.author.mention}\'s Calculator \n```\n```",view=view)

    @commands.command()
    async def covid(self, ctx, *, countryName = None):
        try:
            if countryName is None:
                embed=discord.Embed(title="This command is used like this: ```-covid [country]```", 
                                    colour=0xff0000, 
                                    timestamp=ctx.message.created_at)
                await ctx.send(embed=embed)
            else:
                url = f"https://coronavirus-19-api.herokuapp.com/countries/{countryName}"
                stats = await self.bot.session.get(url)
                to_get = ["cases", "todayCases", "deaths", "todayDeaths", 
                          "recovered", "active", "critical", "totalTests", "casesPerOneMillion", 
                          "deathsPerOneMillion", "testsPerOneMillion"]
                to_fill = ["**Total Cases**", "**Cases Today**", "**Total Deaths**", "**Deaths Today**",
                           "**Recovered**", "**Active**", "**Critical**", "**Total Tests**", "**Cases Per One Million**",
                           "**Deaths Per One Million**", "**Tests Per One Million**"]
                json_stats = await stats.json()
                country = json_stats["country"]
                info_list = [json_stats[x] for x in to_get]
                embed = discord.Embed(title=f"**COVID-19 Status Of {country}**!", 
                                      description="This Information Isn't Live Always, Hence It May Not Be Accurate!",
                                      colour=0x0000ff, 
                                      timestamp=ctx.message.created_at)
                for field in to_fill:
                    embed.add_field(name=field, value = info_list[to_fill.index(field)], inline = True)
                
                embed.set_thumbnail(url=self.url)
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            embed = discord.Embed(title="Invalid Country Name Or API Error! Try Again..!", colour=0xff0000, timestamp=ctx.message.created_at)
            embed.set_author(name="Error!")
            await ctx.send(embed=embed)

    @commands.command()
    async def graph(self, ctx: commands.Context, *points):
        points = [x for x in points if x.isdigit()]
        if len(points) > 250:
                return await ctx.reply('You can\'t input more than 250 points')
        elif len(points) < 4:
                return await ctx.reply('You are supposed to mention at least 4 points to plot a graph!', mention_author=False)
        filen = await functions.get_graph(self.bot, *points)
        await ctx.send(file=filen)