from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from eet.config import *
import random


author = 'Felix Holzmeister & Rudolf Kerschbamer'

doc = """
This oTree application allows to implement the Equality Equivalence Test (EET) as proposed by Kerschbamer (2015)
with any arbitrary parametrization as well as treatment variations and different graphical representations.
"""


# ::: parametrization in config.py
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
e = Constants.e
g = Constants.g
s = Constants.s

t = Constants.t
a = Constants.a

n = Constants.n


# #################################################################################################################### #
# ### CLASS SUBSESSION ### #
# #################################################################################################################### #
class Subsession(BaseSubsession):

    # ::: list of x-list and y-list form fields ::: #
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
    def creating_session(self):
        if 'eet_scale' in self.session.config:
            scale = self.session.config['eet_scale']
        else:
            scale = 1
        # --- create lists of x and y form fields
        self.session.vars['x_fields'] = ['x_' + str(j) for j in range(1, n + 1)]
        self.session.vars['y_fields'] = ['y_' + str(j) for j in range(1, n + 1)]
        self.session.vars['xy_fields'] = self.session.vars['x_fields'] + self.session.vars['y_fields']

        # --- lists of active player's payoffs ('mp') in x- and y-list
        mp_x = mp_y = []
        # ... in case of symmetric test design
        if not Constants.asymmetric_s:
            mp_x = [(e + (j - t) * s)*scale for j in range(2 * t + 1)]
            mp_y = [(e + (j - t) * s)*scale for j in range(2 * t + 1)]

        # ... in case of asymmetric step sizes
        elif Constants.asymmetric_s:
            mp_x = [(e + sign(j - t) * s * t * ((2 ** abs(j - t) - 1) / (2 ** t - 1)))*scale for j in range(2 * t + 1)]
            mp_y = [(e + sign(j - t) * s * t * ((2 ** abs(j - t) - 1) / (2 ** t - 1)))*scale for j in range(2 * t + 1)]

        # ... in case of asymmetric test size
        if Constants.asymmetric_t:

            # ...in case of symmetric step sizes
            if not Constants.asymmetric_s:
                mp_x = [
                    [x[0] + (j - a) * s * g[i] / g[0] for j in range(a)] + mp_x[i]
                    for i, x in enumerate(mp_x)
                ]
                mp_y = [
                    mp_y[i] + [y[-1] + (j + 1) * s * g[i] / g[0] for j in range(a)]
                    for i, y in enumerate(mp_y)
                ]

            # ...in case of asymmetric step sizes
            elif Constants.asymmetric_s:
                mp_x = [
                    [x[0] - (x[1] - x[0]) * 2 * (2 ** (a - j) - 1) for j in range(a)] + mp_x[i]
                    for i, x in enumerate(mp_x)
                ]
                mp_y = [
                    mp_y[i] + [y[-1] + (y[-1] - y[-2]) * 2 * (2 ** (j + 1) - 1) for j in range(a)]
                    for i, y in enumerate(mp_y)
                ]

        # --- lists of inactive player's payoffs ('op') in x-list and y-list
        op_x = [(e + g)*scale for _ in range(0, n)]
        op_y = [(e - g)*scale for _ in range(0, n)]

        # --- list of equal material payoffs
        e_xy = [e*scale for _ in range(0, n)]

        # --- store payoff lists as globals for reference
        # ------------------------------------------------------------------------------------------------------------
        self.session.vars['mp_x'] = mp_x
        self.session.vars['mp_y'] = mp_y
        self.session.vars['op_x'] = op_x
        self.session.vars['op_y'] = op_y

        # --- print 'my'-payoffs of list(s) in console
        # ------------------------------------------------------------------------------------------------------------
        if self.round_number == 1:
            print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
            print('The settings in config.py imply the following "my"-payoffs in x- and y-list(s):')
            print('x-list:', mp_x)
            print('y-list:', mp_y)
            print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')

        # --- for each player ...
        for p in self.get_players():

            #  initiate lists for choices made in x- and y-list
            p.participant.vars['x_choices'] = [None for _ in range(0, n)]
            p.participant.vars['y_choices'] = [None for _ in range(0, n)]

            # zipped list of decision problems (x-list)
            p.participant.vars['x_list'] = [list(j) for j in zip(
                self.session.vars['x_fields'], mp_x, op_x, e_xy, e_xy)]

            # zipped list of decision problems (y-list)
            p.participant.vars['y_list'] = [list(j) for j in zip(
                self.session.vars['y_fields'], mp_y, op_y, e_xy, e_xy)]

            # randomly determine order of x- and y-lists if <counterbalance = True>
            p.participant.vars['list_ordering'] = random.choice(['xy', 'yx']) \
                if Constants.counterbalance else 'xy'

            # zipped list of all decisions depending on list ordering
            if p.participant.vars['list_ordering'] == 'xy':
                p.participant.vars['xy_list'] = p.participant.vars['x_list'] + p.participant.vars['y_list']
            elif p.participant.vars['list_ordering'] == 'yx':
                p.participant.vars['xy_list'] = p.participant.vars['y_list'] + p.participant.vars['x_list']


        # --- generate random switching point for PlayerBot in tests.py
        # ------------------------------------------------------------------------------------------------------------
        for p in self.session.get_participants():
            p.vars['bot_x_switching_point'] = [random.randint(0, n + 1) / 2 + random.randint(0, n + 1) / 2]
            p.vars['bot_y_switching_point'] = [random.randint(0, n + 1) / 2 + random.randint(0, n + 1) / 2]


