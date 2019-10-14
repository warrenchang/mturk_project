from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)



author = 'Huanren Zhang'

doc = """
Payment information for the session
"""



class Constants(BaseConstants):
    name_in_url = 'payment_inclass'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    participant_payoff = models.CurrencyField()



