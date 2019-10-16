from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np


class BasePage(Page):
    def vars_for_template(self):
        all_players = self.player.in_all_rounds()
        all_players.reverse()
        v = {
            # 'treatment': self.session.config['treatment'],
            'num_rounds': Constants.interaction_length[self.player.interaction_number-1],
            'all_players': all_players,
        }
        v.update(self.extra_vars_for_template())
        return v

    def extra_vars_for_template(self):
        return {}


class BaseWaitPage(WaitPage):
    def vars_for_template(self):
        all_players = self.player.in_all_rounds()
        all_players.reverse()
        v = {
            # 'treatment': self.session.config['treatment'],
            'num_rounds': Constants.interaction_length[self.player.interaction_number-1],
            'all_players': all_players,
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
        if not self.timeout_happened:
            p.timed_out = 0
            choice = p.choice
            p.noise = np.random.normal(0, Constants.deltas1[choice])
            if p.treatment % 2 == 1:
                p.mu = Constants.mus1[self.round_number-1, choice]
                p.payoff = np.round(p.mu + p.noise)
            else:
                p.mu = Constants.mus2[self.round_number-1, choice]
                p.payoff = np.round(p.mu + p.noise)
        else:
            p.timed_out = 1
            p.choice = -1
            p.payoff = 0

        if p.treatment % 2 == 1:
            p.best_mu = max(Constants.mus1[self.round_number - 1])
        else:
            p.best_mu = max(Constants.mus2[self.round_number - 1])
        p.cum_payoff = sum([p.payoff for p in p.in_all_rounds() if p.interaction_number == p.interaction_number])
        p.num_decisions = sum([1-p.timed_out for p in p.in_all_rounds() if p.interaction_number == p.interaction_number])
        if p.num_decisions == 0:
            p.avg_payoff = 0
        else:
            p.avg_payoff = np.around(float(p.cum_payoff) / p.num_decisions, decimals=1)


class DecisionWaitPage(BaseWaitPage):
    template_name = 'multiarm_bandit/DecisionWaitPage.html'

    def is_displayed(self):
        return (self.player.interaction_number == 3 and
                 self.player.round_in_interaction > Constants.info_round)

    def after_all_players_arrive(self):
        # it only gets executed once
        payoffs = [p.payoff for p in self.group.get_players() if p.timed_out == 0]
        for p in self.group.get_players():
            if len(payoffs) > 0:
                p.max_pay = np.around(float(max(payoffs)), decimals=0)
                p.average_pay = np.around(float(sum(payoffs))/len(payoffs), decimals=1)
            else:
                p.max_pay = 0
                p.average_pay = 0


class Results(BasePage):
    def get_timeout_seconds(self):
        if self.player.timed_out:
            return 3
        else:
            return 8


class NewInfo(BasePage):
    timeout_seconds = 36

    def is_displayed(self):
        return (self.player.interaction_number == 3 and self.player.round_in_interaction == Constants.info_round)


class NewInfoWaitPage(BaseWaitPage):
    template_name = 'multiarm_bandit/NewInfoWaitPage.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return (self.player.interaction_number == 3 and self.player.round_in_interaction == Constants.info_round)


class InteractionResultsPage(BasePage):
    timeout_seconds = 20

    def is_displayed(self):
        return self.player.round_in_interaction == Constants.interaction_length[self.player.interaction_number-1]



class InteractionWaitPage(BaseWaitPage):
    template_name = 'multiarm_bandit/InteractionWaitPage.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.player.round_in_interaction == Constants.interaction_length[self.player.interaction_number-1]


page_sequence = [
    Introduction,
    Decision,
    DecisionWaitPage,
    Results,
    NewInfo,
    NewInfoWaitPage,
    InteractionResultsPage,
    InteractionWaitPage,
]
