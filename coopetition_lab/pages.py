from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random
import math


class BasePage(Page):
    def vars_for_template(self):
        v =  {
            'other_player': self.player.get_partner(),
            'decision_time': self.session.config['decision_time'],
        }
        v.update(self.extra_vars_for_template())
        return v

    def extra_vars_for_template(self):
        return {}


class BaseWaitPage(WaitPage):
    def vars_for_template(self):
        v =  {
            'other_player': self.player.get_partner(),
            'decision_time': self.session.config['decision_time'],
        }
        v.update(self.extra_vars_for_template())
        return v

    def extra_vars_for_template(self):
        return {}


class MatchingWaitPage(BaseWaitPage):
    template_name = 'coopetition_lab/MatchingWaitPage.html'
    # wait_for_all_groups = True
    group_by_arrival_time = True

    def is_displayed(self):
        return (self.participant.vars['qualified'] and (self.round_number == 1))


class PostMatchingWaitPage(BaseWaitPage):
    template_name = 'coopetition_lab/MatchingWaitPage.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return (self.participant.vars['qualified'] and (self.round_number == 1))


class StartPage(BasePage):
    timeout_seconds = 30

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


class SettingParameters(BasePage):
    ## this page is used to set parameters for players
    timeout_seconds = 0

    def is_displayed(self):
        return self.participant.vars['qualified']

    def before_next_page(self):
        ## the variable "matched" is true only if the player is successfully matched.
        self.player.endowment = 10
        self.player.other_endowment = 10
        if self.player.condition == "Asm":
            if self.player.id_in_group == 1:
                self.player.endowment = 20
                self.player.role = 'A'
            else:
                self.player.other_endowment = 20
                self.player.role = 'B'



class Decision(BasePage):
    form_model = 'player'
    form_fields = ['a1','a2']

    def get_timeout_seconds(self):
        if (self.round_number <= 5) and (self.player.interaction_number == 1):
            return 60
        else:
            return self.session.config['decision_time']

    def is_displayed(self):
        return self.participant.vars['qualified']

    def error_message(self, values):
        if values["a1"] + values["a2"] > self.player.endowment:
            return 'The sum of the numbers cannot be greater than %d.'%self.player.endowment

    def before_next_page(self):
        if self.timeout_happened:
            self.player.a1 = int(math.ceil(random.random()*self.player.endowment))
            self.player.a2 = int(math.ceil(random.random()*(self.player.endowment-self.player.a1)))
            self.player.timed_out = True
        else:
            self.player.timed_out = False

        self.player.a3 = self.player.endowment - self.player.a1 - self.player.a2


class DecisionWaitPage(BaseWaitPage):
    template_name = 'coopetition_lab/DecisionWaitPage.html'

    def is_displayed(self):
        return self.participant.vars['qualified']

    def after_all_players_arrive(self):
        # it only gets executed once
        ## the condition is added so that lab customized wait page can go though in case no matching is made
        if len(self.group.get_players())==2:
            self.group.interact()
        # print('players have interacted!')


class Results(BasePage):
    timeout_seconds = 20

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
        return self.player.round_in_interaction == Constants.interaction_length[self.player.interaction_number-1]


class InteractionWaitPage1(BaseWaitPage):
    template_name = 'coopetition_lab/InteractionWaitPage.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return (self.player.round_in_interaction == Constants.interaction_length[self.player.interaction_number-1]) and not (self.player.round_number == Constants.num_rounds)

class InteractionWaitPage2(BaseWaitPage):
    template_name = 'coopetition_lab/InteractionWaitPage.html'

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

page_sequence = [
    MatchingWaitPage,
    PostMatchingWaitPage,
    SettingParameters,
    StartPage,
    Introduction,
    Decision,
    DecisionWaitPage,
    Results,
    InteractionResults,
    InteractionWaitPage1,
    InteractionWaitPage2,
]