# #################################################################################################################### #
# ### CLASS GROUP ### #
# #################################################################################################################### #
class Group(BaseGroup):
    pass


# #################################################################################################################### #
# ### CLASS PLAYER ### #
# #################################################################################################################### #
class Player(BasePlayer):

    # ::: add model fields to player class ::: #
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
    list = models.IntegerField()

    for j in range(1, n + 1):
        locals()['x_' + str(j)] = models.StringField(
            doc="binary choice problem #" + str(j) + " in x-list"
        )
    del j
    for j in range(1, n + 1):
        locals()['y_' + str(j)] = models.StringField(
            doc="binary choice problem #" + str(j) + " in y-list"
        )
    del j

    x_score = models.FloatField(
        doc="x-score: non-parametric index of distributional concerns in the domain of disadvantageous inequality"
    )
    y_score = models.FloatField(
        doc="y-score: non-parametric index of distributional concerns in the domain of advantageous inequality"
    )
    archetype = models.StringField(
        doc="archetype of distributional preferences as defined by Kerschbamer (2015)"
    )

    choice_to_pay = models.StringField()
    decision_to_pay = models.StringField()


    # ::: set row, choice, and decision to pay ::: #
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
    def set_choice_to_pay(self):

        # randomly determine which row to pay
        self.participant.vars['row_to_pay'] = random.choice(self.participant.vars['xy_list'])

        # set choice to pay
        self.choice_to_pay = self.participant.vars['row_to_pay'][0]

        # determine decision to pay
        decision_to_pay_in_all_rounds = [p.__getattribute__(self.choice_to_pay) for p in self.in_all_rounds()]
        self.decision_to_pay = [j for j in decision_to_pay_in_all_rounds if j is not None][0]
        self.participant.vars['row_to_pay'].append(self.decision_to_pay)


    # ::: determine (x,y)-score if lists have been answered consistently :::
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
    def xy_scores(self):
        # determine x-score
        print(self.participant.vars['x_choices'])
        u = t if not Constants.asymmetric_t else t + a

        xr_choices = sum([choice =='R' for choice in self.participant.vars['x_choices']])
        self.x_score = (u + 0.5) - xr_choices

        # determine y-score
        yr_choices = sum([choice =='R' for choice in self.participant.vars['y_choices']])
        self.y_score = yr_choices - (t + 0.5)


    # ::: set archetype of distributional preferences ::: #
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
    def archetypes(self):
        # if all choices are consistent...
        aid = 1
        aid += 3 if self.y_score == -0.5 or self.y_score == 0.5 else 0
        aid += 6 if self.y_score < -0.5 else 0
        aid += 1 if self.x_score == -0.5 or self.x_score == 0.5 else 0
        aid += 2 if self.x_score > 0.5 else 0

        self.archetype = archetypes[aid]


# ::: dictionary of archetypes
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
archetypes = {
    1: 'Inequality-Averse',
    2: 'Maximin',
    3: 'Altruistic',
    4: 'Envious',
    5: 'Selfish',
    6: 'Kiss-Up',
    7: 'Spiteful',
    8: 'Kick-Down',
    9: 'Equality-Averse'
}


# ::: define sign-function
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
