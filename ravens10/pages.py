from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
import time

class StartPage(Page):
    def is_displayed(self):
        if self.round_number == 1:
            print('This is the start of Ravens tests')
        return self.round_number == 1 and (not self.session.config['debug'])


class Introduction(Page):

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        # user has 5 minutes to complete as many pages as possible
        self.participant.vars['expiry_timestamp'] = time.time() + Constants.minutes_given*60

    def vars_for_template(self):
        return {
            'ravens_payoff_per_question': self.session.config['ravens_payoff_per_question'],
            'image_path': Constants.name_in_url+'/example.png'
        }


class QuestionPage(Page):
    form_model = 'player'
    form_fields = ['answer']

    def get_timeout_seconds(self):
        return self.participant.vars['expiry_timestamp'] - time.time()

    def vars_for_template(self):
        return {
            'ravens_payoff_per_question': self.session.config['ravens_payoff_per_question'],
            'image_path': Constants.name_in_url+'/{}.png'.format(self.round_number)
        }

    def before_next_page(self):
        if self.timeout_happened:
            self.player.answer = 0
        self.player.ans_correct = self.player.answer == Constants.answer_keys[self.round_number-1]
        self.player.participant.vars['ravens_payoff'] += self.player.ans_correct * self.session.config['ravens_payoff_per_question']
        self.player.payoff = self.player.ans_correct*self.session.config['ravens_payoff_per_question']


class Belief(Page):
    form_model = 'player'
    form_fields = ['belief1','belief2']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds



class Results(Page):
    # timeout_seconds = 60

    def is_displayed(self):
        return False
        # return (self.round_number == Constants.num_rounds) and (self.session.config['ravens_payoff_per_question']>0)

    def vars_for_template(self):
        return {
            'total_correct': sum([p.ans_correct for p in self.player.in_all_rounds()]),
            'earnings': sum([p.ans_correct for p in self.player.in_all_rounds()])*self.participant.vars['ravens_payoff_per_question']>0
                }

    # def before_next_page(self):
    #     for p in self.subsession.get_players():
    #         p.participant.vars['payoff_ravens'] = (sum([p.ans_correct for p in self.player.in_all_rounds()]) *
    #                                                self.participant.vars['ravens_payoff_per_question'] > 0)


page_sequence = [
    # StartPage,
    Introduction,
    QuestionPage,
    Belief,
    Results
]
