from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class MyPage(Page):
    timeout_seconds = 120


page_sequence = [
    MyPage,
]
