from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Huanren Zhang'

doc = """
Lying game: number of switchings
"""


class Constants(BaseConstants):
    name_in_url = 'lying1'
    players_per_group = None
    num_rounds = 1

    payment_per_incidence = 5
    num_trials = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    outcome = models.IntegerField(min=0,max=10)

