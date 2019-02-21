from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Huanren Zhang'

doc = """
Questions that can be measures by a likert scale (1-7).
"""

GENDER_CHOICES = (
    ('female', 'Female'),
    ('male', 'Male'),
    # ('no_answer', 'Prefer not to answer'),
)

class Constants(BaseConstants):
    name_in_url = 'survey_likert'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players(): # set interaction number and round number
            if p.id_in_group%2 ==1:
                p.redwood_anchor = 400
                p.AUN_anchor = 10
            else:
                p.redwood_anchor = 50
                p.AUN_anchor = 65

            if p.id_in_group%3 ==1:
                p.receiver1 = "both"
            elif p.id_in_group%3 ==2:
                p.receiver1 = "dolphin"
            else:
                p.receiver1 = "farmer"


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    role = models.PositiveIntegerField()
    CRT1 = models.PositiveIntegerField(verbose_name= (
            "A bat and a ball cost DKK 110 in total. The bat costs DKK 100 more than the ball. "
            +"How much DKK does the ball cost?"))
    CRT2 = models.PositiveIntegerField(verbose_name= (
            "If it takes 5 machines 5 minutes to make 5 widgets, "+
            "how many minutes would it take 100 machines to make 100 widgets?"))
    CRT3 = models.PositiveIntegerField(verbose_name= (
        "In a lake, there is a patch of lily pads. Every day, the patch doubles in size. "
        +"If it takes 48 days for the patch to cover the entire lake, "
        +"how many days would it take for the patch to cover half of the lake?"))
    AUN_anchor = models.IntegerField(min=0, max=100)
    AUN_yes = models.BooleanField(widget=widgets.RadioSelectHorizontal)
    AUN = models.IntegerField(min=0, max=100)
    redwood_anchor = models.PositiveIntegerField()
    redwood_yes = models.BooleanField(widget=widgets.RadioSelectHorizontal)
    redwood = models.PositiveIntegerField()

    receiver1 = models.CharField()
    donation1 = models.IntegerField(min=0)
    donation2 = models.IntegerField(min=0)
