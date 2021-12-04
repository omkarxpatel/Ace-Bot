import discord
from discord.ext import commands
from typing import Dict, List




class EmbedPlacer:
    def __init__(self, **kwargs):
        self.context: commands.Context = kwargs.get('ctx')
        self.cog: commands.Cog = kwargs.get('cog')
        self.command: commands.Command = kwargs.get('command')
        self.mapping: Dict[commands.Cog, List[commands.Command]] = kwargs.get('mapping')
        self.important: str = kwargs.get('important')

    @property
    def generate_help_embed(self):
        collection = self.mapping.items()
        embed = discord.Embed(title=f"{self.context.bot.user.name}'s Commands!",description=f"Need Help? Join the [support server](https://discord.gg/K5NDA6CY). \nType `{self.context.prefix}help [command]` to get more info on a command.")
        for cog, commands in collection:
            if not cog or cog.qualified_name.lower() == "jishaku":
              continue  
            try:
              attr = cog.__class__.__cog_settings__.get('hidden')
            except AttributeError:
              raise
            if attr:
              continue
            else:
              description = cog.description.replace("{prefix}", self.context.prefix) if cog.description else "No description has been set yet!"
              embed.add_field(name=f'{cog.qualified_name}', value=f'{description}')
        embed.set_footer(text=f"Requested by {self.context.author} | {self.context.author.id}")
        return embed

    @property
    def generate_cog_help(self):
        string = ""
        embed = discord.Embed(title=f"{self.context.bot.user.name}'s Help!", description=f"Need help? Join the [support server](https://discord.gg/K5NDA6CY).\n{self.important}\n**Category**: {self.cog.qualified_name}\nType `{self.context.prefix}help [command]` to get more info on a command.\nType `{self.context.prefix}help [group]` to get more info on a group.\n")
        attr = self.cog.__class__.__cog_settings__.get('hidden')   
        if attr:
              return
        for command in self.cog.walk_commands():
          if isinstance(command, commands.Group):
              some_string = f"(g) {self.context.prefix}{command.name} "
              parameters = command.clean_params
              for name, parameter in parameters.items():
                    if parameter.default is parameter.empty:
                        some_string += f"[{name}] "
                    else:
                        some_string += f"<{name}> "
              string += some_string + "\n"
          elif isinstance(command, commands.Command):
              some_string = f"(c) {self.context.prefix}{command.qualified_name} "
              parameters = command.clean_params
              for name, parameter in parameters.items():
                    if parameter.default is parameter.empty:
                        some_string += f"[{name}] "
                    else:
                        some_string += f"<{name}> "
              string += some_string + "\n"
        new_split = [x.split() for x in string.split('\n')]
        new_order = sorted(new_split, key=len)
        new = map(' '.join, new_order)
        string = '\n'.join(new)
        embed.description += f"```css\n{string}\n```"
        return embed

    @property
    def generate_command_help(self):
        embed = discord.Embed(description=self.important,title=f"{self.context.bot.user.name}'s Help")
        help = self.command.help if self.command.help else "Command is not officially documented yet."
        embed.add_field(name="**Documentation:**", value=f"{help}", inline=True)
        aliases = ', '.join([f"`{x}`" for x in self.command.aliases]) if self.command.aliases else "`None`"
        parameters = self.command.clean_params
        some_string = ""
        if parameters:
          for name, parameter in parameters.items():
              if parameter.default is parameter.empty:
                  some_string += f"[`{name}`], "
              else:
                  some_string += f"<`{name} | default = {str(parameter.default).replace('`None`', 'author')}`>, "
          some_string = some_string[:-2]
        else:
          some_string = "`None`"
        alias = aliases if aliases == "`None`" else f"[{aliases}]"
        embed.add_field(name="Aliases", value=alias, inline=True)
        embed.add_field(name="Parameters", value=some_string, inline=False)
        return embed

