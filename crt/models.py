from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from otreeutils.surveys import create_player_model_for_survey, generate_likert_field, generate_likert_table


author = 'Huanren Zhang'

doc = """
Cognitive Reflection Test (CRT)
"""


class Constants(BaseConstants):
    name_in_url = 'crt'
    players_per_group = None
    num_rounds = 1
    correct_answers = [25,10,35]


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.participant.vars['crt_payoff'] = 0
        if not ('crt_payoff_per_question' in self.session.config):
            self.session.config['crt_payoff_per_question'] = 0


class Group(BaseGroup):
    pass


# define survey questions per page
# for each page define a page title and a list of questions
# the questions have a field name, a question text (input label), and a field type (model field class)
SURVEY_DEFINITIONS = (
    {
        'page_title': '',
        'form_help_initial': """
            <p>You have 90 seconds to answer the following questions and will be paid {{ crt_payment }} points for each correct answer.</p>""",
        'survey_fields': [   # you can also split questions into several forms for better CSS styling
            {                # you need to provide a dict then. you can add more keys to the dict which are then available in the template
                'form_name': 'first_form',   # optional, can be used for CSS styling
                'fields': [
                    ('crt1', {
                        # 'text': 'A notebook and a pencil cost DKK 110 in total. The notebook costs DKK 100 more than the pencil. How much does the pencil cost in DKK?',
                        'text': 'A monitor and a keyboard cost $350 in total. The monitor costs $300 more than the keyboard. How much does the keyboard cost?',
                        'field': models.PositiveIntegerField(),
                    }),
                    ('crt2', {
                        'text': 'It takes 10 computers 10 minutes to run 10 simulations. How many minutes does it take 200 computers to run 200 simulations?',
                        'field': models.PositiveIntegerField(),
                    }),
                    ('crt3', {
                        'text': 'There is a patch of lily pads in a pond. The patch doubles in size every day. If it takes 36 days for the patch to cover the entire pond, '
                                'how many days would it take to cover half the pond?',
                        'field': models.PositiveIntegerField(),
                    }),
                ]
            },
        ]
    },
    {
        'page_title': '',
        'survey_fields': [  # you can also split questions into several forms for better CSS styling
            {
            # you need to provide a dict then. you can add more keys to the dict which are then available in the template
                'form_name': 'first_form',  # optional, can be used for CSS styling
                'fields': [
                    ('crt_e1', {
                        # 'text': 'A notebook and a pencil cost DKK 110 in total. The notebook costs DKK 100 more than the pencil. How much does the pencil cost in DKK?',
                        'text': 'How many of the 3 questions do you think you solved correct?',
                        'field': models.IntegerField(min=0,max=3),
                    }),
                    ('crt_e2', {
                        'text': 'Out of 100 other randomly selected participants, how many do you thik solve more questions correctly than you?',
                        'field': models.IntegerField(min=0,max=100),
                    }),
                ]
            },
        ]
    },
)


# now dynamically create the Player class from the survey definitions
# we can also pass additional (non-survey) fields via `other_fields`
Player = create_player_model_for_survey('crt.models', SURVEY_DEFINITIONS,
            other_fields={'num_correct_anwers': models.IntegerField()})

