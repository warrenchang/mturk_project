from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from eet.config import *

# set number of pages per list
# --------------------------------------------------------------------------------------------------------------------
if Constants.one_page:
    pages_per_list = 1
else:
    pages_per_list = 2

# ::: variables for all templates ::: #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
def vars_for_all_templates(self):

    # --- page number, page number in list, and list index
    # ---------------------------------------------------------------------------------------------------------------- #
    page = self.subsession.round_number
    return {
        'n':                Constants.n,
        'num_choices':      Constants.n * 2,
        'list_ordering':    self.participant.vars['list_ordering'],
        'x_list':           self.participant.vars['x_list'],
        'y_list':           self.participant.vars['y_list'],
    }



# #################################################################################################################### #
# ### CLASS GROUPING WAIT PAGE ### #
# #################################################################################################################### #
class GroupingWaitPage(WaitPage):
    # ----------------------------------------------------------------------------------------------------------------
    template_name = 'payment_weet_coopetition/GroupingWaitPage.html'
    group_by_arrival_time = True

    # set payoff after both players arrive
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def vars_for_template(self):
        self.player.final_payment = float(self.participant.payoff_plus_participation_fee())
        self.player.bonus = self.player.final_payment - float(self.session.config['participation_fee'])
        if ('workerid' in self.participant.vars):
            self.player.workerid = self.participant.vars['workerid']
        self.player.matched = self.participant.vars['matched']

        if 'coopetition_payoff' in self.participant.vars:
            coopetition_payoff = self.participant.vars['coopetition_payoff']
        else:
            coopetition_payoff = 0

        coopetition_payment = int(float(coopetition_payoff)*self.session.config['real_world_currency_per_point']*100)/100

        print(self.participant.vars)
        return {
            'qualified': self.participant.vars['qualified'],
            'matched': self.participant.vars['matched'],
            'coopetition_payoff': coopetition_payoff,
            'coopetition_payment': coopetition_payment,
            'participation_fee': self.session.config['participation_fee'],
            'quiz_bonus': self.session.config['quiz_bonus'],
            'final_payment': self.participant.payoff_plus_participation_fee(),
        }

# #################################################################################################################### #
# ### CLASS RESULTS ### #
# #################################################################################################################### #
class Results(Page):
    timeout_seconds = 120
    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):
        row_to_pay = self.participant.vars['row_to_pay']
        print(row_to_pay)
        decision_to_pay = row_to_pay[5]
        p1_payoff = row_to_pay[1] if decision_to_pay == 'L' else row_to_pay[3]
        p2_payoff = row_to_pay[2] if decision_to_pay == 'L' else row_to_pay[4]

        return {
            # 'p1_payoff':        p1_payoff,
            # 'p2_payoff':        p2_payoff,
            'p1_payoffL':       c(row_to_pay[1]),
            'p2_payoffL':       c(row_to_pay[2]),
            'p1_payoffR':       c(row_to_pay[3]),
            'p2_payoffR':       c(row_to_pay[4]),
            'id_to_pay':        row_to_pay[6],
            'id_in_group':      self.player.id_in_group,
            'decision':  decision_to_pay,
        }


class EndInfo(Page):
    def vars_for_template(self):
        eet_payoff = self.participant.vars['eet_payoff']

        self.player.final_payment = float(self.participant.payoff_plus_participation_fee())

        self.player.bonus = self.player.final_payment - float(self.session.config['participation_fee'])

        self.player.matched = self.participant.vars['matched']

        if 'coopetition_payoff' in self.participant.vars:
            coopetition_payoff = self.participant.vars['coopetition_payoff']
        else:
            coopetition_payoff = 0

        coopetition_payment = int(float(coopetition_payoff)*self.session.config['real_world_currency_per_point']*100)/100
        eet_payment = int(float(eet_payoff)*self.session.config['real_world_currency_per_point']*100)/100

        print(self.participant.vars)
        return {
            'qualified': self.participant.vars['qualified'],
            'matched': self.participant.vars['matched'],
            'coopetition_payoff': coopetition_payoff,
            'coopetition_payment': coopetition_payment,
            'eet_payment': eet_payment,
            'participation_fee': self.session.config['participation_fee'],
            'quiz_bonus': self.session.config['quiz_bonus'],
            'final_payment': self.participant.payoff_plus_participation_fee(),
        }


# #################################################################################################################### #
# ### PAGE SEQUENCE ### #
# #################################################################################################################### #
page_sequence = [
    GroupingWaitPage,
    Results,
    EndInfo
]
