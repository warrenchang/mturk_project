from otree.api import Currency as c, currency_range
from . import pages1
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages1.SomeUnderstandingQuestions)
        yield (pages1.QuizResults)
