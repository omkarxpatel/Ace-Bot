import discord 
from discord.ext import commands

class ListenEvents(commands.Cog, command_attrs=dict(hidden=True)):
    """🤨 How did you get here """
    def __init__(self, bot):
        self.bot = bot

    async def get_webhook(self, channel):
        hookslist = await channel.webhooks()
        if hookslist:
            for hook in hookslist:
                if hook.token:
                    return hook
                else: continue
        hook = await channel.create_webhook(name="AceBot ModMail")
        return hook

    @commands.Cog.listener('on_message')
    async def modmail(self, message):
        if message.guild: return
        if message.author == self.bot.user: return
        category = self.bot.get_guild(897667014796144661).get_channel(912141371471712276)
        channel = discord.utils.get(category.channels, name=str(message.author.id))
        if not channel:
            embed = discord.Embed(color = discord.Color.blurple(),title='Thanks for reaching out!',description='Your message was sent directly to my developers and they will respond as sonn as they can\n\n\If the message recieves a <:tickYes:885222891883470879> reaction, then the message was sent successfuly\n\If the message recieves a <:tickNo:885222934036226068> reaction, then the message was **NOT** sent')
            await message.author.send(embed=embed)
            channel = await category.create_text_channel(name=str(message.author.id), position=0, reason="ModMail")
        wh = await self.get_webhook(channel)

        files = []
        for attachment in message.attachments:
            if attachment.size > 8388600:
                await message.author.send('The message was sent without attachment, because the attachment size was greater than 8 MB.')
                continue
            files.append(await attachment.to_file(spoiler=attachment.is_spoiler()))

        try:
            embed = discord.Embed(color=discord.Color.green(),timestamp = discord.utils.utcnow())
            embed.add_field(name='Message Received:',value=message.content)
            await wh.send(embed=embed, username=message.author.name, avatar_url=message.author.avatar.url, files=files)
            await message.add_reaction('<a:tick:912173533151514655>')
        except: return await message.add_reaction('<a:tickfalse:912178613258969098>')

    @commands.Cog.listener('on_message')
    async def modmail_reply(self, message):
        if not message.guild: return
        if message.author.bot: return
        if message.channel.category_id != 912141371471712276: return

        user = self.bot.get_user(int(message.channel.name))
        if not user or not user.mutual_guilds:
            return await message.channel.send("Could not find user.")
        files = []
        for attachment in message.attachments:
            if attachment.size > 8388600:
                await message.author.send('Sent message without attachment! File size greater than 8 MB.')
                continue
            files.append(await attachment.to_file(spoiler=attachment.is_spoiler()))
        try:
            embed = discord.Embed(color=discord.Color.green(),timestamp = discord.utils.utcnow())
            embed.add_field(name='Message Received:',value=message.content)
            await user.send(embed=embed, files=files)
        except: return await message.add_reaction('<a:tickfalse:912178613258969098>')

def setup(bot):
    bot.add_cog(ListenEvents(bot))