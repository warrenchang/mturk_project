import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    APPS_DEBUG = False
else:
    APPS_DEBUG = True

# don't share this with anybody.
SECRET_KEY = 'xbsw&0b==_fg)5#4n)ckwgr1-na%c#z=pmt4+13yr!h-x&s=1p'


# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')
AUTH_LEVEL = 'DEMO'

ADMIN_USERNAME = environ.get('OTREE_ADMIN_USERNAME')
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')



# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

Qid_preferences = '3KVW4MB3P584GRBMDJDG682UC8SXJD' # Qualification ID of Preferences
Qid_coopetition = '355NDHMUE4408REV3XQ8DXPSH6SCF1'  # Qualification ID of Coopetition
Qid_coopetition_sandbox = '3KPASCSMA0FIAKFOHBY5SS3J0R98H3'
Qid_preferences_sandbox = '3F97VQZTZ52G8HM1KEZAOKL8XI1HUS'
Test_workerids = ['A2J47PTIYO03TZ','A38IOZBVC9FXFJ']



# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'AED '
REAL_WORLD_CURRENCY_CODE = 'RMB '
REAL_WORLD_CURRENCY_CODE = '$'
USE_POINTS = True
# POINTS_CUSTOM_NAME = '$'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2
POINTS_DECIMAL_PLACES = 0

# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [
    'otree',
    'otreeutils',
    'otree_mturk_utils',
]
EXTENSION_APPS  = [
    'otree_mturk_utils',
]

# SENTRY_DSN = ''
SENTRY_DSN = 'http://08e879c62c554e08b7b637e7172b5ba7:daa025e5010e414f98c785f2c04a74f9@sentry.otree.org/150'

DEMO_PAGE_INTRO_TEXT = ""

ROOMS = [
    {
        'name': '1',
        'display_name': 'Room 1',
        'participant_label_file': '_rooms/room1.txt',
    },
    {
        'name': '2',
        'display_name': 'Room 2',
        'participant_label_file': '_rooms/room2.txt',
    },
]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1 / 100,
    'participation_fee': 0,
    'debug': APPS_DEBUG,
    'doc': "",
}


