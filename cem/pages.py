from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext as _


# variables for all templates
# --------------------------------------------------------------------------------------------------------------------
def vars_for_all_templates(self):
    player = self.player
    return {
        'lottery_x':  c(Constants.lottery_x[player.set_number-1][player.round_in_set-1]),
        'lottery_px':  Constants.lottery_px[player.set_number-1][player.round_in_set-1],
        'lottery_y':  c(Constants.lottery_y[player.set_number-1][player.round_in_set-1]),
        'lottery_py':  100-Constants.lottery_px[player.set_number-1][player.round_in_set-1],
        'sure_payoffs': Constants.sure_payoffs[player.set_number-1][player.round_in_set-1],
    }

# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):

    # only display instruction in round 1
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        return self.player.round_in_set == 1


# ******************************************************************************************************************** #
# *** PAGE DECISION *** #
# ******************************************************************************************************************** #
class Decision(Page):
    # form model
    form_model = 'player'

    # form fields
    # ----------------------------------------------------------------------------------------------------------------
    form_fields = ['choice_' + str(k) for k in range(1, Constants.num_choices+1)]

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):
        player = self.player
        form_fields = ['choice_' + str(k) for k in range(1, Constants.num_choices+1)]
        return {
            'choices':  zip(form_fields, Constants.sure_payoffs[player.set_number-1][player.round_in_set-1])
        }

    # set payoff, determine consistency, and set switching row
    # ----------------------------------------------------------------------------------------------------------------
    def before_next_page(self):
        # set payoff
        self.player.set_payoffs()
        # set certainty equivalent
        self.player.set_ce()


# ******************************************************************************************************************** #
# *** PAGE RESULTS *** #
# ******************************************************************************************************************** #
class Results(Page):

    # skip results until last page
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        # return self.round_number == Constants.num_rounds
        return False


    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):
        for set,lottery,x,px,y,sp,choice,payoff in self.participant.vars['lottery_payoff_info']:
            print(set,lottery,x,px,y,sp,choice,payoff )
        return {
            'payment_info' : self.participant.vars['lottery_payoff_info']
        }


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Decision]

if Constants.instructions:
    page_sequence.insert(0, Instructions)

if Constants.results:
    page_sequence.append(Results)
