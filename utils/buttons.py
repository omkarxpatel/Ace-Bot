import discord
import simpcalc
from typing import List
from discord.ext import commands
from discord import Interaction
from urllib.parse import quote_plus

class Google(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f'https://www.google.com/search?q={query}'
        self.add_item(discord.ui.Button(label='Click Here', url=url))

class YTDropdown(discord.ui.Select):
    def __init__(self, **kwargs):
        self.list: List[str] = kwargs.get('lists')
        options = []
        counter = 0
        for title, uploader, link in self.list:
            if counter == 0:
                default = True
            else:
                default = False
            my_class = discord.SelectOption(label=uploader, description=title, value=f"{counter}", emoji="<:youtube:917124931635003412>", default=default)
            options.append(my_class)
            counter += 1
        super().__init__(placeholder=None,min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        values = self.values[0]
        await interaction.message.edit(self.list[int(values)][2])
        
class YTDropdownView(discord.ui.View):
    def __init__(self, **kwargs):
        super().__init__()
        self.ctx: commands.Context = kwargs.get('context')
        self.bot = kwargs.get('bot') 
        self.list: List[str] = kwargs.get('lists')
        self.add_item(YTDropdown(lists=self.list))

    @discord.ui.button(style=discord.ButtonStyle.green, label="Play", row=1)
    async def play(self, button: discord.ui.Button, interaction: discord.Interaction):
        command = self.bot.get_command('play')
        vc = interaction.user.voice.channel
        await self.ctx.invoke(command, )
        await interaction.response.send_message(f"Joining `#{vc}`")
        
    @discord.ui.button(style=discord.ButtonStyle.red, label="Pause", row=1)
    async def pause(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(f"⏸️Pausing the player")


class InteractiveView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.expr = ""
        self.calc = simpcalc.Calculate()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="1", row=0)
    async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "1"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="2", row=0)
    async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "2"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="3", row=0)
    async def three(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "3"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="+", row=0)
    async def plus(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "+"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="4", row=1)
    async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "4"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="5", row=1)
    async def five(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "5"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="6", row=1)
    async def six(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "6"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="/", row=1)
    async def divide(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "/"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="7", row=2)
    async def seven(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "7"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="8", row=2)
    async def eight(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "8"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="9", row=2)
    async def nine(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "9"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="*", row=2)
    async def multiply(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "*"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label=".", row=3)
    async def dot(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "."
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="0", row=3)
    async def zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "0"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.red, label="<==", row=3)
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr = self.expr[:-1]
        await interaction.message.edit(content=f"```\n{self.expr}\n```")


    @discord.ui.button(style=discord.ButtonStyle.green, label="-", row=3)
    async def minus(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "-"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="(", row=4)
    async def left_bracket(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "("
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label=")", row=4)
    async def right_bracket(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += ")"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.red, label="C", row=4)
    async def clear(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr = ""
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="=", row=4)
    async def equal(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            self.expr = await self.calc.calculate(self.expr)
        except simpcalc.errors.BadArgument:
            return await interaction.response.send_message("Um, looks like you provided a wrong expression....")
        await interaction.message.edit(content=f"```\n{self.expr}\n```")


class TButton(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None

  @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
  async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
      await interaction.response.send_message('Creating a ticket', ephemeral=True)
      self.value = True
      self.stop()
  @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
  async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
      await interaction.response.send_message('Canceling the ticket', ephemeral=True)
      self.value = False
      self.stop()

class Close(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None

  @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
  async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
      await interaction.response.send_message('Closing the ticket in a few seconds..', ephemeral=True)
      self.value = True
      self.stop()
  @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
  async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
      await interaction.response.send_message('Keeping the ticket', ephemeral=True)
      self.value = False
      self.stop()

class LookingForButton(discord.ui.Button):
    sep = '\u2001'

    def __init__(self, disabled: bool = False, label: str = None):
        super().__init__(style=discord.ButtonStyle.blurple, label=(label or f'{self.sep*14}Join 🎮{self.sep*14}'),
                        disabled=disabled, row=0)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: LookingToPlay = self.view
        if interaction.user and interaction.user.id == view.ctx.author.id:
            return await interaction.response.send_message(embed=discord.Embed(title='Error Occured', description='You can\'t play with yourself', color=discord.Color.red()),
                                                            ephemeral=True)
        view.value = interaction.user
        view.stop()

class CancelButton(discord.ui.Button):
    sep = '\u2001'

    def __init__(self, disabled: bool = False, label: str = None):
        super().__init__(style=discord.ButtonStyle.red, label=(label or f'{self.sep*14}Exit ❌{self.sep*14}'),
                        disabled=disabled, row=1)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: LookingToPlay = self.view
        if interaction.user.id == view.ctx.author.id:
            view.value = None
            for item in view.children:
                item.disabled = True
            await view.message.edit(view=view)
            view.stop()
        else:
            await interaction.response.send_message(embed=discord.Embed(title='Error Occured', description='Only the game author can do that action!', color=discord.Color.red()), 
                                                    ephemeral=True)

class GiveUp(discord.ui.Button):
    sep = '\u2001'

    def __init__(self, disabled: bool = False, label: str = None):
        super().__init__(style=discord.ButtonStyle.red, label=(label or f'{self.sep*4}Give up 🏳️{self.sep*4}'),
                        custom_id='giveUp' ,disabled=disabled, row=3)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        for child in view.children:
            child.disabled = True
        if interaction.user.id == view.player1.id:
            winner = view.player2
        elif interaction.user.id == view.player2.id:
            winner = view.player1
        embed = discord.Embed(title=f'{interaction.user} gave up 🏳️',description=f'{winner.mention} has won 🏆',color=discord.Color.greyple())
        await interaction.response.edit_message(embed=embed ,view=view)
        view.stop()
        
class LookingToPlay(discord.ui.View):
    def __init__(self, timeout: int = 120, label: str = None):
        super().__init__(timeout=timeout)
        self.message: discord.Message = None
        self.value: discord.User = None
        self.ctx: commands.Context = None
        self.add_item(LookingForButton(label=label))
        self.add_item(CancelButton())

    async def on_timeout(self) -> None:
        for button in self.children:
            button.disabled = True
        await self.message.edit(embed=discord.Embed(title='Timed out ⏰',description='Timed out - game has ended.'), view=None)


# Defines a custom button that contains the logic of the game.
# The ['TicTacToe'] bit is for type hinting purposes to tell your IDE or linter
# what the type of `self.view` is. It is not required.
class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=discord.ButtonStyle.secondary, label='  ', row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.player1:
            self.style = discord.ButtonStyle.blurple
            self.label = '\U0001f1fd'
            self.disabled = True
            view.board[self.y][self.x] = view.X
        else:
            self.style = discord.ButtonStyle.red
            self.label = '🅾'
            self.disabled = True
            view.board[self.y][self.x] = view.O

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                embed = discord.Embed(title=f'{view.current_player.name} is the winner - \U0001f1fd', description=f'{view.current_player.mention} has won 🏆', color=discord.Color.blue())
            elif winner == view.O:
                embed = discord.Embed(title=f'{view.current_player.name} is the winner - 🅾',  description=f'{view.current_player.mention} has won 🏆', color=discord.Color.red())
            else:
                embed = discord.Embed(title=f' It\'s a tie ☠️', color=discord.Color.red())

            for child in view.children:
                child.disabled = True


        else:
            if view.current_player == view.player1:
                view.current_player = view.player2
                embed = discord.Embed(title="Tic Tac Toe", description=f"{view.current_player.mention}'s turn - 🅾",color=interaction.message.embeds[0].color)
            else:
                view.current_player = view.player1
                embed = discord.Embed(title="Tic Tac Toe", description=f"{view.current_player.mention}'s turn - \U0001f1fd", color=interaction.message.embeds[0].color)

        await interaction.response.edit_message(embed=embed, view=view)


# This is our actual board View
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, ctx: commands.Context, player1: discord.Member, player2: discord.Member, starter: discord.User):
        super().__init__()
        self.current_player = starter
        self.ctx: commands.Context = ctx
        self.player1: discord.Member = player1
        self.player2: discord.Member = player2
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))
        self.add_item(GiveUp())

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user and interaction.data['custom_id'] == 'giveUp':
            return True
        if interaction.user and interaction.user.id == self.current_player.id:
            return True
        elif interaction.user and interaction.user.id in (self.player1.id, self.player2.id):
            await interaction.response.send_message(embed=discord.Embed(title='Not your turn', description='Wait for your turn to make a move', color=discord.Color.red()), ephemeral=True)
        elif interaction.user:
            await interaction.response.send_message(embed=discord.Embed(title='Forbidden ', description='You aren\'t a part of this game!', color=discord.Color.red()), ephemeral=True)
        return False
    
