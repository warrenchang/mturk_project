from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Huanren Zhang'

doc = """
Quiz questions that test the understanding of PD with private monitoring and communication
"""


class Constants(BaseConstants):
    name_in_url = 'quiz'
    players_per_group = None
    num_rounds = 1

    summary_template = 'coopetition_quiz/Instructions_template.html'
    examples_template = 'coopetition_quiz/Examples_template.html'
    quiz_info = 'coopetition_quiz/QuizInfo.html'
    extra_info = 'coopetition_quiz/ExtraInfo.html'


class Subsession(BaseSubsession):
    def creating_session(self):
        # this is run before the start of every round
        # set the treatment variable
        treatment = self.session.config['treatment']

        for p in self.get_players(): # set interaction number and round number
            p.treatment = treatment
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
    condition = models.StringField()
    A = models.IntegerField()
