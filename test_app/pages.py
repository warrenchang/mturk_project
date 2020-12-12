from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class ResultsWaitPage(WaitPage):
    group_by_arrival_time = True



class Results(Page):
    pass


page_sequence = [
    ResultsWaitPage,
    Results
]
