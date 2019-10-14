from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Huanren Zhang'

doc = """
Instructions on how to read payoff matrices, with quiz questions testing understanding.
"""


class Constants(BaseConstants):
    name_in_url = 'payoff_matrix_quiz'
    quiz_info = 'payoff_matrix_quiz/QuizInfo.html'    # information before the quiz questions
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    wrong_attempts = models.PositiveIntegerField()   # number of wrong attempts on understanding questions page
