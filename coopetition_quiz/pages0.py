from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

from otreeutils.pages import AllGroupsWaitPage, ExtendedPage, UnderstandingQuestionsPage, APPS_DEBUG
import math


class StartPage(Page):
    timeout_seconds = 300

    def is_displayed(self):
        if self.round_number == 1:
            print('This is the start of quiz')
        return self.round_number == 1 #and (not self.session.config['debug'])

    def vars_for_template(self):
        return {
            'exchange_rate': int(round(1/self.session.config['real_world_currency_per_point'])),
            'max_payment': self.session.config['max_payment'],
        }


class Instructions(Page):
    timeout_seconds = 300

    def is_displayed(self):
        if self.round_number == 1:
            print('This is the start of quiz')
        return self.round_number == 1 #and (not self.session.config['debug'])


class Examples(Page):
    timeout_seconds = 300

    def is_displayed(self):
        if self.round_number == 1:
            print('This is the start of quiz')
        return self.round_number == 1 #and (not self.session.config['debug'])


class SomeUnderstandingQuestions(UnderstandingQuestionsPage):
    page_title = ''
    # extra_template = ''
    extra_template = Constants.extra_info
    quiz_info = Constants.quiz_info
    set_correct_answers = APPS_DEBUG    # this is the default setting
    # set_correct_answers = False  # do not fill out the correct answers in advance (this is for fast skipping through pages)
    form_model = 'player'
    form_field_n_wrong_attempts = 'wrong_attempts'
    timeout_seconds = 480

    def get_questions(self):
        if self.session.config['treatment'] == 'Det0_60':
            questions = [
                {
                    'question': '[True/False] The more you and the other participant invest in the Investment Account, the higher the total return.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] The more you invest in the Rationing Account, the higher share you can obtain from the total return of the Investment Account',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': 'At the start of a round, you and the other participant each receive 10 points. Suppose you put 10 points in the Investment Account, while the other keeps these 10 points for himself (\(x_1=10, y_1=0\) and \(x_2=0, y_2=0\)). What is the total return from the Investment Account?',
                    'options': ['0','10','20','100'],
                    'correct': '0',
                },
                {
                    'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put all the 10 points in the Investment Account (\(x_1=x_2=10\)). What is the total return from the Investment Account?",
                    'options': ['10','20','100','160'],
                    'correct': '100',
                },
                {
                    'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put 5 points in the Investment Account (\(x_1=x_2=5\)). What is the total return from the Investment Account?",
                    'options': ['5','10','25','50'],
                    'correct': '25',
                },
                {
                    'question': "Suppose you put 3 points in the Rationing Account (\(y_1 = 3\)), and the other participant put 2 points in the Rationing Account (\(y_2 = 2\)). What is your share of the total return from the Investment Account? ",
                    'options': ['0.4','0.5','0.6','1'],
                    'correct': '0.6',
                },
            ]

        elif self.session.config['treatment'] == 'Det60_0':
            questions = [
                {
                    'question': '[True/False] The more you and the other participant invest in the Investment Account, the higher the total return.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] The more you invest in the Rationing Account, the higher share you can obtain from the total return of the Investment Account',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': 'At the start of a round, you and the other participant each receive 10 points. Suppose you put 10 points in the Investment Account, while the other keeps these 10 points for himself (\(x_1=10, y_1=0\) and \(x_2=0, y_2=0\)). What is the total return from the Investment Account?',
                    'options': ['0','10','20','60'],
                    'correct': '60',
                },
                {
                    'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put all the 10 points in the Investment Account (\(x_1=x_2=10, y_1=y_2=0\)). What is the total return from the Investment Account?",
                    'options': ['10','20','100','160'],
                    'correct': '160',
                },
                {
                    'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put 5 points in the Investment Account (\(x_1=x_2=5\)). What is the total return from the Investment Account?",
                    'options': ['5','10','25','85'],
                    'correct': '85',
                },
                {
                    'question': "Suppose you put 3 points in the Rationing Account  (\(y_1 = 3\)), and the other participant put 2 points in the Rationing Account (\(y_2 = 2\)). What is your share of the total return from the Investment Account? ",
                    'options': ['0.4','0.5','0.6','1'],
                    'correct': '0.6',
                },
            ]

        elif self.session.config['treatment'] == 'Asm0_60':
            questions = [
                {
                    'question': '[True/False] At the start of each round, Player A receives 20 points and Player B receives 10 points.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] The more you and the other participant invest in the Investment Account, the higher the total return.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] The more you invest in the Rationing Account, the higher share you can obtain from the total return of the Investment Account',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': "Suppose both players put all points in the Investment Account (\(x_A=20, x_B=10, y_A=y_B=0\)). What is the total return from the Investment Account?",
                    'options': ['10', '20', '100', '150'],
                    'correct': '100',
                },
                {
                    'question': "Suppose both players put 10 points in the Investment Account (\(x_A=x_B=10\)). What is the total return from the Investment Account?",
                    'options': ['10', '20', '50', '100'],
                    'correct': '50',
                },
                {
                    'question': 'Suppose you put 10 points in the Investment Account, while the other put 0 point. What is the total return from the Investment Account?',
                    'options': ['0', '10', '20', '50'],
                    'correct': '0',
                },
                {
                    'question': "Suppose you put 3 points in the Rationing Account, and the other participant put 2 points in the Rationing Account. What is your share of the total return from the Investment Account?",
                    'options': ['0.4','0.5','0.6','1'],
                    'correct': '0.6',
                },
            ]

        elif self.session.config['treatment'] == 'Asm60_0':
            questions = [
                {
                    'question': '[True/False] At the start of each round, Player A receives 20 points and Player B receives 10 points.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] The more you and the other participant invest in the Investment Account, the higher the total return.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] The more you invest in the Rationing Account, the higher share you can obtain from the total return of the Investment Account',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': "Suppose both players put all points in the Investment Account (\(x_A=20, x_B=10, y_A=y_B=0\)). What is the total return from the Investment Account?",
                    'options': ['10','20','100','160'],
                    'correct': '160',
                },
                {
                    'question': "Suppose both players put 10 points in the Investment Account (\(x_A=x_B=10\)). What is the total return from the Investment Account?",
                    'options': ['10','20','50','110'],
                    'correct': '110',
                },
                {
                    'question': 'Suppose you put 10 points in the Investment Account, while the other put 0 point. What is the total return from the Investment Account?',
                    'options': ['0','10','20','60'],
                    'correct': '60',
                },
                {
                    'question': "Suppose you put 3 points in the Rationing Account, and the other participant put 2 points in the Rationing Account. What is your share of the total return from the Investment Account?",
                    'options': ['0.4','0.5','0.6','1'],
                    'correct': '0.6',
                },
            ]

        elif self.session.config['treatment'] == 'Fix0_60':
            questions = [
                {
                    'question': '[True/False] The more you and the other participant invest in the Investment Account, the higher the total return if the investment is a success.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                # {
                #     'question': '[True/False] Whether the investment in a round is a success is determined by a random number generated by the computer. If the number is less than or equal to 100, the investment is a success. ',
                #     'options': ['True', 'False'],
                #     'correct': 'True',
                # },
                {
                    'question': '[True/False] The more you invest in the Rationing Account, the higher share you can obtain from the total return of the Investment Account',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] The investment is successful with probability 0.5.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': 'At the start of a round, you and the other participant each receive 10 points. Suppose you put 10 points in the Investment Account, while the other keeps these 10 points for himself (\(x_1=10, y_1=0\) and \(x_2=0, y_2=0\)). What is the total return from the Investment Account if the investment is successful?',
                    'options': ['0','10','20','100'],
                    'correct': '0',
                },
                {
                    'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put all the 10 points in the Investment Account (\(x_1=x_2=10, y_1=y_2=0\)). What is the total return from the Investment Account if the investment is a success?",
                    'options': ['10','20','100','200'],
                    'correct': '200',
                },
                {
                    'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put 5 points in the Investment Account (\(x_1=x_2=5\)). What is the total return from the Investment Account if the investment is a success?",
                    'options': ['5','10','25','50'],
                    'correct': '50',
                },
                {
                    'question': "Suppose you put 3 points in the Rationing Account  (\(y_1 = 3\)), and the other participant put 2 points in the Rationing Account (\(y_2 = 2\)). What is your share of the total return from the Investment Account? ",
                    'options': ['0.4','0.5','0.6','1'],
                    'correct': '0.6',
                },
            ]

        elif self.session.config['treatment'] == 'Fix60_0':
            questions = [
                {
                    'question': '[True/False] The more you and the other participant invest in the Investment Account, the higher the total return if the investment is a success.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                # {
                #     'question': '[True/False] Whether the investment in a round is a success is determined by a random number generated by the computer. If the number is less than or equal to 100, the investment is a success. ',
                #     'options': ['True', 'False'],
                #     'correct': 'True',
                # },
                {
                    'question': '[True/False] The more you invest in the Rationing Account, the higher share you can obtain from the total return of the Investment Account',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] The investment is successful with probability 0.5.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': 'At the start of a round, you and the other participant each receive 10 points. Suppose you put 10 points in the Investment Account, while the other keeps these 10 points for himself (\(x_1=10, y_1=0\) and \(x_2=0, y_2=0\)). What is the total return from the Investment Account if it is successful?',
                    'options': ['10','20','60','100'],
                    'correct': '60',
                },
                {
                    'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put all the 10 points in the Investment Account (\(x_1=x_2=10, y_1=y_2=0)\). What is the total return from the Investment Account if the investment is a success?",
                    'options': ['10','20','100','260'],
                    'correct': '260',
                },
                {
                    'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put 5 points in the Investment Account (\(x_1=x_2=5\)). What is the total return from the Investment Account if the investment is a success?",
                    'options': ['10','25','50','110'],
                    'correct': '110',
                },
                {
                    'question': "Suppose you put 3 points in the Rationing Account  (\(y_1 = 3\)), and the other participant put 2 points in the Rationing Account (\(y_2 = 2\)). What is your share of the total return from the Investment Account? ",
                    'options': ['0.4','0.5','0.6','1'],
                    'correct': '0.6',
                },
            ]

        elif self.session.config['treatment'] == 'Var0_60':

            questions = [
                {
                    'question': '[True/False] The more you and the other participant invest in the Investment Account, the more likely that the investment is a success.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] The more you invest in the Rationing Account, the higher share you can obtain from the total return of the Investment Account',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': "What is the total return of the investment if it is a success?",
                    'options': ['10', '20', '100', '110'],
                    'correct': '110',
                },
                # {
                #     'question': "What is the total return of the investment if it is a failure?",
                #     'options': ['0', '10', '20', '50'],
                #     'correct': '0',
                # },
                {
                    'question': 'At the start of a round, you and the other participant each receive 10 points. Suppose both of you keep these 10 points for yourselves (\(x_1=x_2=0, y_1=y_2=0)\). Your final earnings is',
                    'options': ['10','20','40','100'],
                    'correct': '10',
                },
                {
                    'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put all the 10 points in the Investment Account (\(x_1=x_2=10\)). In order for the investment to be a success, the random number must be NO greater than",
                    'options': ['10','20','100','200'],
                    'correct': '100',
                },

                {
                    'question': "Suppose you put 3 points in the Rationing Account  (\(y_1 = 3\)), and the other participant put 2 points in the Rationing Account (\(y_2 = 2\)). What is your share of the total return from the Investment Account? ",
                    'options': ['0.4','0.5','0.6','1'],
                    'correct': '0.6',
                },
            ]

        elif self.session.config['treatment'] == 'Var60_0':

            questions = [
                {
                    'question': '[True/False] The more you and the other participant invest in the Investment Account, the more likely that the investment is a success.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] The more you invest in the Rationing Account, the higher share you can obtain from the total return of the Investment Account',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': "What is the total return of the investment if it is a success?",
                    'options': ['10', '20', '100', '170'],
                    'correct': '170',
                },
                {
                    'question': 'At the start of a round, you and the other participant each receive 10 points. Suppose both of you keep these 10 points for yourselves (\(x_1=x_2=0, y_1=y_2=0\)). Your final earnings is',
                    'options': ['10','20','40','100'],
                    'correct': '40',
                },
                {
                    'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put all the 10 points in the Investment Account (\(x_1=x_2=10\)). In order for the investment to be a success, the random number must be NO greater than",
                    'options': ['10','20','100','200'],
                    'correct': '100',
                },
                {
                    'question': "Suppose you put 3 points in the Rationing Account (\(y_1 = 3\)), and the other participant put 2 points in the Rationing Account (\(y_2 = 2\)). What is your share of the total return from the Investment Account? ",
                    'options': ['0.4','0.5','0.6','1'],
                    'correct': '0.6',
                },
            ]

        return questions

    def before_next_page(self):
        ## the variable matched is used to determine whether the participant will play a one-shot game
        ## in case matching is not reached
        self.participant.vars['matched'] = False
        if self.timeout_happened:
            self.participant.vars['qualified'] = False
        else:
            self.participant.vars['qualified'] = self.player.wrong_attempts < 3


class QuizResults(Page):
    timeout_seconds = 30

    def vars_for_template(self):
        return {
            'qualified': self.participant.vars['qualified'],
            'max_payment': self.session.config['max_payment'],
        }

class WorkerID(Page):
    timeout_seconds = 60

    form_model = 'player'
    form_fields = ['workerid']

    def is_displayed(self):
        return self.participant.vars['qualified']

    def before_next_page(self):
        self.participant.vars['workerid'] = self.player.workerid


page_sequence = [
    StartPage,
    Instructions,
    Examples,
    SomeUnderstandingQuestions,
    QuizResults,
    WorkerID,
]
