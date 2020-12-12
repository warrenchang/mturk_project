from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


# #################################################################################################################### #
# ### CLASS CONSTANTS ### #
# #################################################################################################################### #
class Constants(BaseConstants):

    # ::: Test Parametrization ::: #
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #

    # e determines the locus of the equal-material-payoff allocation (m,o) = (e,e).
    # Note that option 'right' implies a payoff equal to e for both players in all binary decisions.
    e = 100

    # g is a 'gap' variable characterizing the vertical distance to (e,e).
    # The 'other' payoff in option 'left' is determined by (e+g) for the x-list and (e-g) for the y-list.
    # Note that g is restricted to be strictly smaller than e (to prevent negative payoffs).
    g = 30

    # s is a 'step size' variable characterizing the horizontal distance between two adjacent allocations.
    # That is, the 'my' payoff varies in steps of size s around the locus payoff e.
    s = 10

    # t is a 'test size' variable determining the number of steps (of size s) which are made to the left
    # and to the right starting from the point just above or below the equal-payoff allocation (m,o) = (e,e).
    # t is restricted to be an integer smaller or equal to g/s and must be larger or equal to 1.
    t = 2


    # ::: List Variations and Modifications of Parameterization ::: #
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #

    # <asymmetric_s = True> replaces the symmetric default step size between two adjacent decisions to increase
    # the power of the test to discriminate between selfish and different variants of non-selfish behavior.
    # Asymmetric step-sizes imply that step sizes are smaller at the centre but larger at the borders.
    # The specific functional form to determine asymmetric steps can be modified in <models.py:65>.
    asymmetric_s = True

    # <asymmetric_t = True> replaces the symmetric default test size specification by extending the x-list to the left
    # and the y-list to the right in order to examine whether subjects put more weight on the material payoff of the
    # passive person than on their own material payoff. <a = [int]> determines how many choices are added on each list.
    # Note that <asymmetric_t = True> implies that the number of choices per list increases from 2t + 1 to 2t + a + 1.
    asymmetric_t = False
    a = 1

    # ::: Role Assignment ::: #
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #

    # If <role_uncertain = True>, each player decides in the role of the active player.
    # Only after both players in a group have made their decisions it is randomly determined which
    # player's decisions are relevant for payout, i.e., who is the active and who the passive player.
    role_uncertain = True


    # ::: Overall Settings and Appearance ::: #
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #

    # randomly determine order of x- and y-lists if <counterbalance = True>
    counterbalance = False

    # If <one_page = True>, both the x- and y-list will be displayed on a single page.
    # If <one_page = False>, each of the two lists will be shown on a separate page.
    one_page = True


    # Enforce consistency, i.e., only allow for a single switching point per list (implemented using JavaScript).
    # If <enforce_consistency = True>, all options "Left" below a selected option "Left" are automatically selected.
    # Similarly, options "Right" above a selected option "Right" are automatically checked, implying consistent choices.
    # Note that <enforce_consistency> is only implemented if <one_choice_per_page = False> and <shuffle_lists = False>.
    enforce_consistency = True


    # ::: oTree Settings (modify only if custom features require it!) ::: #
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
    name_in_url = 'eet'
    players_per_group = None
    num_rounds = 1

    # set additional lists to zero if <asymmetric_t = False>
    if not asymmetric_t:
        a = 0

    # set number of items in x- and y-list
    n = 2 * t + a + 1

    # set number of rounds
    if one_page:
        num_rounds = 1
    else:
        num_rounds = 2
