from . import models
from ._builtin import Page
from .models import Constants
import random


class StartPage(Page):
    pass

class Page0(Page):
    form_model = 'player'
    form_fields = ['gender', 'rank_estimate']
    def before_next_page(self):
        if self.timeout_happened:
            self.player.gender = random.choice(['male','female'])
            self.player.rank_estimate = random.choice([1,2,3,4,5])

page_sequence = [
    Page0,
    # Questions,
    # CFC,
    # OCEAN,
]
