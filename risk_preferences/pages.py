from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from otree_mturk_utils.pages import CustomMturkPage, CustomMturkWaitPage
from .models import Constants
import random


class Decision(CustomMturkPage):
    timeout_seconds = 480
    form_model = 'player'
    form_fields = ['choice']

    def is_displayed(self):
        if 'qualified' in self.participant.vars:
            return self.participant.vars['qualified']
        else:
            return True

    def before_next_page(self):
        p = self.player
        p.rand_number = int(random.random()*10)+1
        if p.rand_number <= 5:
            p.payoff = Constants.outcomesA[p.choice-1]
        else:
            p.payoff = Constants.outcomesB[p.choice-1]

        if self.timeout_happened:
            p.payoff = 0


class Results(CustomMturkPage):
    timeout_seconds = 30
    def is_displayed(self):
        if 'qualified' in self.participant.vars:
            return self.participant.vars['qualified']
        else:
            return True

page_sequence = [
    Decision,
    Results
]
