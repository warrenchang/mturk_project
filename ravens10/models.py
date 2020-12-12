from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Huanren Zhang'

doc = """
Raven's progressive matrices test measuring cognitive ability
"""


class Constants(BaseConstants):
    name_in_url = 'ravens10'
    players_per_group = None
    answer_keys = [1, 6, 5, 1, 5, 2, 5, 6, 7, 8]
    num_rounds = len(answer_keys)
    minutes_given = int(num_rounds/2)
    instructions_template = 'ravens10/Instructions.html'


class Subsession(BaseSubsession):
    def creating_session(self):
        # this is run before the start of every round
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['ravens_payoff'] = 0
            if not('ravens_payoff_per_question' in self.session.config):
                self.session.config['ravens_payoff_per_question'] = 0


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    answer = models.IntegerField(choices=[1,2,3,4,5,6,7,8],widget = widgets.RadioSelectHorizontal)
    ans_correct = models.BooleanField()
    belief1 = models.IntegerField(min=0,max=Constants.num_rounds)
    belief2 = models.IntegerField(min=0,max=100)

