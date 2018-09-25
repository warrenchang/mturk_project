from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Huanren Zhang'

doc = """
Coopetition game: trade-off between value co-creation and value appropriation
"""

def get_share(p1,p2):
    if p1==0 and p2 ==0:
        return 1/2
    else:
        return p1/(p1+p2)

class Constants(BaseConstants):
    name_in_url = 'coopetition_oneshot'
    instructions_template = 'coopetition_mturk/Summary_template.html'

    players_per_group = None

    A_values = [0,60]
    num_rounds = 1


class Subsession(BaseSubsession):

    def creating_session(self):
        # this is run before the start of every round
        for p in self.get_players(): # set interaction number and round number
            p.treatment = self.session.config['treatment']
            p.condition = p.treatment[:3]
            if p.treatment[3] == '0':
                p.A = Constants.A_values[0]
            else:
                p.A = Constants.A_values[1]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    condition = models.StringField()
    A = models.IntegerField()

    a1 = models.IntegerField(min=0, max=10)
    a2 = models.IntegerField(min=0, max=10)
    a3 = models.IntegerField(min=0, max=10)

