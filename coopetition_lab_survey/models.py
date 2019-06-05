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
    name_in_url = 'coopetition_lab_survey'
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
    # {
    #     'page_title': 'Survey Questions',
    #     'survey_fields': [
    #         ('gender', {
    #             # 'text': 'What is your gender.',
    #             'text': '性别',
    #             'field': models.CharField(choices=GENDER_CHOICES),
    #         }),
    #         ('age', {   # field name (which will also end up in your "Player" class and hence in your output data)
    #             # 'text': 'What is your age?',   # survey question
    #             'text': '年龄',   # survey question
    #             'field': models.PositiveIntegerField(min=10, max=100),  # the same as in normal oTree model field definitions
    #         }),
    #         ('difficulty',
    #          {
    #              'text': '你认为实验信息容易理解吗?',
    #              # 'text': 'Do you consider the experiment easy to understand and follow?',
    #              'field': models.PositiveIntegerField(
    #                  choices=[
    #                      # [1, '1. Very easy'],
    #                      # [2, '2. Easy'],
    #                      # [3, '3. Moderate'],
    #                      # [4, '4. Difficult'],
    #                      # [5, '5. Very difficult']
    #                      [1, '1. 非常容易'],
    #                      [2, '2. 容易'],
    #                      [3, '3. 一般'],
    #                      [4, '4. 困难'],
    #                      [5, '5. 非常困难']
    #                  ]),
    #          }),
    #         ('satisfaction',
    #          {
    #              # 'text': 'How satisfied are you with the outcome and your earnings in the experiment?',
    #              'text': '你对实验结果还满意么?',
    #              'field': models.PositiveIntegerField(
    #                  choices=[
    #                      [1, '1. 非常不满意'],
    #                      [2, '2. 不满意'],
    #                      [3, '3. 一般'],
    #                      [4, '4. 满意'],
    #                      [5, '5. 非常满意']
    #                      # [1, '1. Very unsatisfied'],
    #                      # [2, '2. Unsatisfied'],
    #                      # [3, '3. Neutral'],
    #                      # [4, '4. Satisfied'],
    #                      # [5, '5. Very satisfied']
    #                  ]),
    #          }),
    #         ('participate_again',
    #          {
    #              # 'text': 'Would you like to participate in similar experiments in the future?',
    #              'text': '你是否有兴趣以后参加类似的实验?',
    #              'field': models.IntegerField(
    #                  choices=[
    #                      [1, '1. 非常感兴趣'],
    #                      [2, '2. 感兴趣'],
    #                      [3, '3. 一般'],
    #                      [4, '4. 不感兴趣'],
    #                      [5, '5. 非常不感兴趣']
    #                  ]),
    #          }),
    #         ('strategies',
    #          {
    #              'text': 'What strategy did you use for the experiment? Does it change from Part 1 to Part 2?',
    #              'field': models.TextField(blank=True),
    #          }),
    #         ('experiment_comments', {  # field name (which will also end up in your "Player" class and hence in your output data)
    #             'text': 'Any comments about the experiment? (What you like/dislike about the experiment? Which part is hard to follow?)',
    #             'field': models.TextField(blank=True),
    #         }),
    #
    #     ]
    # },

    {
        'page_title': '',
        'survey_fields': [
            ('gender', {
                'text': '性别',
                'field':
                    models.IntegerField(choices=[
                                              [1, '男'],
                                              [0, '女'],
                     ]),
            }),
            ('age', {   # field name (which will also end up in your "Player" class and hence in your output data)
                'text': '年龄',   # survey question
                'field': models.PositiveIntegerField(min=10, max=100),  # the same as in normal oTree model field definitions
            }),
            ('difficulty',
             {
                 'text': '你认为实验信息容易理解吗?',
                 'field': models.PositiveIntegerField(
                     choices=[
                                              [1, '1. 非常容易'],
                                              [2, '2. 容易'],
                                              [3, '3. 一般'],
                                              [4, '4. 困难'],
                                              [5, '5. 非常困难']
                     ]),
             }),
            ('participate_again',
             {
                 'text': '你是否有兴趣以后参加类似的实验?',
                 'field': models.IntegerField(
                     choices=[
                                              [1, '1. 不感兴趣'],
                                              [2, '2. 一般'],
                                              [3, '3. 感兴趣'],
                     ]),
             }),
            ('strategies',
             {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': '你在实验当中采用的是什么策略？',
                 'field': models.TextField(blank=True),
             }),
            ('experiment_comments', {  # field name (which will also end up in your "Player" class and hence in your output data)
                'text': '你对本实验有什么意见或建议',
                'field': models.TextField(blank=True),
            }),
        ]
    },
)

# now dynamically create the Player class from the survey definitions
Player = create_player_model_for_survey('survey_online.models', SURVEY_DEFINITIONS)
