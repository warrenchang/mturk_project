from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from otreeutils.surveys import create_player_model_for_survey, generate_likert_field, generate_likert_table


author = 'Huanren Zhang'

doc = """
survey questions
"""


class Constants(BaseConstants):
    name_in_url = 'survey_questions'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


# some pre-defined choices

GENDER_CHOICES = (
    ('female', 'Female'),
    ('male', 'Male'),
    ('no_answer', 'Prefer not to answer'),
)

YESNO_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
)

EBAY_ITEMS_PER_WEEK = (
    ('<5', 'less than 5'),
    ('5-10', 'between 5 and 10'),
    ('>10', 'more than 10'),
)

# define a Likert 5-point scale with its labels

likert_5_labels = (
    'Strongly disagree',
    'Disagree',
    'Neither agree nor disagree',
    'Agree',
    'Strongly agree'
)

likert_7_labels = (
    'Strongly Disagree',
    'Moderately Disagree',
    'Slightly Disagree',
    'Neutral',
    'Slightly Agree',
    'Moderately Agree',
    'Strongly Agree'
)

likert_5point_field = generate_likert_field(likert_5_labels)
likert_7point_field = generate_likert_field(likert_7_labels)


# define survey questions per page
# for each page define a page title and a list of questions
# the questions have a field name, a question text (input label), and a field type (model field class)
SURVEY_DEFINITIONS = (
    {
        # 'page_title': 'Please finish the following questions.',
        'page_title': '',
        'survey_fields': [
            # create a table of Likert scale choices
            # we use the same 5-point scale a before and specify four rows for the table,
            # each with a tuple (field name, label)
            generate_likert_table(likert_7_labels,
                                  [
                                      ('cfc1', 'When I make a decision, I think about how it might affect me in the future.'),
                                      ('cfc2', 'I am willing to give up something that is beneficial today in order to benefit more from that in the future.'),
                                      ('ambiguity1', 'There is a right way and a wrong way to do almost everything.'),
                                      ('ambiguity2', 'Practically every problem has a solution.'),
                                      ('trust', 'I assume that people have only the best intensions.'),
                                      ('nr2', 'I am willing to punish someone who treats others unfairly, even if there may be costs.'),
                                      ('risk', ' I am willing to take risks.'),
                                      ('competition', 'I like to compete with others.'),
                                      ('math', ' I am good at math.'),
                                  ],
                                  form_help_initial='<p>Below are a number of descriptions that may or may not apply to you. ' +
                                                    'Please indicate the extent to which you agree or disagree with that statement ' +
                                                    'on a scale of 1 (strongly disagree) to 7 (strongly agree).</p>',
                                  # HTML to be placed on top of form
                                  form_help_final='<p></p>',  # HTML to be placed below form
                                  table_row_header_width_pct=50,
                                  # width of row header (first column) in percent. default: 25
                                  table_rows_randomize=True,  # randomize order of displayed rows
                                  ),
        ]
    },
    {
        'page_title': 'Please answer the following quesitons',
        'survey_fields': [  # you can also split questions into several forms for better CSS styling
            {
            # you need to provide a dict then. you can add more keys to the dict which are then available in the template
                'form_name': 'first_form',  # optional, can be used for CSS styling
                'fields': [
                    ('tp1', {
                        # 'text': 'A notebook and a pencil cost DKK 110 in total. The notebook costs DKK 100 more than the pencil. How much does the pencil cost in DKK?',
                        'text': 'Suppose you are offered an immediate payment of $80 or a delayed payment 30 days from now. How much would you need to be paid in 30 days in order to give up $80 immediately?' ,
                        'field': models.PositiveIntegerField(),
                    }),
                    ('tp2', {
                        'text': 'Suppose you are offered an immediate payment of $100 in 30 days or an even further delayed payment in 60 days. How much would you require to be paid in 60 days in order to give up $100 in 30 days?',
                        'field': models.PositiveIntegerField(),
                    }),
                ]
            },
        ]
    },
    {
        'page_title': '',
        'survey_fields': [
            # create a table of Likert scale choices
            # we use the same 5-point scale a before and specify four rows for the table,
            # each with a tuple (field name, label)
            generate_likert_table(likert_7_labels,
                                  [
                                      ('pr', 'When someone does me a favor I am willing to return it.'),
                                      ('nr1', ' If I am treated very unjustly, I will take revenge at the first occasion, even if there is a cost to do so.'),
                                      ('ambiguity4', 'I find it hard to make a choice when the outcome is uncertain.'),
                                      ('ambiguity3', 'I feel relieved when an ambiguous situation suddenly becomes clear.'),
                                      ('altruism', 'I am willing to give to good causes without expecting anything in return.'),
                                      ('fne', 'I am concerned with what other people think of me.'),
                                      ('friend', 'I have relatives or friends that I can count on to help whenver needed.'),
                                      ('smarter', 'Generally speaking, I am smarter than an average person.'),
                                      ('cfc3', 'I only act to satisfy immediate concerns, figuring that I will take care of future problems that may occur at a later date.'),
                                  ],
                                  form_help_initial='<p>Below are a number of descriptions that may or may not apply to you. ' +
                                                    'Please indicate the extent to which you agree or disagree with that statement ' +
                                                    'on a scale of 1 (strongly disagree) to 7 (strongly agree).</p>',  # HTML to be placed on top of form
                                  form_help_final='<p></p>',                    # HTML to be placed below form
                                  table_row_header_width_pct=50,                          # width of row header (first column) in percent. default: 25
                                  table_rows_randomize=True,                              # randomize order of displayed rows
            ),
        ]
    },
)

# now dynamically create the Player class from the survey definitions
# we can also pass additional (non-survey) fields via `other_fields`
Player = create_player_model_for_survey('survey_questions.models', SURVEY_DEFINITIONS, other_fields={
})

