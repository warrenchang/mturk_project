from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.Decision,
               {"time": random.choice(['1200','0800']),
                "place": random.choice(['train station','tiananmen'])
                }
               )
        yield (pages.Results)
