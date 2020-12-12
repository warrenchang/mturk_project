from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from eet.config import *


# set number of pages per list
# --------------------------------------------------------------------------------------------------------------------
if Constants.one_page:
    pages_per_list = 1
else:
    pages_per_list = 2


# ::: variables for all templates ::: #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
def vars_for_all_templates(self):
    return {
        'n':                Constants.n,
        'num_choices':      Constants.n * 2,
        'list_ordering':    self.participant.vars['list_ordering'],
        'x_list':           self.participant.vars['x_list'],
        'y_list':           self.participant.vars['y_list'],
    }

# #################################################################################################################### #
# ### CLASS INSTRUCTIONS ### #
# #################################################################################################################### #
class Instructions(Page):
    # --- only display instructions in first round
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        return self.subsession.round_number == 1


# #################################################################################################################### #
# ### CLASS DECISION ### #
# #################################################################################################################### #
class Decision(Page):
    # form model
    form_model = 'player'

    # ::: form fields and variables for template if <one_page == True> ::: #
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
    if Constants.one_page:
        # --- form fields
        def get_form_fields(self):
            return self.session.vars['xy_fields']

        # --- variables for template
        def vars_for_template(self):
            return {
                'show_x':  True,
                'show_y':  True
            }
    # ::: form fields and variables for template if <one_page == False> ::: #
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
    else:
        # --- form fields
        def get_form_fields(self):

            # page number and page number in list
            page = self.subsession.round_number
            page_in_list = (page - 1) % pages_per_list + 1

            # list ordering
            list_ordering = self.participant.vars['list_ordering']

            # return form fields
            if page_in_list == 1 and list_ordering == 'xy':
                return self.session.vars['x_fields']
            if page_in_list == 1 and list_ordering == 'yx':
                return self.session.vars['y_fields']
            if page_in_list == 2 and list_ordering == 'xy':
                return self.session.vars['y_fields']
            if page_in_list == 2 and list_ordering == 'yx':
                return self.session.vars['x_fields']

        # --- variables for template
        def vars_for_template(self):

            # page number, page number in list, and list index
            page = self.subsession.round_number
            page_in_list = (page - 1) % pages_per_list + 1

            # list ordering
            list_ordering = self.participant.vars['list_ordering']

            # return which list to show
            if page_in_list == 1 and list_ordering == 'xy':
                return {
                    'show_x':   True,
                    'show_y':   False
                }
            if page_in_list == 1 and list_ordering == 'yx':
                return {
                    'show_x':   False,
                    'show_y':   True
                }
            if page_in_list == 2 and list_ordering == 'xy':
                return {
                    'show_x':   False,
                    'show_y':   True
                }
            if page_in_list == 2 and list_ordering == 'yx':
                return {
                    'show_x':   True,
                    'show_y':   False
                }

    # ::: determine consistency, switching row, (x,y)-scores, utility function parameters, and  archetypes ::: #
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
    def before_next_page(self):
        # ------------------------------------------------------------------------------------------------------------
        # set choices in x-list
        for j, choice in enumerate(self.session.vars['x_fields']):
            if self.participant.vars['x_choices'][j] is None:
                self.participant.vars['x_choices'][j] = getattr(self.player, choice)

        # set choices in y-list
        for j, choice in enumerate(self.session.vars['y_fields']):
            if self.participant.vars['y_choices'][j] is None:
                self.participant.vars['y_choices'][j] = getattr(self.player, choice)

        # --- after all decisions have been made ...
        # ------------------------------------------------------------------------------------------------------------
        if self.subsession.round_number == Constants.num_rounds:
            # set row, choice, and decision to pay
            self.player.set_choice_to_pay()
            # determine (x,y)-score
            self.player.xy_scores()
            # set archetype
            self.player.archetypes()

            print(self.player.id_in_group)
            print(self.participant.vars)




# #################################################################################################################### #
# ### PAGE SEQUENCE ### #
# #################################################################################################################### #
page_sequence = [
    Instructions,
    Decision,
]
