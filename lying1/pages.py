from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Decision(Page):
    form_model = 'player'
    form_fields = ['outcome']


    def before_next_page(self):
        self.player.payoff = self.player.outcome*Constants.payment_per_incidence
        self.participant.vars['lying1_payoff'] = self.player.payoff


page_sequence = [
    Decision,
]
