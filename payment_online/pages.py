from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import math


class PaymentAdjustment(Page):
    timeout_seconds = 0

    def before_next_page(self):
        self.participant.vars['payoff_points'] = self.participant.payoff

        if not self.participant.vars['qualified']:
            self.participant.payoff -= (self.session.config['participation_fee']
                                     / self.session.config['real_world_currency_per_point'])
        else:
            ## note that you need to change Currency to float in order to maintain the precision!!!!

            # ## record the un-rounded payoff in points
            # payoff_points = self.participant.payoff
            # ## record the payoff in points so that the real payoff is rounded up to the nearest $0.1
            # rounded_payoff_points = (math.ceil(float(payoff_points)*self.session.config['real_world_currency_per_point']*10)
            #                          /10/self.session.config['real_world_currency_per_point'])
            # self.participant.payoff = c(rounded_payoff_points)

            ## For qualified workers, make sure that the minimum payoff from points is $0.1

            if (self.participant.payoff  > 0) and (self.participant.payoff < 0.1/self.session.config['real_world_currency_per_point']):
                self.participant.payoff = c(0.1/self.session.config['real_world_currency_per_point'])

        self.player.final_payment = float(self.participant.payoff_plus_participation_fee())
        self.player.bonus = self.player.final_payment - float(self.session.config['participation_fee'])
        self.participant.vars['experiment_payment'] = self.player.final_payment - self.session.config['participation_fee']
        if 'workerid' in self.participant.vars:
            self.player.workerid = self.participant.vars['workerid']




class EndInfo(Page):
    def vars_for_template(self):
        print(self.participant.vars)
        return {
            'qualified': self.participant.vars['qualified'],
            'participation_fee': self.session.config['participation_fee'],
            'experiment_payoff': c(self.participant.vars['payoff_points']),
            'payment': self.participant.vars['experiment_payment'],
            'final_payment':  self.participant.payoff_plus_participation_fee(),
        }

page_sequence = [
    PaymentAdjustment,
    EndInfo,
]
