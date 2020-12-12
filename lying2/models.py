from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Huanren Zhang'

doc = """
Lying game: guess number
"""


class Constants(BaseConstants):
    name_in_url = 'lying2'
    players_per_group = None
    num_rounds = 1

    guess_bonus = 40
    deduction = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    outcome = models.IntegerField(min=1,max=100)

