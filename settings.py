import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
    APPS_DEBUG = False
else:
    DEBUG = True
    APPS_DEBUG = True

# DEBUG = False
# APPS_DEBUG = False

# don't share this with anybody.
SECRET_KEY = 'xbsw&0b==_fg)5#4n)ckwgr1-na%c#z=pmt4+13yr!h-x&s=1p'


DATABASES = {
    'default': dj_database_url.config(
        # Rather than hardcoding the DB parameters here,
        # it's recommended to set the DATABASE_URL environment variable.
        # This will allow you to use SQLite locally, and postgres/mysql
        # on the server
        # Examples:
        # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
        # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME

        # fall back to SQLite if the DATABASE_URL env var is missing
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

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
AUTH_LEVEL = 'STUDY'

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
ADMIN_PASSWORD = 'econexperiment'


# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'AED '
REAL_WORLD_CURRENCY_CODE = 'RMB '
REAL_WORLD_CURRENCY_CODE = '$'
USE_POINTS = True
# POINTS_CUSTOM_NAME = 'tokens'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2
POINTS_DECIMAL_PLACES = 1

# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [
    'otree',
    'otreeutils',
    'otree_mturk_utils',
    # 'otree_tools',
]
EXTENSION_APPS  = [
    'otree_mturk_utils',
    # 'otree_tools',
]

# SENTRY_DSN = ''
SENTRY_DSN = 'http://08e879c62c554e08b7b637e7172b5ba7:daa025e5010e414f98c785f2c04a74f9@sentry.otree.org/150'

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            oTree on GitHub
        </a>.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Here are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish.
</p>
"""

ROOMS = [
    {
        'name': 'ssel_b_side',
        'display_name': 'SSEL B01 - B24',
        'participant_label_file': '_rooms/ssel_b_side.txt',
    },
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


# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['bonus', 'choice', 'study'],
    'title': 'experiment on decision-making',
    'description': 'interaction with other MTurk workers',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 1, # 7 days
    'grant_qualification_id': '38TZ8V8N0DM053SXV290O3KU9JSIPY',
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # { # to prevent retakes
        #     'QualificationTypeId': "YOUR_QUALIFICATION_ID_HERE",
        #     'Comparator': "DoesNotExist",
        # },
        { # to prevent retakes
            'QualificationTypeId': '38TZ8V8N0DM053SXV290O3KU9JSIPY',
            'Comparator': "DoesNotExist",
        },
        { #Worker_Locale
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}]
        },

        { # Worker_​NumberHITsApproved
            'QualificationTypeId': "00000000000000000040",
            'Comparator': "GreaterThan",
            'IntegerValues': [100]
        },
        { # Worker_​NumberHITsApproved
            'QualificationTypeId': "000000000000000000L0",
            'Comparator': "GreaterThan",
            'IntegerValues': [85]
        },
        # qualification.LocaleRequirement("EqualTo", "US"),
        # qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        # qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}

MTURK_NUM_PARTICIPANTS_MULTIPLE = 3


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1 / 300,
    'participation_fee': 0,
    'debug': DEBUG,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
        'name': 'coopetition_mturk_det0_60',
        'display_name': "Coopetition Det0_60",
        'num_demo_participants': 4,
        'participation_fee': 1,
        'max_payment': 6,
        'treatment' : 'Det0_60',
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk', 'coopetition_oneshot',
                         'survey_online','risk_preferences', 'payment_online'
                         ],
    },
    {
        'name': 'coopetition_mturk_det60_0',
        'display_name': "Coopetition Det60_0",
        'num_demo_participants': 4,
        'participation_fee': 1,
        'max_payment': 6,
        'treatment': 'Det60_0',
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk', 'coopetition_oneshot',
                         'survey_online','risk_preferences', 'payment_online'
                         ],
    },
    {
        'name': 'coopetition_mturk_fix0_60',
        'display_name': "Coopetition Fix0_60",
        'num_demo_participants': 4,
        'participation_fee': 1,
        'max_payment': 6,
        'treatment': 'Fix0_60',
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk', 'coopetition_oneshot',
                         'survey_online','risk_preferences', 'payment_online'
                         ],
    },
    {
        'name': 'coopetition_mturk_fix60_0',
        'display_name': "Coopetition Fix60_0",
        'num_demo_participants': 4,
        'participation_fee': 1,
        'max_payment': 6,
        'treatment': 'Fix60_0',
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk', 'coopetition_oneshot',
                         'survey_online','risk_preferences', 'payment_online'
                         ],
    },
    {
        'name': 'coopetition_mturk_var0_60',
        'display_name': "Coopetition Var0_60",
        'num_demo_participants': 4,
        'participation_fee': 1,
        'max_payment': 6,
        'treatment': 'Var0_60',
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk', 'coopetition_oneshot',
                         'survey_online','risk_preferences', 'payment_online'
                         ],
    },
    {
        'name': 'coopetition_mturk_var60_0',
        'display_name': "Coopetition Var60_0",
        'num_demo_participants': 4,
        'participation_fee': 1,
        'max_payment': 6,
        'treatment': 'Var60_0',
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk', 'coopetition_oneshot',
                         'survey_online','risk_preferences', 'payment_online'
                         ],
    },

    {
        'name': 'coopetition_mturk_asym0_60',
        'display_name': "Coopetition Asm0_60",
        'num_demo_participants': 4,
        'participation_fee': 1,
        'max_payment': 6,
        'treatment': 'Asm0_60',
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk', 'coopetition_oneshot',
                         'survey_online', 'payment_online'
                         ],
    },
    {
        'name': 'coopetition_mturk_asym60_0',
        'display_name': "Coopetition Asym60_0",
        'num_demo_participants': 4,
        'participation_fee': 1,
        'max_payment': 6,
        'treatment': 'Asm60_0',
        # 'debug': False,
        'app_sequence': ['coopetition_quiz', 'coopetition_mturk', 'coopetition_oneshot',
                         'survey_online', 'payment_online'
                         ],
    },

]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
