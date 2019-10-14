from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import math



class EndInfo(Page):
    def vars_for_template(self):
        print(self.participant.vars)
        final_payment = self.participant.payoff_plus_participation_fee()
        self.player.final_payment = final_payment
        if final_payment < 30:
            final_payment = 30
        return {
            'participation_fee': self.session.config['participation_fee'],
            'experiment_currency': self.participant.payoff,
            'final_payment': final_payment,
            'language': self.session.config['language']
        }

page_sequence = [
    EndInfo,
]
