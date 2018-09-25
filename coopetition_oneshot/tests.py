from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
import math


class PlayerBot(Bot):
    def play_round(self):
        a1 = int(math.ceil(random.random() * 5))
        a2 = int(math.ceil(random.random() * 5))
        yield (pages.Decision, {"a1": a1, "a2":a2})
