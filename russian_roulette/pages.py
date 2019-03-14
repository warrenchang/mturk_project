from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from otree_mturk_utils.pages import CustomMturkPage, CustomMturkWaitPage
from .models import Constants


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

        if p.rand_number <= p.choice:
            p.payoff = Constants.bonus - p.choice
            p.bullets -= 1

        if p.rand_number < p.bullets/6:
            p.payoff = 0

        if self.timeout_happened:
            p.payoff = 0


class Results(CustomMturkPage):
    timeout_seconds = 30
    def is_displayed(self):
        if 'qualified' in self.participant.vars:
            return self.participant.vars['qualified']
        else:
            return True

class EndInfo(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    Decision,
    EndInfo,
]
