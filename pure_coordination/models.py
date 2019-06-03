from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Huanren Zhang'

doc = """
Beauty contest as a coordination game: choose the most beautiful face.
"""


class Constants(BaseConstants):
    name_in_url = 'beauty'
    players_per_group = 2
    num_rounds = 2
    bonus = 2 # bonus is real money


class Subsession(BaseSubsession):
    def creating_session(self):
        # this is run before the start of every round
        self.group_randomly()


class Group(BaseGroup):
    def interact(self):
        p1,p2 = self.get_players()

        # first calculate payoff
        p1.other_choice = p2.choice
        p2.other_choice = p1.choice

        p1.potential_payoff = (p1.choice == p1.other_choice)*Constants.bonus / self.session.config['real_world_currency_per_point']
        p2.potential_payoff = p1.potential_payoff

        if self.round_number == Constants.num_rounds:
            p1.payoff = p1.potential_payoff
            p2.payoff = p2.potential_payoff


        # print((self.round_number,p1.payoff,p2.payoff))
        # print((p1.participant.id_in_session,p1.action,p1.payoff,p1.signal,p2.participant.id_in_session,p2.action,p2.payoff,p2.signal))


class Player(BasePlayer):
    choice = models.IntegerField(min=1,max=5)
    other_choice = models.IntegerField(min=1,max=5)
    potential_payoff = models.CurrencyField()

    def get_partner(self):
        return self.get_others_in_group()[0]