SESSION_CONFIGS = [
    {
        'name': 'test',
        'display_name': "Testing Group Matching",
        'num_demo_participants': 4,
        'app_sequence': [
            'test_app0',
            'test_app'
        ],
    },
    {
        'name': 'survey_preference',
        'display_name': "Preference Elicitation Experiment",
        'num_demo_participants': 2,
        'participation_fee': 2,
        'avg_payment': 4,
        'max_payment': 6,
        'crt_payoff_per_question': 20,  # points for each correct answer
        'ravens_payoff_per_question': 10,  # points for each correct answer
        'real_world_currency_per_point': 1 / 100,
        'access_key_id' : AWS_ACCESS_KEY_ID,
        'secret_access_key': AWS_SECRET_ACCESS_KEY,
        'debug': False,
        'sandbox': False,
        'Qid': Qid_preferences,
        'Qid_sandbox': Qid_preferences_sandbox,
        'app_sequence': [
            'mturkid',  'survey_questions',
            'eet',
            'cem',
            'ambiguity_cem','ravens10',
            'crt','end_questions',
            'payment_preference','payment_weet'
            # 'lying1', # 'lying2', # 'lying3',
        ],
    },
    {
        'name': 'coopetition_mturk_asm0_60',
        'display_name': "Coopetition Asm0_60",
        'num_demo_participants': 4,
        'participation_fee': 1.2,
        'quiz_bonus': 0.6,
        'avg_payment': 4,
        'max_payment': 6,
        'real_world_currency_per_point': 1 / 250,
        'eet_scale': 2, # scaling of EET payoffs for saliency
        'access_key_id': AWS_ACCESS_KEY_ID,
        'secret_access_key': AWS_SECRET_ACCESS_KEY,
        'debug': False,
        'sandbox': False,
        'Qid': Qid_coopetition,
        'Qid2': Qid_preferences,
        'Qid_sandbox': Qid_coopetition_sandbox,
        'Qid2_sandbox': Qid_preferences_sandbox,
        'treatment': 'Asm0_60',
        'interaction_length': 15,
        'attempts_allowed': 8,  # how many attempts allowed for the subjects
        'quiz_time': 5,  # max time allowed for the quiz in mimutes
        # 'debug': False,
        'app_sequence': ['mturkid', 'survey_questions', 'eet', 'coopetition_quiz', 'coopetition_mturk',
                         'end_questions_coopetition', 'payment_coopetition','payment_weet_coopetition'
                         ],
    },
    {
        'name': 'coopetition_mturk_asm60_0',
        'display_name': "Coopetition Asm60_0",
        'num_demo_participants': 4,
        'participation_fee': 1.2,
        'quiz_bonus': 0.6,
        'avg_payment': 4,
        'max_payment': 6,
        'real_world_currency_per_point': 1 / 250,
        'eet_scale': 2, # scaling of EET payoffs for saliency
        'access_key_id': AWS_ACCESS_KEY_ID,
        'secret_access_key': AWS_SECRET_ACCESS_KEY,
        'debug': False,
        'sandbox': False,
        'Qid': Qid_coopetition,
        'Qid2': Qid_preferences,
        'Qid_sandbox': Qid_coopetition_sandbox,
        'Qid2_sandbox': Qid_preferences_sandbox,
        'treatment': 'Asm60_0',
        'interaction_length': 15,
        'attempts_allowed': 8,  # how many attempts allowed for the subjects
        'quiz_time': 8,  # max time allowed for the quiz in mimutes
        # 'debug': False,
        'app_sequence': ['mturkid', 'survey_questions', 'eet', 'coopetition_quiz', 'coopetition_mturk',
                         'end_questions_coopetition', 'payment_coopetition','payment_weet_coopetition'
                         ],
    },
    {
        'name': 'ambiguity',
        'display_name': "Urn Gamble",
        'num_demo_participants': 4,
        'participation_fee': 2,
        'avg_payment': 4,
        'eet_scale': 4,  # scaling of EET payoffs for saliency
        'crt_payoff_per_question': 20,  # points for each correct answer
        'ravens_payoff_per_question': 10,  # points for each correct answer
        'real_world_currency_per_point': 1 / 100,
        'debug': False,
        'sandbox': True,
        'app_sequence': [
            'survey_questions','cem','ambiguity_cem',
        ],
    },
    {
        'name': 'eet',
        'display_name': "Equality Equivalence Test",
        'num_demo_participants': 4,
        'participation_fee': 2,
        'avg_payment': 4,
        'eet_scale': 4, # scaling of EET payoffs for saliency
        'crt_payoff_per_question': 20,  # points for each correct answer
        'ravens_payoff_per_question': 10,  # points for each correct answer
        'real_world_currency_per_point': 1 / 100,
        'debug': True,
        'sandbox': True,
        'app_sequence': [
            'eet', 'payment_weet'
        ],
    },
    {
        'name': 'mturk_id',
        'display_name': "Input MTurk ID",
        'num_demo_participants': 4,
        'avg_payment': 4,
        'max_payment': 6,
        'participation_fee': 1.5,
        'debug': False,
        'sandbox': True,
        'access_key_id': AWS_ACCESS_KEY_ID,
        'secret_access_key': AWS_SECRET_ACCESS_KEY,
        'Qid': Qid_preferences,
        'Qid_sandbox': Qid_preferences_sandbox,
        # 'debug': False,
        'app_sequence': [
            'mturkid',  # remember to change qualified and matched in survey_online for real mturk experiment
        ],
    },
    {
        'name': 'coopetition_mturk_a2m0_60',
        'display_name': "Coopetition A2m0_60",
        'num_demo_participants': 4,
        'participation_fee': 1,
        'max_payment': 6,
        'real_world_currency_per_point': 1 / 280,
        'treatment': 'A2m0_60',
        'interaction_length': 15,
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk',
                         'end_questions', 'payment_coopetition'
                         ],
    },
    {
        'name': 'coopetition_mturk_a2m60_0',
        'display_name': "Coopetition A2m60_6",
        'num_demo_participants': 4,
        'participation_fee': 1,
        'max_payment': 6,
        'real_world_currency_per_point': 1 / 280,
        'treatment': 'A2m60_0',
        'interaction_length': 15,
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk',
                         'end_questions', 'payment_coopetition'
                         ],
    },
    {
        'name': 'coopetition_mturk_det0_60',
        'display_name': "Coopetition Det0_60",
        'num_demo_participants': 2,
        'participation_fee': 1,
        'max_payment': 6,
        'treatment' : 'Det0_60',
        'interaction_length': 15,
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk', 'coopetition_oneshot',
                         'end_questions', 'payment_coopetition'
                         ],
    },
    {
        'name': 'coopetition_mturk_det60_0',
        'display_name': "Coopetition Det60_0",
        'num_demo_participants': 2,
        'participation_fee': 1,
        'max_payment': 6,
        'treatment': 'Det60_0',
        'interaction_length': 15,
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk', 'coopetition_oneshot',
                         'end_questions', 'payment_coopetition'
                         ],
    },
    {
        'name': 'coopetition_mturk_fix60_0',
        'display_name': "Coopetition Fix60_0",
        'num_demo_participants': 4,
        'participation_fee': 1,
        'max_payment': 7,
        'treatment': 'Fix60_0',
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk', 'coopetition_oneshot',
                         'end_questions', 'payment_coopetition'
                         ],
    },
    {
        'name': 'coopetition_mturk_var0_60',
        'display_name': "Coopetition Var0_60",
        'num_demo_participants': 4,
        'participation_fee': 1,
        'max_payment': 7,
        'treatment': 'Var0_60',
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk', 'coopetition_oneshot',
                         'end_questions', 'payment_coopetition'
                         ],
    },
]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
