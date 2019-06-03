from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1 and (not self.session.config['debug'])


class Guess(Page):
    form_model = 'player'
    form_fields = ['guess']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.guess = random.randint(0, 100)


class DecisionWaitPage(WaitPage):
    template_name = 'guess_number/DecisionWaitPage.html'

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        sorted_guesses = sorted(p.guess for p in self.group.get_players())
        return {'sorted_guesses': sorted_guesses}


class ResultsWaitPage(WaitPage):
    template_name = 'guess_number/ResultsWaitPage.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number != Constants.num_rounds

    def vars_for_template(self):
        sorted_guesses = sorted(p.guess for p in self.group.get_players())
        return {'sorted_guesses': sorted_guesses}


class Payment(Page):
    # wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        paying_round = self.session.vars['paying_round']
        num_winners = self.session.vars['num_winners']
        is_winner = self.participant.vars['is_winner']
        cum_payoff = sum([p.payoff for p in self.player.in_all_rounds()]).to_real_world_currency(self.session)
        return {'paying_round': paying_round, 'num_winners':num_winners, 'is_winner':is_winner, 'cum_payoff':cum_payoff}


page_sequence = [Introduction,
                 Guess,
                 DecisionWaitPage,
                 Results,
                 ResultsWaitPage,
                 Payment
                 ]