class RequestToPlayView(discord.ui.View):
    def __init__(self, ctx: commands.Context, member: discord.Member, game: str = 'Rock Paper Scissors'):
        super().__init__(timeout=15)
        self.member = member
        self.ctx = ctx
        self.message: discord.Message = None
        self.value: bool = None
        self.game = game

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id in (self.ctx.author.id, self.member.id):
            return True
        await interaction.response.defer()

    @discord.ui.button(label='Confirm', emoji='✅')
    async def confirm(self, _, interaction: Interaction):
        if interaction.user.id == self.member.id:
            await interaction.response.defer()
            self.clear_items()
            self.message.content = None
            self.value = True
            self.stop()
        else:
            await interaction.response.defer()

    @discord.ui.button(label='Deny', emoji='❌')
    async def deny(self, _, interaction: Interaction):
        if interaction.user.id == self.ctx.author.id:
            await interaction.response.edit_message(content=f"{self.ctx.author.mention}, you have cancelled the challenge.", view=None)
        else:
            await interaction.response.edit_message(content=f"{self.ctx.author.mention}, {self.member} has denied your challenge.", view=None)
        self.value = False
        self.stop()

    async def start(self):
        self.message = await self.ctx.send(f"{self.member.mention}, {self.ctx.author} is challenging you to at {self.game}, do you accept?", view=self)

    async def on_timeout(self) -> None:
        self.clear_items()
        await self.message.edit(content=f"{self.ctx.author.mention}, did not respond in time to the challenge!")
        self.stop()


