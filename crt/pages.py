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


class CRTInfo(Page):
    # timeout_seconds = 120

    def vars_for_template(self):
        return {
            'crt_payoff_per_question': self.session.config['crt_payoff_per_question']
        }


class SurveyPage1(SurveyPage):
    timeout_seconds = 90

    debug_fill_forms_randomly = True   # enable random data input if APPS_DEBUG is True


class SurveyPage2(SurveyPage):
    # timeout_seconds = 60
    debug_fill_forms_randomly = True   # enable random data input if APPS_DEBUG is True

    def vars_for_template(self):
        return {
            'crt_payoff_per_question': self.session.config['crt_payoff_per_question']
        }

    def before_next_page(self):
        player = self.player
        player.num_correct_anwers = ((player.crt1 == Constants.correct_answers[0])
                                 + (player.crt2 == Constants.correct_answers[1])
                                 + (player.crt3 == Constants.correct_answers[2]))
        if 'crt_payoff_per_question' in self.session.config:
            player.payoff = player.num_correct_anwers * self.session.config['crt_payoff_per_question']
        else:
            player.payoff = 0
        self.participant.vars['crt_payoff'] = player.payoff




# Create a list of survey pages.
# The order is important! The survey questions are taken in the same order
# from the SURVEY_DEFINITIONS in models.py

survey_pages = [
    SurveyPage1,
    SurveyPage2,
]

# Common setup for all pages (will set the questions per page)
setup_survey_pages(models.Player, survey_pages)

page_sequence = [
    # SurveyIntro,
]

# add the survey pages to the page sequence list
page_sequence.extend(survey_pages)
page_sequence.insert(0,CRTInfo) # insert CRTIntro before the second survey page