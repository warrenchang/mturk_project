from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        yield(pages.SurveyPage1,
              {'gender':'male', 'age': 16, 'birth_place':'Middle East'}
              )
