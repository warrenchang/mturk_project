from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random


class BasePage(Page):
    def vars_for_template(self):
        v =  {
            # 'treatment': self.session.config['treatment'],
            'other_player': self.player.get_partner(),
            'num_rounds': Constants.interaction_length[self.player.interaction_number-1],
            'p11': Constants.payoff_matrix[self.player.interaction_number][self.player.id_in_group]['A']['A'],
            'p12': Constants.payoff_matrix[self.player.interaction_number][self.player.id_in_group]['A']['B'],
            'p21': Constants.payoff_matrix[self.player.interaction_number][self.player.id_in_group]['B']['A'],
            'p22': Constants.payoff_matrix[self.player.interaction_number][self.player.id_in_group]['B']['B'],

            'p11o': Constants.payoff_matrix[self.player.interaction_number][3-self.player.id_in_group]['A']['A'],
            'p12o': Constants.payoff_matrix[self.player.interaction_number][3-self.player.id_in_group]['A']['B'],
            'p21o': Constants.payoff_matrix[self.player.interaction_number][3-self.player.id_in_group]['B']['A'],
            'p22o': Constants.payoff_matrix[self.player.interaction_number][3-self.player.id_in_group]['B']['B'],
        }
        v.update(self.extra_vars_for_template())
        return v

    def extra_vars_for_template(self):
        return {}


class BaseWaitPage(WaitPage):
    def vars_for_template(self):
        v =  {
            # 'treatment': self.session.config['treatment'],
            'other_player': self.player.get_partner(),
            'num_rounds': Constants.interaction_length[self.player.interaction_number-1],
            'p11': Constants.payoff_matrix[self.player.interaction_number][self.player.id_in_group]['A']['A'],
            'p12': Constants.payoff_matrix[self.player.interaction_number][self.player.id_in_group]['A']['B'],
            'p21': Constants.payoff_matrix[self.player.interaction_number][self.player.id_in_group]['B']['A'],
            'p22': Constants.payoff_matrix[self.player.interaction_number][self.player.id_in_group]['B']['B'],

            'p11o': Constants.payoff_matrix[self.player.interaction_number][3-self.player.id_in_group]['A']['A'],
            'p12o': Constants.payoff_matrix[self.player.interaction_number][3-self.player.id_in_group]['A']['B'],
            'p21o': Constants.payoff_matrix[self.player.interaction_number][3-self.player.id_in_group]['B']['A'],
            'p22o': Constants.payoff_matrix[self.player.interaction_number][3-self.player.id_in_group]['B']['B'],
        }
        v.update(self.extra_vars_for_template())
        return v

    def extra_vars_for_template(self):
        return {}

class Introduction(BasePage):
    # timeout_seconds = 30

    def is_displayed(self):
        if self.player.round_in_interaction == 1:
            print('This is the start of new match')
        return self.player.round_in_interaction == 1 and (not self.session.config['debug'])
        # return self.round_number == 1


class Decision(BasePage):
    timeout_seconds = 32
    form_model = 'player'
    form_fields = ['action']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.action = random.choice(['A','B'])


class DecisionWaitPage(BaseWaitPage):
    template_name = 'repeated_game_PD/DecisionWaitPage.html'

    def after_all_players_arrive(self):
        # it only gets executed once
        self.group.interact()
        # print('players have interacted!')


class Results(BasePage):
    timeout_seconds = 10
    # def get_timeout_seconds(self):
    #     if self.player.treatment == 'reputation':
    #         return None
    #     else:
    #         return 30


# class ResultsWaitPage(BaseWaitPage):
class ResultsWaitPage(WaitPage):
    template_name = 'repeated_game_PD/ResultsWaitPage.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.player.treatment == 'reputation'


class InteractionResults(BasePage):
    timeout_seconds = 30

    def is_displayed(self):
        return self.player.round_in_interaction == Constants.interaction_length[self.player.interaction_number-1]


class InteractionWaitPage(BaseWaitPage):
    template_name = 'repeated_game_PD/InteractionWaitPage.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.player.round_in_interaction == Constants.interaction_length[self.player.interaction_number-1]

page_sequence = [
    Introduction,
    Decision,
    DecisionWaitPage,
    Results,
    ResultsWaitPage,
    InteractionResults,
    InteractionWaitPage,
]
