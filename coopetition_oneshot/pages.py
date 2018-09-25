from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from otree_mturk_utils.pages import CustomMturkPage, CustomMturkWaitPage
from .models import Constants
import random
import math


def get_share(p1,p2):
    if p1==0 and p2 ==0:
        return 1/2
    else:
        return p1/(p1+p2)



class Decision(Page):
    timeout_seconds = 90
    form_model = 'player'
    form_fields = ['a1','a2']

    def is_displayed(self):
        return self.participant.vars['qualified'] and (not self.participant.vars['matched'])

    def error_message(self, values):
        if values["a1"] + values["a2"] > 10:
            return 'The sum of the numbers cannot be greater than 10.'

    def before_next_page(self):
        # calculate the payoff based on the decision of one participant
        a1 = 5
        a2 = 5
        a3 = 0
        p = self.player
        p.a3 = 10 - p.a1 - p.a2

        if p.condition == 'Fix':
            ## a random number between 1 and 200 (inclusive)
            rand_num = int(math.ceil(random.random() * 200))
            ## a random number between 1 and 110 (inclusive)
        elif p.condition == 'Var':
            rand_num = int(math.ceil(random.random() * 110))

        if p.condition =='Det':
            pie = p.a1*a1 + p.A
        elif p.condition =='Fix':
            if rand_num <= 100: # investment is a success
                pie = 2*p.a1*a1 + p.A
            else:
                pie = p.A
        elif p.condition =='Var':
            if rand_num <= p.a1*a1: # investment is a success
                pie = 200 + p.A
            else:
                pie = p.A

        print('Coopetition one-shot game, participant payoff')
        print(self.participant.payoff)
        p.payoff = pie*get_share(p.a2,a2)+ p.a3
        print('Coopetition one-shot game, participant payoff after update')
        print(self.participant.payoff)


class Results(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.participant.vars['qualified'] and (not self.participant.vars['matched'])


page_sequence = [
    Decision,
    # Results,
]
