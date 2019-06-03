from . import models
from ._builtin import Page
from .models import Constants
import random


class StartPage(Page):
    pass

class Page0(Page):
    form_model = 'player'
    form_fields = ['gender']
    def before_next_page(self):
        if self.timeout_happened:
            self.player.gender = random.choice(['male','female'])

page_sequence = [
    Page0,
    # Questions,
    # CFC,
    # OCEAN,
]