class ObjectSelector(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Rock', description='Rock beats Scissors', emoji='🗿'),
            discord.SelectOption(label='Paper', description='Paper beats Rock', emoji='📄'),
            discord.SelectOption(label='Scissors', description='Scissors beats Paper', emoji='✂')
        ]
        super().__init__(placeholder='Select your object...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: RockPaperScissors = self.view
        view.responses[interaction.user.id] = self.values[0]

        embed = view.message.embeds[0].copy()
        embed.description = f"> {view.ctx.default_tick(view.player1.id in view.responses)} {view.player1.display_name}" \
                            f"\n> {view.ctx.default_tick(view.player2.id in view.responses)} {view.player2.display_name}"

        await view.message.edit(embed=embed)

        if len(view.responses) == 2:
            response = view.check_winner()
            embed.description = f"> ✅ **{view.player1.display_name}** chose **{view.responses[view.player1.id]}**" \
                                f"\n> ✅ **{view.player2.display_name}** chose **{view.responses[view.player2.id]}**" \
                                f"\n" \
                                f"\n{response}"

            view.clear_items()
            await view.message.edit(embed=embed, view=view)
            view.stop()


class RockPaperScissors(discord.ui.View):

    def __init__(self, ctx: commands.Context, player1: discord.Member, player2: discord.Member):
        super().__init__()
        self.message: discord.Message = None
        self.ctx: commands.Context = ctx
        self.player1: discord.Member = player1
        self.player2: discord.Member = player2
        self.responses = {}
        self.add_item(ObjectSelector())

    async def interaction_check(self, interaction: Interaction) -> bool:
        if not interaction.user or interaction.user.id not in (self.player1.id, self.player2.id):
            await interaction.response.send_message('You are not a part of this game!', ephemeral=True)
            return False
        if interaction.user.id in self.responses:
            await interaction.response.send_message(f'You already selected **{self.responses[interaction.user.id]}**, sorry!', ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        for item in self.children:
            if isinstance(item, discord.ui.Select):
                item.placeholder = "Timed out! Please try again."
            item.disabled = True
        await self.message.edit(view=self)

    def check_winner(self):
        mapping = {
            'Rock': 0,
            'Paper': 1,
            'Scissors': 2
        }
        win_1 = f'**{self.responses[self.player1.id]}** beats **{self.responses[self.player2.id]}** - **{self.player1.display_name}** wins! 🎉'
        win_2 = f'**{self.responses[self.player2.id]}** beats **{self.responses[self.player1.id]}** - **{self.player2.display_name}** wins! 🎉'
        tie = f'It\'s a **tie**! both players lose. 👔'

        if self.responses[self.player1.id] == self.responses[self.player2.id]:
            return tie
        elif (mapping[self.responses[self.player1.id]] + 1) % 3 == mapping[self.responses[self.player2.id]]:
            return win_2
        else:
            return win_1

class ButtonPaginator(discord.ui.View):
    def __init__(self, another_list: list, ctx: commands.Context, **kwargs):
        super().__init__(timeout=30)
        self.value: int = 0
        self.some_list: List[discord.Embed] = another_list
        self.ctx: commands.Context = ctx

    async def on_timeout(self) -> None:
        for button in self.children:
            button.disabled = True
        await self.message.edit(embed=self.some_list[self.value], view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        if self.ctx.author == interaction.user:
            return True
        else:
            embed = discord.Embed(description=f"This isn't your embed and thus you can't react to it! If you want to, open a prompt for yourself. Use `{self.ctx.prefix}help {self.ctx.command.name}` for more info!", color = self.ctx.bot.theme)
            return await interaction.response.send_message(embed=embed, ephemeral=True)         
            

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}")
    async def first(self, button: discord.ui.Button, interaction: discord.Interaction):
        print(await self.interaction_check(interaction))
        self.value = 0
        self.some_list[0].set_footer(text=f"1/{len(self.some_list)}")
        self.children[0].disabled = True
        self.children[1].disabled = True
        self.children[3].disabled = False
        self.children[4].disabled = False
        await interaction.message.edit(embed=self.some_list[0], view=self)

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⬅️")
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.value - 1 < 0:
            return
        if self.value - 1 == 0:
            self.children[0].disabled = True
            self.children[1].disabled = True
            self.children[3].disabled = False
            self.children[4].disabled = False
            self.value -= 1
        else:
            self.value -= 1
            self.children[0].disabled = False
            self.children[1].disabled = False
            self.children[3].disabled = False
            self.children[4].disabled = False
        self.some_list[self.value].set_footer(text=f"{self.value+1}/{len(self.some_list)}")
        await interaction.message.edit(embed=self.some_list[self.value], view=self)

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏹️")
    async def stop(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.edit(view=None)

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="➡️")
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.value + 1 > len(self.some_list) - 1:
            return
        if self.value + 1 == len(self.some_list) - 1:
            self.value += 1
            self.children[0].disabled = False
            self.children[1].disabled = False
            self.children[3].disabled = True
            self.children[4].disabled = True
        else:
            self.value += 1
            self.children[0].disabled = False
            self.children[1].disabled = False
            self.children[3].disabled = False
            self.children[4].disabled = False
        self.some_list[self.value].set_footer(text=f"{self.value+1}/{len(self.some_list)}")
        await interaction.message.edit(embed=self.some_list[self.value], view=self)

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}")
    async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.value != (len(self.some_list) - 1):
            self.value = len(self.some_list) - 1
            self.children[0].disabled = False
            self.children[1].disabled = False
            self.children[3].disabled = True
            self.children[4].disabled = True
            self.some_list[self.value].set_footer(text=f"{len(self.some_list)}/{len(self.some_list)}")
            await interaction.message.edit(embed=self.some_list[self.value], view=self)