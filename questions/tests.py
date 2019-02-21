from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.Page1, {
            "Q1": random.choice(range(1, 8)),
            "Q2": random.choice(range(1, 8)),
            "Q3": random.choice(range(1, 8)),
            "Q4": random.choice(range(1, 8)),
            "Q5": random.choice(range(1, 8)),
            "Q6": random.choice(range(1, 8)),
            "Q7": random.choice(range(1, 8)),
            "Q8": random.choice(range(1, 8)),
        })

