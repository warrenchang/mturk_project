from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Your name here'

doc = """
Simply gamble choice for risk preference elicitation
"""


class Constants(BaseConstants):
    name_in_url = 'russian_roulette'
    players_per_group = None
    num_rounds = 3
    bonus = 5000
    bullets = [ 1,4,6 ]


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players(): # set interaction number and round number
            p.bullets = Constants.bullets[self.round_number-1]
            p.bullets = Constants.bullets[p.round_number-1]
            p.price = int(random.random()*Constants.bonus)+1
            p.rand_number = random.random()



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choice = models.PositiveIntegerField(max=5000)
    price = models.PositiveIntegerField()
    rand_number = models.FloatField()
    bullets = models.IntegerField()
    ## it may be helpful to define treatment variable, making it easier for data analysis later
