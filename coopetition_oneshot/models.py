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
    instructions_template = 'coopetition_mturk/Instructions_template.html'

    players_per_group = None

    A_values = [0,60]
    num_rounds = 1
    var_max = 105 ## maximal value for Var treatment


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
            if random.random() > 0.5:
                p.role = "A"
            else:
                p.role = "B"
            p.endowment = 10
            p.other_endowment = 10

            if p.condition == "Asm":
                if p.role == "A":
                    p.endowment = 20
                else:
                    p.other_endowment = 20


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    condition = models.StringField()
    A = models.IntegerField()

    endowment = models.IntegerField()
    other_endowment = models.IntegerField()
    role = models.StringField()

    a1 = models.IntegerField(min=0, max=20)
    a2 = models.IntegerField(min=0, max=20)
    a3 = models.IntegerField(min=0, max=20)

