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
                    'question': '[True/False] 你和你的对手投入越多的资源投入到投资账户，你们的合作总收益就会越高。',
                    # 'question': 'The more you and the other participant invest in the Investment Account, the higher the total return.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] 你投入越多的资源到分配账户，你所获得的合作总收益的份额就越高。',
                    # 'question': '[True/False] The more you invest in the Rationing Account, the higher share you can obtain from the total return of the Investment Account',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '每期开始时，你和你的对手各自获得10份资源. 如果你投入10份资源到投资账户(\(x_1=10, y_1=0\))而你的对手将10份资源个人保留(\(x_2=0, y_2=0\)). 你们的合作总收益是多少?',
                    # 'question': 'At the start of a round, you and the other participant each receive 10 points. Suppose you put 10 points in the Investment Account, while the other keeps these 10 points for himself (\(x_1=10, y_1=0\) and \(x_2=0, y_2=0\)). What is the total return from the Investment Account?',
                    'options': ['0','10','20','100'],
                    'correct': '0',
                },
                {
                    'question': '每期开始时，你和你的对手各自获得10份资源. 如果你和你的对手都投入10份资源到投资账户(\(x_1=x_2=10, y_1=y_2=0\)), 你们的合作总收益是多少?',
                    # 'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put all the 10 points in the Investment Account (\(x_1=x_2=10\)). What is the total return from the Investment Account?",
                    'options': ['10','20','100','160'],
                    'correct': '100',
                },
                {
                    'question': '每期开始时，你和你的对手各自获得10份资源. 如果你和你的对手都投入5份资源到投资账户(\(x_1=x_2=5\)), 你们的合作总收益是多少?',
                    # 'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put 5 points in the Investment Account (\(x_1=x_2=5\)). What is the total return from the Investment Account?",
                    'options': ['5','10','25','50'],
                    'correct': '25',
                },
                {
                    'question': '如果你投入3份资源到分配账户(\(y_1 = 3\)), 而你的对手投入2份资源到分配账户(\(y_2 = 2\))。你获得的合作总收益的份额是多少?',
                    # 'question': "Suppose you put 3 points in the Rationing Account (\(y_1 = 3\)), and the other participant put 2 points in the Rationing Account (\(y_2 = 2\)). What is your share of the total return from the Investment Account? ",
                    'options': ['0.4','0.5','0.6','1'],
                    'correct': '0.6',
                },
            ]

        elif self.session.config['treatment'] == 'Det60_0':
            questions = [
                {
                    'question': '[True/False] 你和你的对手投入越多的资源投入到投资账户，你们的合作总收益就会越高。',
                    # 'question': '[True/False] The more you and the other participant invest in the Investment Account, the higher the total return.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] 你投入越多的资源到分配账户，你所获得的合作总收益的份额就越高。',
                    # 'question': '[True/False] The more you invest in the Rationing Account, the higher share you can obtain from the total return of the Investment Account',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '每期开始时，你和你的对手各自获得10份资源. 如果你投入10份资源到投资账户(\(x_1=10, y_1=0\))而你的对手将10份资源个人保留(\(x_2=0, y_2=0\)). 你们的合作总收益是多少?',
                    # 'question': 'At the start of a round, you and the other participant each receive 10 points. Suppose you put 10 points in the Investment Account, while the other keeps these 10 points for himself (\(x_1=10, y_1=0\) and \(x_2=0, y_2=0\)). What is the total return from the Investment Account?',
                    'options': ['0','10','20','60'],
                    'correct': '60',
                },
                {
                    'question': '每期开始时，你和你的对手各自获得10份资源. 如果你和你的对手都投入10份资源到投资账户(\(x_1=x_2=10, y_1=y_2=0\)), 你们的合作总收益是多少?',
                    # 'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put all the 10 points in the Investment Account (\(x_1=x_2=10, y_1=y_2=0\)). What is the total return from the Investment Account?",
                    'options': ['10','20','100','160'],
                    'correct': '160',
                },
                {
                    'question': '每期开始时，你和你的对手各自获得10份资源. 如果你和你的对手都投入5份资源到投资账户(\(x_1=x_2=5\)), 你们的合作总收益是多少?',
                    # 'question': "At the start of a round, you and the other participant each receive 10 points. Suppose both of you put 5 points in the Investment Account (\(x_1=x_2=5\)). What is the total return from the Investment Account?",
                    'options': ['5','10','25','85'],
                    'correct': '85',
                },
                {
                    'question': '如果你投入3份资源到分配账户(\(y_1 = 3\)),，而你的对手投入2份资源到分配账户(\(y_2 = 2\))。你获得的合作总收益的份额是多少?',
                    # 'question': "Suppose you put 3 points in the Rationing Account  (\(y_1 = 3\)), and the other participant put 2 points in the Rationing Account (\(y_2 = 2\)). What is your share of the total return from the Investment Account? ",
                    'options': ['0.4','0.5','0.6','1'],
                    'correct': '0.6',
                },
            ]

        elif self.session.config['treatment'] == 'Asm0_60':
            questions = [
                {
                    'question': '[True/False] 每期开始时，玩家A拥有20份资源，玩家B拥有10份资源。',
                    # 'question': '[True/False] At the start of each round, Player A receives 20 points and Player B receives 10 points.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] 你和你的对手投入越多的资源投入到投资账户，你们的合作总收益就会越高。',
                    # 'question': '[True/False] The more you and the other participant invest in the Investment Account, the higher the total return.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] 你投入越多的资源到分配账户，你所获得的合作总收益的份额就越高。',
                    # 'question': '[True/False] The more you invest in the Rationing Account, the higher share you can obtain from the total return of the Investment Account',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '如果你和你的对手将全部资源都投入到投资账户(\(x_A=20, x_B=10, y_A=y_B=0\)), 你们的合作总收益是多少?',
                    # 'question': "Suppose both players put all points in the Investment Account (\(x_A=20, x_B=10, y_A=y_B=0\)). What is the total return from the Investment Account?",
                    'options': ['10', '20', '100', '150'],
                    'correct': '100',
                },
                {
                    'question': ' 如果你和你的对手都投入10份资源到投资账户(\(x_A=x_B=10\)), 你们的合作总收益是多少?',
                    # 'question': "Suppose both players put 10 points in the Investment Account (\(x_A=x_B=10\)). What is the total return from the Investment Account?",
                    'options': ['10', '20', '50', '100'],
                    'correct': '50',
                },
                {
                    'question': '如果你投入10份资源到投资账户而你的对手将投入0份资源到投资账户，你们的合作总收益是多少?',
                    # 'question': 'Suppose you put 10 points in the Investment Account, while the other put 0 point. What is the total return from the Investment Account?',
                    'options': ['0', '10', '20', '50'],
                    'correct': '0',
                },
                {
                    'question': '如果你投入3份资源到分配账户(\(y_1 = 3\)),，而你的对手投入2份资源到分配账户(\(y_2 = 2\))。你获得的合作总收益的份额是多少?',
                    # 'question': "Suppose you put 3 points in the Rationing Account, and the other participant put 2 points in the Rationing Account. What is your share of the total return from the Investment Account?",
                    'options': ['0.4','0.5','0.6','1'],
                    'correct': '0.6',
                },
            ]

        elif self.session.config['treatment'] == 'Asm60_0':
            questions = [
                {
                    'question': '[True/False] 每期开始时，玩家A拥有20份资源，玩家B拥有10份资源。',
                    # 'question': '[True/False] At the start of each round, Player A receives 20 points and Player B receives 10 points.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] 你和你的对手投入越多的资源投入到投资账户，你们的合作总收益就会越高。',
                    # 'question': '[True/False] The more you and the other participant invest in the Investment Account, the higher the total return.',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '[True/False] 你投入越多的资源到分配账户，你所获得的合作总收益的份额就越高。',
                    # 'question': '[True/False] The more you invest in the Rationing Account, the higher share you can obtain from the total return of the Investment Account',
                    'options': ['True', 'False'],
                    'correct': 'True',
                },
                {
                    'question': '如果你和你的对手将全部资源都投入到投资账户(\(x_A=20, x_B=10, y_A=y_B=0\)), 你们的合作总收益是多少?',
                    # 'question': "Suppose both players put all points in the Investment Account (\(x_A=20, x_B=10, y_A=y_B=0\)). What is the total return from the Investment Account?",
                    'options': ['10','20','100','160'],
                    'correct': '160',
                },
                {
                    'question': ' 如果你和你的对手都投入10份资源到投资账户(\(x_A=x_B=10\)), 你们的合作总收益是多少?',
                    # 'question': "Suppose both players put 10 points in the Investment Account (\(x_A=x_B=10\)). What is the total return from the Investment Account?",
                    'options': ['10','20','50','110'],
                    'correct': '110',
                },
                {
                    'question': '如果你投入10份资源到投资账户而你的对手将投入0份资源到投资账户，你们的合作总收益是多少?',
                    # 'question': 'Suppose you put 10 points in the Investment Account, while the other put 0 point. What is the total return from the Investment Account?',
                    'options': ['0','10','20','60'],
                    'correct': '60',
                },
                {
                    'question': '如果你投入3份资源到分配账户(\(y_1 = 3\)),，而你的对手投入2份资源到分配账户(\(y_2 = 2\))。你获得的合作总收益的份额是多少?',
                    # 'question': "Suppose you put 3 points in the Rationing Account, and the other participant put 2 points in the Rationing Account. What is your share of the total return from the Investment Account?",
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
