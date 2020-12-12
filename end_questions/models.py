from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from otreeutils.surveys import create_player_model_for_survey, generate_likert_field, generate_likert_table


author = 'Huanren Zhang'

doc = """
survey questions at the end of the experiment
"""


class Constants(BaseConstants):
    name_in_url = 'end_questions'
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
    # ('no_answer', 'Prefer not to answer'),
)

YESNO_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
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
        'page_title': '',
        'survey_fields': [
            # create a table of Likert scale choices
            # we use the same 5-point scale a before and specify four rows for the table,
            # each with a tuple (field name, label)
            ## Big-five (OCEAN: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
            generate_likert_table(likert_7_labels,
                                  [
                                      ('extraversion', "Extraverted, enthusiastic"),
                                      ('agreeablnessR', "Critical, quarrelsome"),
                                      ('conscientiousness', "Dependable, self-disciplined"),
                                      ('neuroticism', "Anxious, easily upset"),
                                      ('openness', "Open to new experiences, complex"),
                                      ('extraversionR', "Reserved, quiet"),
                                      ('agreeableness', "Sympathetic, warm"),
                                      ('conscientiousnessR', "Disorganized, careless"),
                                      ('neuroticismR', "Calm, emotionally stable"),
                                      ('opennessR', "Conventional, uncreative"),
                                  ],
                                  form_help_initial='<p>Below are a number of traits that may or may not apply to you.' +
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
        'page_title': 'Please answer the following questions',
        'survey_fields': [
            ('age', {  # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'What is your age?',  # survey question
                'field': models.PositiveIntegerField(min=16, max=100),
            # the same as in normal oTree model field definitions
            }),
            ('gender', {
                'text': 'Gender.',
                'field': models.CharField(widget = widgets.RadioSelect, choices=GENDER_CHOICES),
            }),
            ('education', {
                'text': 'Highest education level achieved?',
                'field': models.CharField(widget = widgets.RadioSelect,
                                          choices=('Less than a high school degree',
                                                   'High School',
                                                   'Colleage degree or equivalent',
                                                   'Graduate degree or equivalent')),
            }),
            ('income', {
                'text': 'The total amount of income you earn last year?',
                'field': models.CharField(
                    widget = widgets.RadioSelect,
                    choices=('Under $10,000',
                             '$10,000 to $25,000',
                             '$25,000 to $50,000',
                             '$50,000 to $100,000',
                             'Over $100,000'))
            }),
            ('financial', {
                'text': 'Do you have experience in financial markets (stocks, bonds, portfolios,ect.)?',
                'field': models.CharField(
                    widget=widgets.RadioSelect,
                    choices=('No experience',
                             'Very little experience',
                             'Some experience',
                             'A lot of experience',
                             ))
            }),
            ('relationship', {
                'text': 'What is your relationship status?',
                'field': models.CharField(widget = widgets.RadioSelect,
                                          choices=('Single',
                                                   'In a relationship',
                                                   'Married',
                                                   'Separated',
                                                   'Divorced',
                                                   'Widowed',),),
            }),
            # ('children', {
            #     'text': 'Do you have children?',
            #     'field': models.CharField(widget=widgets.RadioSelect,
            #                               choices=YESNO_CHOICES),
            # }),
        ]
    },
    {
        'page_title': '',
        'survey_fields': [
            ('nodeception', {
                'text': 'Unlike some other requesters on Mechanical turk, we do not use deception in our studies ' +
                        'For our own records, to what extent did you believe that the information presetned in the study is truthful?',
                'field': models.CharField(widget=widgets.RadioSelect,
                                          choices=('Very skeptical',
                                                   'Somewhat skeptical',
                                                   'Neutral',
                                                   'Somewhat confident',
                                                   'Very confident',), ),
            }),
            ('difficulty',
             {
                 'text': 'Do you consider the experiment easy to understand and follow?',
                 'field': models.PositiveIntegerField(widget=widgets.RadioSelect,
                     choices=[
                         [1, '1. Very easy'],
                         [2, '2. Easy'],
                         [3, '3. Moderate'],
                         [4, '4. Difficult'],
                         [5, '5. Very difficult']
                     ]),
             }),
            ('experiment_comments',
             {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'Any comments about the experiment? (What you like/dislike about the experiment? Which part is hard to follow? How can we improve)',
                 'field': models.TextField(blank=True),
             }),
            ('email',
             {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'You can leave your email address below if you want to be informed when future experiments become available',
                 'field': models.StringField(blank=True),
             }),
        ]
    },
)


# now dynamically create the Player class from the survey definitions
# we can also pass additional (non-survey) fields via `other_fields`
Player = create_player_model_for_survey('end_questions.models', SURVEY_DEFINITIONS,
            other_fields={})

