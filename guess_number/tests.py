from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield(pages.Guess, {'guess':random.randint(0, 100)})
        yield(pages.Results)
        if self.subsession.round_number == Constants.num_rounds:
            yield(pages.Payment)

