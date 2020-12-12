from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from ambiguity_cem.config import *
import random
from random import randrange


author = 'Felix Holzmeister'

doc = """
Certainty equivalent method as proposed by Cohen et al. (1987) and Abdellaoui et al. (2011),
as well as variations thereof suggested by Bruner (2009) and Gächter et al. (2010).
"""

# ******************************************************************************************************************** #
# *** CLASS SUBSESSION
# ******************************************************************************************************************** #
class Subsession(BaseSubsession):
    # initiate lists before session starts in round 1
    # ----------------------------------------------------------------------------------------------------------------
    def creating_session(self):
        # setting random paying rounds
        if self.round_number == 1:
            if Constants.num_paying_rounds > 0:
                paying_rounds = []
                for i in range(Constants.num_sets):
                    paying_rounds += random.sample(range(i * Constants.num_rounds_in_set + 1,
                                                         i * Constants.num_rounds_in_set + Constants.num_rounds_in_set + 1),
                                                   Constants.num_paying_rounds)
                paying_rounds.sort()
                self.session.vars['ambiguity_paying_rounds'] = paying_rounds
            for p in self.get_players():
                p.participant.vars['ambiguity_payoff_info'] = []

        set_number = int((self.round_number-1)/Constants.num_rounds_in_set)+1
        round_in_set = (self.round_number-1)%Constants.num_rounds_in_set+1
        print(set_number,round_in_set)
        x = Constants.lottery_x[set_number-1][round_in_set-1]
        y = Constants.lottery_y[set_number-1][round_in_set-1]
        px = Constants.lottery_px[set_number-1][round_in_set-1]
        paying_round = self.round_number in self.session.vars['ambiguity_paying_rounds']

        # initializing players
        for p in self.get_players(): # set interaction number and round number
            # print((p.participant.id_in_session, p.interaction_number, p.round_in_interaction, p.treatment))
            p.round_in_set = round_in_set
            p.set_number = set_number
            p.paying_round = paying_round
            p.x = x
            p.y = y
            p.px = px
        # print('Session paying round',self.session.vars['paying_rounds'] )


# ******************************************************************************************************************** #
# *** CLASS GROUP
# ******************************************************************************************************************** #
class Group(BaseGroup):
    pass


# ******************************************************************************************************************** #
# *** CLASS PLAYER
# ******************************************************************************************************************** #
class Player(BasePlayer):

    # add model fields to class player
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    for j in range(1, Constants.num_choices + 1):
        locals()['choice_' + str(j)] = models.StringField()
    del j

    # prospect (x,px%; y, (100-px)%)
    x = models.IntegerField()
    y = models.IntegerField()
    px = models.IntegerField()
    set_number = models.PositiveIntegerField() # current set number
    round_in_set = models.PositiveIntegerField() # current round in set
    ball_color = models.StringField(choices=['Black','White'],
                                    widget=widgets.RadioSelectHorizontal,
                                    ) # current round in set
    guess_ball = models.IntegerField()

    paying_round = models.BooleanField() # whether the current round is payoff relevant
    # after which row the player switching to sure payoff (counting from 1 instead of 0)
    # 0 represents always choose sure payoff
    # num_choices + 1 represents never choose sure payoff
    switching_row = models.IntegerField()
    ce = models.FloatField()

    # set player's payoff
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_payoffs(self):
        if self.paying_round: # if the current round is payoff relevant
            # random draw to determine whether to pay the "high" or "low" outcome of the randomly picked lottery
            random_draw = random.randint(1, 100)

            index_to_pay = random.randint(1,Constants.num_choices)
            choice_to_pay = getattr(self, 'choice_'+str(index_to_pay))
            sure_payoff = Constants.sure_payoffs[self.set_number-1][self.round_in_set-1][index_to_pay-1]

            if choice_to_pay == 'A':
                if random_draw <= self.px:
                    self.payoff = Constants.endowment + self.x
                else:
                    self.payoff = Constants.endowment + self.y
            else:
                self.payoff = Constants.endowment + sure_payoff

            # set payment information as global variable
            # ------------------------------------------------------------------------------------------------------------
            self.participant.vars['ambiguity_payoff_info'].append([self.set_number, self.round_in_set,
                                                             self.x,self.px,self.y, sure_payoff, choice_to_pay, self.payoff])
            print(self.id_in_group, self.participant.vars['ambiguity_payoff_info'])

    # determine switching row
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_ce(self):
        sure_payoffs = Constants.sure_payoffs[self.set_number-1][self.round_in_set-1]
        choices = [int(getattr(self, 'choice_%d'%i) == 'B') for i in range(1,Constants.num_choices+1)]
        # choices = [getattr(self, 'choice_%d'%i) for i in range(1,Constants.num_choices+1)]
        choices.insert(0, 0)
        choices.append(1)

        for j in range(len(choices) - 1):
            if choices[j + 1] - choices[j] == 1:
                self.switching_row = j
                break

        if self.switching_row == 0:
            self.ce = sure_payoffs[0]
        elif self.switching_row == Constants.num_choices:
            self.ce = sure_payoffs[-1]
        else:
            self.ce = (sure_payoffs[j-1] + sure_payoffs[j])/2
        print(sure_payoffs,self.switching_row, self.ce)
