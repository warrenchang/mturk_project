# Definition of views/pages for the survey.
# Please note: When using oTree 2.x, this file should be called "pages.py" instead of "views.py"
#

from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

from otreeutils.surveys import SurveyPage, setup_survey_pages


class SurveyIntro(Page):
    pass


# let's create the survey pages here
# unfortunately, it's not possible to create them dynamically



class SurveyPage1(SurveyPage):
    # timeout_seconds = 90

    debug_fill_forms_randomly = True   # enable random data input if APPS_DEBUG is True

    def is_displayed(self):
        return self.participant.vars['matched']


class SurveyPage2(SurveyPage):
    # timeout_seconds = 60
    debug_fill_forms_randomly = True   # enable random data input if APPS_DEBUG is True


class SurveyPage3(SurveyPage):
    # timeout_seconds = 300
    debug_fill_forms_randomly = True   # enable random data input if APPS_DEBUG is True


class SurveyPage4(SurveyPage):
    # timeout_seconds = 90

    debug_fill_forms_randomly = True   # enable random data input if APPS_DEBUG is True
# Create a list of survey pages.
# The order is important! The survey questions are taken in the same order
# from the SURVEY_DEFINITIONS in models.py

survey_pages = [
    SurveyPage1,
    SurveyPage2,
    SurveyPage3,
    SurveyPage4,
]

# Common setup for all pages (will set the questions per page)
setup_survey_pages(models.Player, survey_pages)

page_sequence = [
    # SurveyIntro,
]

# add the survey pages to the page sequence list
page_sequence.extend(survey_pages)
