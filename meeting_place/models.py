from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Huanren Zhang'

doc = """
Choosing meeting place and time. A coordination game that illustrates Schelling's focal point.
"""

def lcs(S,T,word):
    """Find the longest common string after removing 'word'"""
    S = S.lower().replace('beijing','').strip()
    T = T.lower().replace('beijing','').strip()
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = ""
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    longest = c
                    lcs_set = S[i-c+1:i+1]
    return lcs_set


class Constants(BaseConstants):
    name_in_url = 'meeting'
    players_per_group = 2
    num_rounds = 1
    bonus = 2 # bonus is real money


class Subsession(BaseSubsession):
    def creating_session(self):
        # this is run before the start of every round
        self.group_randomly()


class Group(BaseGroup):
    def interact(self):
        p1,p2 = self.get_players()

        # first calculate payoff
        p1.other_time = p2.time
        p2.other_time = p1.time
        p1.other_place = p2.place
        p2.other_place = p1.place

        p1.correct_time = p1.time == p1.other_time
        p1.correct_place = p1.place == p1.other_place
        p1.payoff = (p1.correct_time and p1.correct_place)*Constants.bonus / self.session.config['real_world_currency_per_point']
        p2.payoff = p1.payoff
        p2.correct_place = p1.correct_place
        p2.correct_time = p1.correct_time


class Player(BasePlayer):
    time = models.StringField()
    place = models.StringField()
    other_time = models.StringField()
    other_place = models.StringField()
    correct_time= models.BooleanField()
    correct_place= models.BooleanField()

    def get_partner(self):
        return self.get_others_in_group()[0]

