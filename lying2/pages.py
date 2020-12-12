from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Decision(Page):
    form_model = 'player'
    form_fields = ['outcome']

    def vars_for_template(self):
        guess_bonus = Constants.guess_bonus
        deduction = Constants.deduction

        return {
            'guess_bonus': guess_bonus,
            'deduction': deduction,
            'bonus_off10': guess_bonus - deduction*10,
        }


    def before_next_page(self):
        self.player.payoff = max(Constants.guess_bonus - abs(self.player.outcome - 27)*Constants.deduction,0)
        self.participant.vars['lying2_payoff'] = self.player.payoff


page_sequence = [
    Decision,
]
