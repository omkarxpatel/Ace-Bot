from datetime import datetime
from discord.ext import commands

class OnCooldown(commands.CheckFailure):
    def __init__(self, *, dateobject: datetime):
        self._dateobject = dateobject

    @property
    def time(self):
      return self._dateobject


class NotRegistered(commands.CheckFailure):
    def __init__(self, *, ctx: commands.Context):
        self._context = ctx

    @property
    def ctx(self):
        return self._context