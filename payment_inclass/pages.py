from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import numpy as np


class PaymentAdjustment(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        num_payment = self.session.config['num_payment']
        total_payment = self.session.config['total_payment']
        players = self.subsession.get_players()
        payoffs = [p.participant.payoff for p in players]
        print(payoffs)
        threshold = np.sort(payoffs)[-num_payment:].min()
        print(threshold)
        for p in players:
            p.participant_payoff = p.participant.payoff
            if p.participant.payoff < threshold:
                p.participant.payoff = 0
        total_points = np.sum([p.participant.payoff for p in players])
        print(total_points)
        for p in players:
            p.participant.payoff = int(total_payment * p.participant.payoff / total_points)
            print(p.participant.payoff)


class PaymentInfo(Page):
    def vars_for_template(self):
        participant = self.participant
        print(participant.vars)
        return {
            'experiment_payoff': self.player.participant_payoff,
            'final_payment': self.participant.payoff.to_real_world_currency(self.session),
            'num_payment': self.session.config['num_payment'],
        }

page_sequence = [
    PaymentAdjustment,
    PaymentInfo
]
