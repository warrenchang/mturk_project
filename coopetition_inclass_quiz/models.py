from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Huanren Zhang'

doc = """
Quiz questions that test the understanding of PD with private monitoring and communication
"""


class Constants(BaseConstants):
    name_in_url = 'inclass_quiz'
    players_per_group = None
    num_rounds = 1
    var_max = 110 ## maximal value for Var treatment

    summary_template = 'coopetition_inclass_quiz/Instructions_template.html'
    examples_template = 'coopetition_inclass_quiz/Examples_template.html'
    quiz_info = 'coopetition_inclass_quiz/QuizInfo.html'
    extra_info = 'coopetition_inclass_quiz/ExtraInfo.html'


class Subsession(BaseSubsession):
    def creating_session(self):
        # this is run before the start of every round
        # set the treatment variable
        treatment = self.session.config['treatment']
        language = self.session.config['language']

        for p in self.get_players(): # set interaction number and round number
            p.treatment = treatment
            p.language = language
            p.condition = p.treatment[:3]
            if p.treatment[3] == '0':
                p.A = 0
            else:
                p.A = 60



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    wrong_attempts = models.PositiveIntegerField()   # number of wrong attempts on understanding questions page
    treatment = models.StringField()
    language = models.StringField()
    condition = models.StringField()
    A = models.IntegerField()
    workerid  = models.StringField()
