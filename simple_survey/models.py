from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Huanren Zhang'

doc = """
very short questionnaire
"""


class Constants(BaseConstants):
    name_in_url = 'simple_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.StringField(choices=['Male','Female'],)
    rank_estimate = models.IntegerField(choices=[
        [1, '1 ~ 5'],
        [2, '6 ~ 10'],
        [3, '11 ~ 15'],
        [4, '16 ~ 20'],
        [5, '> 20'],]
    )
