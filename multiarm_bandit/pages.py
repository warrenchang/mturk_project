from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np


class BasePage(Page):
    def vars_for_template(self):
        v =  {
            # 'treatment': self.session.config['treatment'],
            'num_rounds': Constants.interaction_length[self.player.interaction_number-1],
        }
        v.update(self.extra_vars_for_template())
        return v

    def extra_vars_for_template(self):
        return {}


class Introduction(BasePage):
    # timeout_seconds = 30

    def is_displayed(self):
        if self.player.interaction_number == 1:
            print('This is the start of new match')
        return self.player.round_in_interaction == 1
        # return self.player.round_in_interaction == 1 and (not self.session.config['debug'])


class Decision(BasePage):
    timeout_seconds = 20
    form_model = 'player'
    form_fields = ['choice']

    def before_next_page(self):
        p = self.player

        if self.timeout_happened:
            p.choice = np.random.randint(5)
        choice = p.choice
        p.noise = np.random.normal(0,Constants.deltas[choice])
        p.payoff = np.round(Constants.mus1[self.round_number-1,choice] + p.noise)

    def extra_vars_for_template(self):
        previous_players = self.player.in_previous_rounds()
        previous_players.reverse()
        v = {
            'previous_players': previous_players,
        }
        return v


class Results(BasePage):
    timeout_seconds = 9

    def extra_vars_for_template(self):
        all_players = self.player.in_all_rounds()
        all_players.reverse()
        v = {
            'all_players': all_players,
        }
        return v



page_sequence = [
    Introduction,
    Decision,
    Results
]
