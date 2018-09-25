from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from otree_mturk_utils.pages import CustomMturkPage, CustomMturkWaitPage
from .models import Constants
import random
import math


class BasePage(CustomMturkPage):
    def vars_for_template(self):
        v =  {
            'other_player': self.player.get_partner(),
        }
        v.update(self.extra_vars_for_template())
        return v

    def extra_vars_for_template(self):
        return {}


class BaseWaitPage(WaitPage):
    def vars_for_template(self):
        v =  {
            'other_player': self.player.get_partner(),
        }
        v.update(self.extra_vars_for_template())
        return v

    def extra_vars_for_template(self):
        return {}


class MatchingWaitPage(CustomMturkWaitPage):
    # template_name = 'coopetition_mturk/MatchingWaitPage.html'
    group_by_arrival_time = True
    extra_template = Constants.extra_info
    startwp_timer = 180

    def is_displayed(self):
        return (self.participant.vars['qualified'] and (self.round_number == 1))


class StartPage(BasePage):
    timeout_seconds = 90

    def is_displayed(self):
        return (self.participant.vars['qualified'] and
                self.player.round_number == 1)

    def before_next_page(self):
        ## the variable "matched" is true only if the player is successfully matched.
        self.participant.vars['matched'] = True


class Introduction(BasePage):
    timeout_seconds = 90

    def is_displayed(self):
        if self.player.round_in_interaction == 1:
            print('This is the start of new match')
        return (self.participant.vars['qualified'] and
                self.player.round_in_interaction == 1 and
                self.player.interaction_number == 2)


class Decision(BasePage):
    form_model = 'player'
    form_fields = ['a1','a2']

    def get_timeout_seconds(self):
        if (self.round_number <= 5) and (self.player.interaction_number == 1):
            return 60
        else:
            return 30

    def is_displayed(self):
        return self.participant.vars['qualified']

    def error_message(self, values):
        if values["a1"] + values["a2"] > 10:
            return 'The sum of the numbers cannot be greater than 10.'

    def before_next_page(self):
        if self.timeout_happened:
            self.player.a1 = int(math.ceil(random.random()*10))
            self.player.a2 = int(math.ceil(random.random()*(10-self.player.a1)))
            self.player.timed_out = True
        else:
            self.player.timed_out = False

        self.player.a3 = 10 - self.player.a1 - self.player.a2


class DecisionWaitPage(BaseWaitPage):
    template_name = 'coopetition_mturk/DecisionWaitPage.html'

    def is_displayed(self):
        return self.participant.vars['qualified']

    def after_all_players_arrive(self):
        # it only gets executed once
        ## the condition is added so that mturk customized wait page can go though in case no matching is made
        if len(self.group.get_players())==2:
            self.group.interact()
        # print('players have interacted!')


class Results(BasePage):
    timeout_seconds = 30

    def extra_vars_for_template(self):
        return {'x1x2': self.player.a1*self.player.other_a1}

    def is_displayed(self):
        return self.participant.vars['qualified']

    def before_next_page(self):
        self.player.cum_payoff = sum([p.payoff for p in self.player.in_all_rounds()
                                      if p.interaction_number == self.player.interaction_number])


class InteractionResults(BasePage):
    timeout_seconds = 10

    def is_displayed(self):
        return self.participant.vars['qualified'] and self.player.round_in_interaction == Constants.interaction_length[self.player.interaction_number-1]


class InteractionWaitPage(BaseWaitPage):
    template_name = 'coopetition_mturk/InteractionWaitPage.html'

    def is_displayed(self):
        return self.participant.vars['qualified'] and self.player.round_in_interaction == Constants.interaction_length[self.player.interaction_number-1]


page_sequence = [
    MatchingWaitPage,
    StartPage,
    Introduction,
    Decision,
    DecisionWaitPage,
    Results,
    InteractionResults,
    InteractionWaitPage,
]
