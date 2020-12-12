# <imports>
from otree.api import Currency as c
from otree.constants import BaseConstants
# import numpy as np
# </imports>


# ******************************************************************************************************************** #
# *** CLASS CONSTANTS *** #
# ******************************************************************************************************************** #
class Constants(BaseConstants):
    guess_bonus = 50
    deduction = guess_bonus/10
    # prospect (x,px%; y, (100-px)%) vs. sure_payoff
    lottery_x = [[100], [0]]
    lottery_y = [[0], [-30]]
    lottery_px = [[50], [50]]

    sure_payoffs = [  # sure payoffs for all sets of lotteries
        [[0, 22, 38, 46, 50, 54, 62, 78, 100],  # p =50%
         ],  # p =50%, mixed prospect
        [[-30, -23, -19, -17, -15, -13, -11, -7, 0],  # p =50%
         ]
        ]
    # <num_choices> determines how many choices between a lottery and a sure payoff shall be implemented
    num_choices = len(sure_payoffs[0][0])
    num_rounds = len([item for sublist in lottery_px for item in sublist])
    num_sets = len(lottery_px)
    num_rounds_in_set = len(lottery_px[0])
    # number of decision situations in each set that are payoff relevant
    num_paying_rounds = 1

    # initial endowment (in currency units set in settings.py)
    # <endowment> defines an additional endowment for the task to capture potential losses if <variation = lottery_lo>
    # if no additional endowment should be implemented, set <endowment> to 0
    endowment = 0

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Overall Settings and Appearance --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # enforce consistency, i.e. only allow for a single switching point
    # if <enforce_consistency = True>, all options "A" above a selected option "A" are automatically selected
    # similarly, all options "B" below a selected option "B" are automatically checked, implying consistent choices
    # note that <enforce_consistency> is only implemented if <one_choice_per_page = False> and <random_order = False>
    enforce_consistency = True

    # show instructions page
    # if <instructions = True>, a separate template "Instructions.html" is rendered prior to the task
    # if <instructions = False>, the task starts immediately (e.g. in case of printed instructions)
    instructions = True

    # show results page summarizing the task's outcome including payoff information
    # if <results = True>, a separate page containing all relevant information is displayed after finishing the task
    # if <results = False>, the template "Decision.html" will not be rendered
    results = True

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- oTree Settings (Don't Modify) --- #
    # ---------------------------------------------------------------------------------------------------------------- #
    name_in_url = 'ambiguity_cem'
    players_per_group = None


