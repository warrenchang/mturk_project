from . import models
from ._builtin import Page
from .models import Constants
import random


class StartPage(Page):
    pass


class CRT(Page):
    form_model = 'player'
    form_fields = ['CRT{}'.format(i) for i in range(1, 4)]
    def before_next_page(self):
        if self.timeout_happened:
            self.player.Q1 = random.choice(range(1,8))
            self.player.Q2 = random.choice(range(1,8))
            self.player.Q3 = random.choice(range(1,8))

class AUN(Page):
    form_model = 'player'
    form_fields = ['AUN','AUN_yes']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.ACN = random.choice(range(1,8))

class redwood(Page):
    form_model = 'player'
    form_fields = ['redwood','redwood_yes']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.redwood = random.choice(range(1,8))

class donation_both(Page):
    form_model = 'player'
    form_fields = ['donation1','donation2']

    def is_displayed(self):
        return (self.player.receiver1 == "both")


class donation1(Page):
    form_model = 'player'
    form_fields = ['donation1']

    def is_displayed(self):
        return (self.player.receiver1 != "both")


class donation2(Page):
    form_model = 'player'
    form_fields = ['donation2']

    def is_displayed(self):
        return (self.player.receiver1 != "both")

class EndInfo(Page):
    pass



page_sequence = [
    # StartPage,
    donation1,
    donation2,
    donation_both,
    redwood,
    AUN,
    CRT,
    EndInfo,
]
