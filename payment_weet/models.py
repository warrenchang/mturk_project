from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
Payment information combining the results of the Equality Equivalence Test (EET) 
"""


## I use "Payoff" to represent earnings in points; "Payment" to represent earnings in real currency


# #################################################################################################################### #
# ### CLASS CONSTANTS ### #
# #################################################################################################################### #
class Constants(BaseConstants):
    name_in_url = 'payment_weet'
    players_per_group = 2
    num_rounds = 1


# #################################################################################################################### #
# ### CLASS SUBSESSION ### #
# #################################################################################################################### #
class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            print(p.participant.vars)
        pass


# #################################################################################################################### #
# ### CLASS GROUP ### #
# #################################################################################################################### #
class Group(BaseGroup):
    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

        # row_to_pay: decision problem, p1_payoffL, p2_payoffL, p1_payoffR, p2_payoffR, choice, proposer's id
        p1.participant.vars['row_to_pay'].append(1)
        p2.participant.vars['row_to_pay'].append(2)

        # determine whose action is implemented
        id_to_pay = random.choice([1,2])

        # ... according to player 1's decision
        if id_to_pay == 1:
            p2.participant.vars['row_to_pay'] = p1.participant.vars['row_to_pay']
            p1.payoff = (p1.participant.vars['row_to_pay'][1] if p1.participant.vars['row_to_pay'][5] == 'L'
                         else p1.participant.vars['row_to_pay'][3])
            p2.payoff = (p2.participant.vars['row_to_pay'][2] if p2.participant.vars['row_to_pay'][5] == 'L'
                         else p2.participant.vars['row_to_pay'][4])
        if id_to_pay == 2:
            p1.participant.vars['row_to_pay'] = p2.participant.vars['row_to_pay']
            p1.payoff = (p1.participant.vars['row_to_pay'][2] if p1.participant.vars['row_to_pay'][5] == 'L'
                         else p1.participant.vars['row_to_pay'][4])
            p2.payoff = (p2.participant.vars['row_to_pay'][1] if p2.participant.vars['row_to_pay'][5] == 'L'
                         else p2.participant.vars['row_to_pay'][3])
        p1.participant.vars['eet_payoff'] = p1.payoff
        p2.participant.vars['eet_payoff'] = p2.payoff


# #################################################################################################################### #
# ### CLASS PLAYER ### #
# #################################################################################################################### #
class Player(BasePlayer):
    final_payment = models.FloatField()

    # the following are used for paying MTurk workers bonuses
    bonus = models.FloatField()
    workerid = models.StringField()

