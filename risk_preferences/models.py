from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Simply gamble choice for risk preference elicitation
"""


class Constants(BaseConstants):
    name_in_url = 'risk_preferences'
    players_per_group = None
    num_rounds = 1
    # outcomesA = [210,180,150,120,90,60,30]
    # outcomesB = [210,270,330,390,450,480,495]

    outcomesA = [ 168,144,120,96,72,48,24 ]
    outcomesB = [ 168,216,264,312,360,384,396]
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choice = models.PositiveIntegerField(choices=[1,2,3,4,5,6,7], widget=widgets.RadioSelectHorizontal())
    rand_number = models.PositiveIntegerField()
