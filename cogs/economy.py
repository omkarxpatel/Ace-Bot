import discord
import random
import asyncio
import datetime
from typing import Optional
from datetime import datetime as dt
from discord.ext import commands
from utils.errors import OnCooldown

shop_entity = {
                'fishing pole': {'alias': ['fishpole', 'fishing', 'pole'], 
                                 'price': 25000
                                 },
                'hunting rifle': {'alias': ['rifle', 'hunting', 'gun'], 
                                  'price': 35000
                                  },
                'shovel': {'alias': ['dig'], 
                           'price': 15000
                           }
              }

def on_cooldown():
      async def predicate(ctx: commands.Context):
          request = await ctx.bot.db.cooldown.find_one({'_id': ctx.author.id})
          if not request:
            return True
          date = request.get(ctx.command.name)
          if not date:
              return True
          if dt.utcnow() > date:
              return True
          else:
              raise OnCooldown(dateobject=date)
      return commands.check(predicate)
# spades = '<:spades:914756982651633665>'
spades = '<:currency:915664733644947536>'

def setup(bot):
    bot.add_cog(economy(bot))


class economy(commands.Cog, name="<:spades:915657207968833607> Economy", command_attrs=dict(alias=['economy', 'econ']), description="Economy commands related to real-life situations\n `ace.help economy`\n`ace.help econ`"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup(self, ctx):
        request = await self.bot.db.economy.find_one({"_id": ctx.author.id})
        print(request)
        if request:
          return await ctx.reply("Seems like you are already registered!", mention_author=False)
        document = {"_id": ctx.author.id, "balance": 5000}
        cooldown_document = {"_id": ctx.author.id, "daily": dt.utcnow(), "weekly": dt.utcnow(), "monthly": dt.utcnow()}
        await self.bot.db.economy.insert_one(document)
        await self.bot.db.cooldown.insert_one(cooldown_document)
        embed = discord.Embed(title=f"Welcome {ctx.author.name}", description=f'You have been successfully registered into the economy database.\nType `ace.help economy` for commands!\n \nAs a starter perk, you have been given `5000` {spades}')
        await ctx.send(embed=embed)

    @commands.command()
    @on_cooldown()
    async def beg(self, ctx):
        request = await self.bot.db.economy.find_one({"_id": ctx.author.id})
        if not request:
          return await ctx.reply("Seems like you are not registered! Do so by using `ace.setup`", mention_author=False)
        cooldown = dt.utcnow() + datetime.timedelta(seconds=60)
        cooldown_data = {"beg": cooldown}
        coins = random.randint(100,400)
        total = request['balance'] + coins
        data = {"balance": total}
        embed = discord.Embed(description=f'You begged and made `{coins}` {spades}\nYour current balance is: `{total}` {spades}', timestamp=discord.utils.utcnow()) 
        embed.set_footer(text='Requested by {}' .format(ctx.message.author))
        await self.bot.db.economy.update_one({"_id": ctx.author.id}, {"$set": data})
        await self.bot.db.cooldown.update_one({"_id": ctx.author.id}, {"$set": cooldown_data})
        await ctx.send(embed=embed)

    @commands.command()
    @on_cooldown()
    async def hourly(self, ctx):
        request = await self.bot.db.economy.find_one({"_id": ctx.author.id})
        if not request:
          await ctx.reply("Seems like you are not registered! Do so by using `ace.setup`", mention_author=False)
        cooldown = dt.utcnow() + datetime.timedelta(hours=1)
        total = request['balance'] + 1500
        data = {"balance": total}
        cooldown_data = {"daily": cooldown}
        embed = discord.Embed(title=f'Here are your hourly coins, {ctx.author.name}', description=f'`1,500` {spades} have been placed in your wallet.\nYour current balance is `{total}` {spades}', timestamp=discord.utils.utcnow())
        embed.set_footer(text='Requested by {}' .format(ctx.message.author))
        await self.bot.db.economy.update_one({"_id": ctx.author.id}, {"$set": data})
        await self.bot.db.cooldown.update_one({"_id": ctx.author.id}, {"$set": cooldown_data})
        await ctx.send(embed=embed)


#86400 seconds cooldown
    @commands.command()
    @on_cooldown()
    async def daily(self, ctx):
        request = await self.bot.db.economy.find_one({"_id": ctx.author.id})
        if not request:
          await ctx.reply("Seems like you are not registered! Do so by using `ace.setup`", mention_author=False)
        cooldown = dt.utcnow() + datetime.timedelta(days=1)
        total = request['balance'] + 7500
        data = {"balance": total}
        cooldown_data = {"daily": cooldown}
        embed = discord.Embed(title=f'Here are your daily coins, {ctx.author.name}', description=f'`7,500` {spades} have been placed in your wallet.\nYour current balance is `{total}` {spades}', timestamp=discord.utils.utcnow())
        embed.set_footer(text='Requested by {}' .format(ctx.message.author))
        await self.bot.db.economy.update_one({"_id": ctx.author.id}, {"$set": data})
        await self.bot.db.cooldown.update_one({"_id": ctx.author.id}, {"$set": cooldown_data})
        await ctx.send(embed=embed)

#604800 seconds cooldown
    @commands.command()
    @on_cooldown()
    async def weekly(self, ctx):
        request = await self.bot.db.economy.find_one({"_id": ctx.author.id})
        if not request:
          await ctx.reply("Seems like you are not registered! Do so by using `ace.setup`", mention_author=False)
        cooldown = dt.utcnow() + datetime.timedelta(days=7)
        total = request['balance'] + 35000
        data = {"balance": total}
        cooldown_data = {"weekly": cooldown}
        embed = discord.Embed(title=f'Here are your weekly coins, {ctx.author.name}', description=f'`35,000` {spades} have been placed in your wallet.\nYour current balance is `{total}` {spades}', timestamp=discord.utils.utcnow())
        embed.set_footer(text='Requested by {}' .format(ctx.message.author))
        await self.bot.db.economy.update_one({"_id": ctx.author.id}, {"$set": data})
        await self.bot.db.cooldown.update_one({"_id": ctx.author.id}, {"$set": cooldown_data})
        await ctx.send(embed=embed)

#2629746 seconds cooldown
    @commands.command()
    @on_cooldown()
    async def monthly(self, ctx):
        request = await self.bot.db.economy.find_one({"_id": ctx.author.id})
        if not request:
          await ctx.reply("Seems like you are not registered! Do so by using `ace.setup`", mention_author=False)
        cooldown = dt.utcnow() + datetime.timedelta(days=30)
        total = request['balance'] + 100000
        data = {"balance": total}
        cooldown_data = {"monthly": cooldown}
        embed = discord.Embed(title=f'Here are your monthly coins, {ctx.author.name}', description=f'`100,000` {spades} have been placed in your wallet.\nYour current balance is `{total}` {spades}', timestamp=discord.utils.utcnow())    
        embed.set_footer(text='Requested by {}' .format(ctx.message.author))
        await self.bot.db.economy.update_one({"_id": ctx.author.id}, {"$set": data})
        await self.bot.db.cooldown.update_one({"_id": ctx.author.id}, {"$set": cooldown_data})
        await ctx.send(embed=embed)

    @commands.command(aliases=['balance'])
    async def bal(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        request = await self.bot.db.economy.find_one({"_id": user.id})
        if not request:
          await ctx.reply("Seems like you are not registered! Do so by using `ace.setup`", mention_author=False)
        balance = request["balance"]
        wallet = request.get('wallet')
        if not wallet:
            wallet = [0, 100000]
            await self.bot.db.economy.update_one({'_id': ctx.author.id}, {'$set': {"wallet": [0, 100000]}})
        bank = f"{wallet[0]:,}/100,000"
        networth = wallet[0] + balance
        embed = discord.Embed(title=f'{user.name}\'s balance', description=f'**Wallet:** `{balance:,}` {spades}\n**Bank:** `{bank}` {spades}\n**Net worth:** `{networth:,}` {spades}', timestamp=discord.utils.utcnow(), color = discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount:int):
        request = await self.bot.db.economy.find_one({"_id": ctx.author.id})
        if not request:
          return await ctx.reply("Seems like you are not registered! Do so by using `ace.setup`", mention_author=False)
        balance = request["balance"]
        wallet = request.get("wallet")
        if not wallet:
          wallet = [0, 100000]
          await self.bot.db.economy.update_one({'_id': ctx.author.id}, {'$set': {"wallet": wallet}})
        if amount > balance:
          return await ctx.send(f"You can not deposit an amount greater than your balance. Your balance is `{balance}` {spades}")
        elif amount < 0:
          return await ctx.send("You can not deposit a negative amount!")
        elif amount == 0:
          return await ctx.send(f"You can not deposit `{amount}` {spades} because you have only 0...")
        elif amount > (wallet[1] - wallet[0]):
          return await ctx.send('You don\'t have enough space in your bank.')
        
        wallet[0] = wallet[0] + amount
        print(wallet)
        data = {"wallet": wallet, "balance": balance-amount}
        await self.bot.db.economy.update_one({'_id': ctx.author.id}, {'$set': data})
        print('done')
        print(await self.bot.db.economy.find_one({"_id": ctx.author.id}))
        embed = discord.Embed(title=f'{ctx.author.name}, `{amount}` {spades} deposited.',description=f'**Current Wallet:** `{data["balance"]:,}` {spades}\n**Current Bank:** `{wallet[0]:,  }/100,000` {spades}', timestamp=discord.utils.utcnow(), color = discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name="withdraw", aliases=['with'])
    async def _with(self, ctx: commands.Context, amount:int):
        request = await self.bot.db.economy.find_one({"_id": ctx.author.id})
        if not request:
          return await ctx.reply("Seems like you are not registered! Do so by using `ace.setup`", mention_author=False)
        balance = request["balance"]
        wallet = request.get("wallet")
        if not wallet:
          wallet = [0, 100000]
          await self.bot.db.economy.update_one({'_id': ctx.author.id}, {'$set': {"wallet": [0, 100000]}})
        if amount > wallet[0]:
          return await ctx.send(f"You can not withdraw an amount greater than what you have in your bank. Your bank balance is `{wallet[0]}` {spades}")
        elif amount < 0:
          return await ctx.send("You can not withdraw a negative amount!")
        elif amount == 0:
          return await ctx.send(f"You can only withdraw a positive integer")
        elif amount > (wallet[0]):
          return await ctx.send('You don\'t have that much money in bank.')  
        wallet[0] = wallet[0] - amount
        data = {"wallet": wallet, "balance": balance + amount}
        await self.bot.db.economy.update_one({'_id': ctx.author.id}, {'$set': data})
        embed = discord.Embed(description=f'{ctx.author.name}, `{amount}` {spades} have been withdrawn from your bank into your wallet. \n**Current Wallet:** {data["balance"]:,} {spades} \n**Current Bank:** {wallet[0]:,} {spades}', timestamp=discord.utils.utcnow(), color = discord.Color.green())
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['og'])
    @commands.is_owner()
    async def ownergive(self, ctx: commands.Context, amount: int, user: discord.User = None):
        user = user or ctx.author
        requestuser = await self.bot.db.economy.find_one({"_id": user.id})
        if not requestuser:
          await ctx.reply("Seems like they are not registered! Make them do so by using `ace.setup`", mention_author=False)
        total = requestuser['balance'] + amount
        data = {"balance": total}
        embed = discord.Embed(title=f'Here are your coins, {ctx.author.name}', description=f'`{amount}` {spades} have been placed in `{user}\'s` wallet.\nTheir current balance is `{total}` {spades}', timestamp=discord.utils.utcnow(), color = discord.Color.green())
        embed.set_footer(text='Developer: {}' .format(ctx.message.author))
        await self.bot.db.economy.update_one({"_id": user.id}, {"$set": data})
        await ctx.reply(embed=embed)

    @commands.group(invoke_without_command=True)
    async def shop(self, ctx: commands.Context):
        user = ctx.author
        request = await self.bot.db.economy.find_one({"_id": user.id})
        if not request:
            await ctx.reply("Seems like you are not registered! Do so by using `ace.setup`", mention_author=False)
        balance = request["balance"]
        embed = discord.Embed(title=f"Shop items", description=f'Your current wallet: `{balance:,}` {spades}\n')
        embed.set_footer(text="Type ace.bal to see your balance")
        
        string =  [f"`{value['price']:,}`{spades} | {item.title()}" for (item, value) in shop_entity.items()]
        string.sort()
        embed.description += '\n'.join(string)
        await ctx.send(embed=embed)

    @shop.command()
    async def buy(self, ctx: commands.Context, *, name: str = None, amount: Optional[int] = 1):
        if not name:
            return await ctx.reply('You need to name the thing you want to purchase.', mention_author=False)
        new_list = [(x[0], x[1]['alias']) for x in shop_entity.items()]
        another_list = [names[0] for names in new_list if name in names[1]]
        if another_list:
            item = shop_entity[another_list[0]]
            print(item)
        else:
            return await ctx.reply('Not a valid item that\'t available on shop.')
        

    @commands.command(aliases=['share'])
    async def give(self, ctx: commands.Context, amount:int, user: discord.User):
      request = await self.bot.db.economy.find_one({"_id": ctx.author.id})
      if not request:
        await ctx.reply("Seems like you are not registered! Do so by using `ace.setup`", mention_author=False)
      requestuser = await self.bot.db.economy.find_one({"_id": user.id})
      if not requestuser:
        await ctx.reply("Seems like they are not registered! Do so by using `ace.setup`", mention_author=False)
      balance = requestuser['balance']
      if amount > balance:
        return await ctx.send(f"You do not have enough money to send `{amount}` {spades}")
      if balance == 0:
        return await ctx.send(f"You have `0` {spades}, you can not send any coins.")

      newtotal = request['balance'] - amount
      newdata = {"balance": newtotal}
      total = requestuser['balance'] + amount
      data = {"balance": total}

      newtotal = request['balance'] - amount
      newdata = {"balance": newtotal}

      embed = discord.Embed(title=f'Sent {user.name} `{amount}` {spades}', description = f'{ctx.author.name}\'s new balance: `{newtotal}` {spades}\n{user.name}\'s new balance: `{total}` {spades}',timestamp=discord.utils.utcnow(), color = discord.Color.green())
      embed.set_footer(text='User: {}' .format(ctx.message.author))
      await self.bot.db.economy.update_one({"_id": user.id}, {"$set": data})
      await self.bot.db.economy.update_one({"_id": ctx.author.id}, {"$set": newdata})
      await ctx.reply(embed=embed)


    @commands.command(aliases=['cc'])
    @commands.is_owner()
    async def coinsclear(self, ctx: commands.Context, amount, user: discord.User = None):
        user = user or ctx.author
        requestuser = await self.bot.db.economy.find_one({"_id": user.id})
        if not requestuser:
          await ctx.reply("Seems like they are not registered! Do so by using `ace.setup`", mention_author=False)  
        coins = requestuser['balance']
        total = requestuser['balance'] - coins
        data = {"balance": total}
        embed = discord.Embed(title=f'Cleared `{coins}` {spades} from {user.name}', description=f'They now have `{total}` {spades} left in their wallet.', timestamp=discord.utils.utcnow(), color = discord.Color.red())
        embed.set_footer(text='Developer: {}' .format(ctx.message.author))
        await self.bot.db.economy.update_one({"_id": user.id}, {"$set": data})
        await ctx.reply(embed=embed)
    
    @commands.command(aliases=['gamble'])
    async def bet(self, ctx: commands.Context, amount: int):
      request = await self.bot.db.economy.find_one({"_id": ctx.author.id})
      if not request:
          await ctx.reply("Seems like you are not registered! Do so by using `ace.setup`", mention_author=False)
      balance = request["balance"]
      if amount < 0:
        return await ctx.send('You can not bet a negative amount.')
      if amount == 0:
        return await ctx.send(f'You can not bet a `0` {spades}.')
      elif amount > balance:
        return await ctx.send(f"You can not bet an amount greater than your balance. Your balance is `{balance}` {spades}")
      if amount > 750000:
        await ctx.send(f"Sorry, you can not bet an amount greater than `750,000`{spades}")
        return
      die1 = random.randint(1, 12)
      die2 = random.randint(1, 12)
      bet3x = amount*3
      if die1 == die2 or die1 in range(die2-2 if die2 > 2 else 0, die2+2):
        total = request['balance'] + bet3x
        data = {"balance": total}
        embed = discord.Embed(title=f'{ctx.author.name}\'s winning gambling game', description=f'You won {spades} `{bet3x}`\n \n**Precent Won:** `300%`\n**New Balance:** {spades} `{total}`', color = discord.Color.green(), timestamp=discord.utils.utcnow())
        embed.set_footer(text='User: {}' .format(ctx.message.author))
        embed.add_field(name=f'**{ctx.author.name}**', value=f'Rolled `{die1}`')
        embed.add_field(name=f'**Ace Bot**', value=f'Rolled `{die2}`')
        await self.bot.db.economy.update_one({"_id": ctx.author.id}, {"$set": data})
        await ctx.send(embed=embed)
      elif die1 != die2:
        total = request['balance'] - amount
        data = {"balance": total}
        embed = discord.Embed(title=f'{ctx.author.name}\'s losing gambling game', description=f'You lost {spades} `{amount}`\n \n**New Balance:** {spades} `{total}`', timestamp=discord.utils.utcnow(), color = discord.Color.red())
        embed.set_footer(text='User: {}' .format(ctx.message.author))
        embed.add_field(name=f'**{ctx.author.name}**', value=f'Rolled `{die1}`')
        embed.add_field(name=f'**Ace Bot**', value=f'Rolled `{die2}`')
        await self.bot.db.economy.update_one({"_id": ctx.author.id}, {"$set": data})
        await ctx.send(embed=embed)

    @commands.command()
    async def slots(self, ctx: commands.Context, bet: int):
        request = await self.bot.db.economy.find_one({"_id": ctx.author.id})
        counter = 0
        if not request:
            await ctx.reply("Seems like you are not registered! Do so by using `ace.setup`", mention_author=False)
        string_list = ["【 <a:slotsroll:915158443697000469> 】", "【 <a:slotsroll:915158443697000469> 】", "【 <a:slotsroll:915158443697000469> 】"]
        embed = discord.Embed(title="Rolling the slot machine", description='|'.join(string_list))
        message = await ctx.send(embed=embed)
        slot_options = "\N{Watermelon} \N{Gem Stone} 3\N{variation selector-16}\N{combining enclosing keycap} \U0001f352 \U0001f4b5 \U0001fa99".split()
        print(slot_options)
        option_list = random.choices(slot_options, k=3)
        print(option_list)
        for item in option_list:
          await asyncio.sleep(1.5)
          string_list[counter] = f"【 {option_list[counter]} 】"
          embed.description = ' | '.join(string_list)
          await message.edit(embed=embed)
          counter += 1

