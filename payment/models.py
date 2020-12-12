from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random



author = 'Huanren Zhang'

doc = """
Payment information for the preference elicitation 
"""



class Constants(BaseConstants):
    name_in_url = 'payment_preference'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    final_payment = models.FloatField()

    # the following are used for paying MTurk workers bonuses
    bonus  = models.FloatField()
    workerid  = models.StringField()



