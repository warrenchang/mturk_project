from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

from otreeutils.pages import AllGroupsWaitPage, ExtendedPage, UnderstandingQuestionsPage, APPS_DEBUG


class StartPage(Page):
    def is_displayed(self):
        if self.round_number == 1:
            print('This is the start of PD quiz')
        return self.round_number == 1 and (not self.session.config['debug'])

class StartPage1(Page):
    pass



class SomeUnderstandingQuestions(UnderstandingQuestionsPage):
    page_title = 'Quiz questions'
    quiz_info = Constants.quiz_info  # information before the quiz questions
    set_correct_answers = APPS_DEBUG    # this is the default setting
    # set_correct_answers = False  # do not fill out the correct answers in advance (this is for fast skipping through pages)
    form_model = 'player'
    form_field_n_wrong_attempts = 'wrong_attempts'

    def get_questions(self):
        questions = [
            {
                'question': 'If you choose X and the other participant chooses X, then your payoff is',
                'options': [9, 6, 5, 3, -1],
                'correct': 9,
            },
            {
                'question': "If you choose Y and the other participant choose X, then the other participant's payoff is",
                'options': [2,3,5,6,8],
                'correct': 2,
            },
            {
                'question': "If the other participant chooses Y, then you should also choose Y to avoid a negative payoff",
                'options': ['True', 'False'],
                'correct': 'True',
            },
            {
                'question': "If you choose X, then the other participant should choose Y to get a higher payoff",
                'options': ['True', 'False'],
                'correct': 'True',
            },
            {
                'question': "If the other participant choose X, then you should also choose X to get a higher payoff",
                'options': ['True', 'False'],
                'correct': 'True',
            },
        ]
        return questions


class QuizResults(Page):
    timeout_seconds = 10


page_sequence = [
    StartPage,
    StartPage1,
    SomeUnderstandingQuestions,
    QuizResults,
]
