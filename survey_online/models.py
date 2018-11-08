from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from otreeutils.surveys import create_player_model_for_survey

author = 'Huanren Zhang'

doc = """
Survey questions
"""


class Constants(BaseConstants):
    name_in_url = 'online_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


GENDER_CHOICES = (
    ('female', 'Female'),
    ('male', 'Male'),
    # ('no_answer', 'Prefer not to answer'),
)

YESNO_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
)


# define survey questions per page
# for each page define a page title and a list of questions
# the questions have a field name, a question text (input label), and a field type (model field class)
SURVEY_DEFINITIONS = (

    {
        'page_title': 'Survey Questions',
        'survey_fields': [
            ('gender', {
                'text': 'What is your gender.',
                'field': models.CharField(choices=GENDER_CHOICES),
            }),
            ('age', {   # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'What is your age?',   # survey question
                'field': models.PositiveIntegerField(min=10, max=100),  # the same as in normal oTree model field definitions
            }),
            ('difficulty',
             {
                 'text': 'Do you consider the experiment easy to understand and follow?',
                 'field': models.PositiveIntegerField(
                     choices=[
                         [1, '1. Very easy'],
                         [2, '2. Easy'],
                         [3, '3. Moderate'],
                         [4, '4. Difficult'],
                         [5, '5. Very difficult']
                     ]),
             }),
            ('satisfaction',
             {
                 'text': 'How satisfied are you with the outcome and your earnings in the experiment?',
                 'field': models.PositiveIntegerField(
                     choices=[
                         [1, '1. Very unsatisfied'],
                         [2, '2. Unsatisfied'],
                         [3, '3. Neutral'],
                         [4, '4. Satisfied'],
                         [5, '5. Very satisfied']
                     ]),
             }),
            ('participate_again',
             {
                 'text': 'Would you like to participate in similar experiments in the future?',
                 'field': models.IntegerField(
                     choices=[
                         [2, 'Yes'],
                         [1, 'Maybe'],
                         [0, 'No'],
                     ]),
             }),
            ('strategies',
             {
                 'text': 'What strategy did you use for the experiment? Does it change from Part 1 to Part 2?',
                 'field': models.TextField(blank=True),
             }),
            ('experiment_comments', {  # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'Any comments about the experiment? (What you like/dislike about the experiment? Which part is hard to follow?)',
                'field': models.TextField(blank=True),
            }),

        ]
    },
    #
    # {
    #     'page_title': 'Survey Questions',
    #     'survey_fields': [
    #         ('gender1', {
    #             'text': 'What is your gender.',
    #             'field': models.CharField(choices=GENDER_CHOICES),
    #         }),
    #         ('age1', {   # field name (which will also end up in your "Player" class and hence in your output data)
    #             'text': 'What is your age?',   # survey question
    #             'field': models.PositiveIntegerField(min=10, max=100),  # the same as in normal oTree model field definitions
    #         }),
    #         ('difficulty1',
    #          {
    #              'text': 'Do you consider the experiment easy to understand and follow?',
    #              'field': models.PositiveIntegerField(
    #                  choices=[
    #                      [1, '1. Very easy'],
    #                      [2, '2. Easy'],
    #                      [3, '3. Moderate'],
    #                      [4, '4. Difficult'],
    #                      [5, '5. Very difficult']
    #                  ]),
    #          }),
    #         ('participate_again1',
    #          {
    #              'text': 'Would you like to participate in similar experiments in the future?',
    #              'field': models.IntegerField(
    #                  choices=[
    #                      [2, 'Yes'],
    #                      [1, 'Maybe'],
    #                      [0, 'No'],
    #                  ]),
    #          }),
    #         ('experiment_comments1', {  # field name (which will also end up in your "Player" class and hence in your output data)
    #             'text': 'Any comments about the experiment? (What you like/dislike about the experiment? Which part is hard to follow?)',
    #             'field': models.TextField(blank=True),
    #         }),
    #
    #     ]
    # },

)

# now dynamically create the Player class from the survey definitions
Player = create_player_model_for_survey('survey_online.models', SURVEY_DEFINITIONS)
