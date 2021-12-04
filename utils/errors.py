from datetime import datetime
from discord.ext import commands

class OnCooldown(commands.CheckFailure):
    def __init__(self, *, dateobject: datetime):
        self._dateobject = dateobject

    @property
    def time(self):
      return self._dateobject