from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import math


class EndInfo(Page):
    timeout_seconds = 185

    def vars_for_template(self):
        participation_fee = self.session.config['participation_fee']
        final_payment = self.participant.payoff_plus_participation_fee()
        payoff_info = [
            ('Allocation task','To be determined.'),
            ('Coin tossing task 1', str(c(self.participant.vars['lying1_payoff']))),
            ("Lottery Task 1", str(c(self.participant.vars['lottery_payoff_info'][0][-1]))),
            ("Lottery Task 2", str(c(self.participant.vars['lottery_payoff_info'][1][-1]))),
            ('Number guessing task', str(c(self.participant.vars['lying2_payoff']))),
            ("Urn Gamble 1", str(c(self.participant.vars['ambiguity_payoff_info'][0][-1]))),
            ("Urn Gamble 2", str(c(self.participant.vars['ambiguity_payoff_info'][1][-1]))),
            ('Coin tossing task 2', str(c(self.participant.vars['lying3_payoff']))),
            ('Solving puzzles', str(c(self.participant.vars['ravens_payoff']))),
            ('Logical questions', str(c(self.participant.vars['crt_payoff'])),)
        ]

        return {
            'payoff_info': payoff_info,
            'participation_fee': participation_fee,
            'payoff_in_points': self.participant.payoff,
            'bonus_payment': final_payment - participation_fee,
            'final_payment':  final_payment,
        }

page_sequence = [
    EndInfo,
]