class Dropdown(discord.ui.Select):
    def __init__(self, **kwargs):
        self.context: commands.Context = kwargs.get('ctx')
        self.mapping: Dict[commands.Cog, List[commands.Command]] = kwargs.get('mapping')
        self.important: str = kwargs.get('important')

        options = [
            discord.SelectOption(label='Home Page', value='default'),
            discord.SelectOption(label='Developer Help', description='Commands that only devs of the bot can use', emoji='<:developerdarkblue:915125525889036299>', value='<:developerdarkblue:915125525889036299> Developer Help'),
            discord.SelectOption(label='Config Help', description='Configuration Commands to personalize the bot', emoji='<:utility:908438154841849927>', value='<:utility:908438154841849927> Config Help'),
            discord.SelectOption(label='Economy Help', description='Economy commands based on real life', emoji='<:spades:915657207968833607>', value='<:spades:915657207968833607> Economy'),
            discord.SelectOption(label='Fun Help', description='Fun commands to use around the server', emoji='<:controller:915124129257111582>', value='<:controller:915124129257111582> Fun Help'),
            discord.SelectOption(label='Moderation Help', description='Moderation commands to moderate your server', emoji='<:moderation:907802138296606740>', value='<:moderation:907802138296606740> Moderation Help'),
            discord.SelectOption(label='Utility Help', description='Utility/misc commands to look at stats and more', emoji='<:users:907302669922738187>', value='<:users:907302669922738187> Utility Help')                                    
        ]
        super().__init__(placeholder='Select a Category', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        values = self.values[0]
        if values == 'default':
            placer = EmbedPlacer(important=self.important, ctx=self.context, mapping=self.mapping)
            embed = placer.generate_help_embed
            await interaction.message.edit(embed=embed)
        else:
            cog = self.context.bot.get_cog(values)
            placer = EmbedPlacer(cog=cog, ctx=self.context, important=self.important)
            embed = placer.generate_cog_help
            await interaction.message.edit(embed=embed)


class DropdownView(discord.ui.View):
    def __init__(self, **kwargs):
        super().__init__()
        self.context: commands.Context = kwargs.get('ctx')
        self.mapping: Dict[commands.Cog, List[commands.Command]] = kwargs.get('mapping')
        self.important: str = kwargs.get('important')
        self.add_item(Dropdown(ctx=self.context, mapping=self.mapping, important=self.important))


def setup(bot):
    bot.add_cog(HelpCog(bot))


class Help(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)
        self.important = "```fix\n(c) means command | (g) means group \n([]) is required  | (<>) is optional\n```"
      

    async def send_command_help(self, command: commands.Command):
        embed_placer = EmbedPlacer(ctx=self.context, command=command)
        embed = embed_placer.generate_command_help
        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_error_message(self, error):
          argument = error.split()[-2].replace('"', '')
          index = -1
          foul_list = [cog.__class__.__cog_settings__.get('alias') for cog in self.context.bot.cogs.values() if not cog.__class__.__cog_settings__.get('hidden')]
          for mylist in foul_list:
              
              if mylist and argument in mylist:
                index = foul_list.index(mylist)
                break
          if index == -1:
              return await self.context.send(error)
          else:
              og_list = [cog for cog in self.context.bot.cogs.values() if not cog.__class__.__cog_settings__.get('hidden')]
              cog: commands.Cog = og_list[index]
              await self.context.send_help(cog)
              
    async def send_bot_help(self, mapping: Dict[commands.Cog, List[commands.Command]]):
        embed_placer = EmbedPlacer(ctx=self.context, mapping = mapping)
        embed = embed_placer.generate_help_embed
        destination = self.get_destination()
        view = DropdownView(ctx=self.context, important=self.important, mapping=mapping)
        await destination.send(embed=embed, view=view)

    async def send_cog_help(self, cog: commands.Cog):
        destination = self.get_destination()
        embed_placer = EmbedPlacer(cog=cog, important=self.important, ctx=self.context)
        embed = embed_placer.generate_cog_help
        await destination.send(embed=embed)
      

class HelpCog(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.bot.help_command = Help()
