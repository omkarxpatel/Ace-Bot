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
        self.new_mapping = [cog for cog in self.mapping.keys() if cog and not cog.__class__.__cog_settings__.get('hidden') and not cog.qualified_name == "Jishaku"]
        self.important: str = kwargs.get('important')
        self.list: list = kwargs.get('lists')
        self._value = 0
        

        options = [
            discord.SelectOption(label='Home Page', value='default'),                                    
        ]
        self.context.bot.loop.create_task(self.get_embeds())
        for cog in self.mapping:
            if cog is None or cog.__class__.__cog_settings__.get('hidden') or cog.qualified_name == 'Jishaku':
                continue
            name = ' '.join(cog.qualified_name.split()[1:]) + ' Help'
            emoji = cog.__class__.__cog_settings__.get('emoji')
            option = discord.SelectOption(label=name, value=cog.qualified_name, emoji=emoji, description=cog.__doc__)
            options.append(option)
        super().__init__(placeholder='Select a Category', min_values=1, max_values=1, options=options)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    async def get_embeds(self):
        self.list_of_embeds = []
        self.constant = EmbedPlacer(important=self.important, mapping=self.mapping, ctx=self.context).generate_help_embed
        self.list_of_embeds.append(self.constant)
        for cog in self.mapping:
            if cog is None or cog.__class__.__cog_settings__.get('hidden') or cog.qualified_name == "Jishaku" or cog == 'None':
                continue
            embed = EmbedPlacer(cog=cog, ctx=self.context, important=self.important)
            if not embed:
                continue
            else:
                self.list_of_embeds.append(embed.generate_cog_help)
        return self.list_of_embeds
        
    @property
    def get_list(self):
        return self.list_of_embeds
        

    async def callback(self, interaction: discord.Interaction):
        values = self.values[0]
        if values == 'default':
            self._value = 0
            placer = EmbedPlacer(important=self.important, ctx=self.context, mapping=self.mapping)
            embed = placer.generate_help_embed
            await interaction.message.edit(embed=embed)
        else:
            cog = self.context.bot.get_cog(values)
            self._value = tuple(self.new_mapping).index(cog) + 1
            placer = EmbedPlacer(cog=cog, ctx=self.context, important=self.important)
            embed = placer.generate_cog_help
            await interaction.message.edit(embed=embed)


class DropdownView(discord.ui.View):
    def __init__(self, **kwargs):
        super().__init__()
        self.context: commands.Context = kwargs.get('ctx')
        self.mapping: Dict[commands.Cog, List[commands.Command]] = kwargs.get('mapping')
        self.important: str = kwargs.get('important')
        self.dropdown_class = Dropdown(ctx=self.context, mapping=self.mapping, important=self.important)
        self.add_item(self.dropdown_class)
        
    @discord.ui.button(style=discord.ButtonStyle.blurple, label="First",row=0,emoji="⏪")
    async def first(self, button: discord.ui.Button, interaction: discord.Interaction):
        embeds = self.dropdown_class.get_list
        if self.dropdown_class.value == 0:
            return
        self.dropdown_class.value = 0
        await interaction.message.edit(embed=embeds[self.dropdown_class.value])

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Previous", row=0, emoji="◀️")
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        embeds = self.dropdown_class.get_list
        if self.dropdown_class.value == 0:
            return
        self.dropdown_class.value -= 1
        await interaction.message.edit(embed=embeds[self.dropdown_class.value])
        


    @discord.ui.button(style=discord.ButtonStyle.red, label="Close Embed", emoji="🗑",  row=0)
    async def stop(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            await interaction.message.delete()
        except:
            raise

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Next", row=0, emoji="▶️")
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        embeds = self.dropdown_class.get_list
        if self.dropdown_class.value == len(embeds):
            return
        self.dropdown_class.value += 1
        await interaction.message.edit(embed=embeds[self.dropdown_class.value])

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Last", row=0, emoji="⏩")
    async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
        embeds = self.dropdown_class.get_list
        if self.dropdown_class.value == len(embeds):
            return
        self.dropdown_class.value = len(embeds) - 1
        await interaction.message.edit(embed=embeds[self.dropdown_class.value])

def setup(bot):
    bot.add_cog(HelpCog(bot))


class Help(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)
        self.important = "```fix\n(c) means command | (g) means group \n([]) is required  | (<>) is optional\n```"

    async def send_command_help(self, command: commands.Command):
        embed_placer = EmbedPlacer(ctx=self.context, command=command, important=self.important)
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
