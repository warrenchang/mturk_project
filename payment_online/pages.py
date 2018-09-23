from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import math


class PaymentAdjustment(Page):
    timeout_seconds = 0

    def before_next_page(self):
        if not self.participant.vars['qualified']:
            self.participant.payoff -= (self.session.config['participation_fee']
                                     / self.session.config['real_world_currency_per_point'])


class PaymentInfo(Page):
    timeout_seconds = 30
    def vars_for_template(self):
        print(self.participant.vars)
        return {
            'qualified': self.participant.vars['qualified'],
            'participation_fee': self.session.config['participation_fee'],
            'experiment_payoff': self.participant.payoff,
            'payment': self.participant.payoff_plus_participation_fee() - self.session.config['participation_fee'],
            'final_payment': self.participant.payoff_plus_participation_fee(),
        }


page_sequence = [
    PaymentAdjustment,
    PaymentInfo]
