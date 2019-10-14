from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Huanren Zhang'

doc = """
A series of finitely repeated coordination games. One round in each game is randomly chosen for payment.
"""


class Constants(BaseConstants):
    name_in_url = 'repeated_game_randpay'
    instructions_template = 'repeated_game_randpay/Instructions.html'
    history_template = 'repeated_game_randpay/History.html'
    historyall_template = 'repeated_game_randpay/HistoryAllRounds.html'
    otherhistory_template = 'repeated_game_randpay/OtherHistory.html'

    # number of rounds in each interaction randomly selected for payments
    # set to non-positive number if all rounds are chosen for payments
    num_paying_rounds = 2

    players_per_group = 2

    interactions = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
        5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    ]
    round_in_interactions = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    ]

    interaction_length = [10, 10, 10, 10, 10]
    treatments = ['random', 'random', 'random', 'random', 'random']


    interactions = [
        1, 1, 1,
        2, 2, 2,
        3, 3, 3,
        4, 4, 4,
        5, 5, 5,
    ]
    round_in_interactions = [
        1, 2, 3,
        1, 2, 3,
        1, 2, 3,
        1, 2, 3,
        1, 2, 3,
    ]

    interaction_length = [3, 3, 3, 3, 3]

    num_rounds = sum(interaction_length) # change num_rounds for testing purpose, but need to make sure that number_sequence

    # payoff matrices for different rounds
    payoff_matrix = {
        1: {
            1: {
                'X':
                    {
                        'X': 10,
                        'Y': 0
                    },
                'Y':
                    {
                        'X': 7,
                        'Y': 7
                    },
            },
            2: {
                'X':
                    {
                        'X': 10,
                        'Y': 0
                    },
                'Y':
                    {
                        'X': 7,
                        'Y': 7
                    },
            },
        },
        2: {
            1: {
                'X':
                    {
                        'X': 12,
                        'Y': 2
                    },
                'Y':
                    {
                        'X': 9,
                        'Y': 9
                    },
            },
            2: {
                'X':
                    {
                        'X': 12,
                        'Y': 2
                    },
                'Y':
                    {
                        'X': 9,
                        'Y': 9
                    },
            },
        },
        3: {
            1: {
                'X':
                    {
                        'X': 8,
                        'Y': -2
                    },
                'Y':
                    {
                        'X': 5,
                        'Y': 5
                    },
            },
            2: {
                'X':
                    {
                        'X': 8,
                        'Y': -2
                    },
                'Y':
                    {
                        'X': 5,
                        'Y': 5
                    },
            },
        },
        4: {
            1: {
                'X':
                    {
                        'X': 10,
                        'Y': 0
                    },
                'Y':
                    {
                        'X': 7,
                        'Y': 7
                    },
            },
            2: {
                'X':
                    {
                        'X': 10,
                        'Y': 0
                    },
                'Y':
                    {
                        'X': 8,
                        'Y': 8
                    },
            },
        },
        5: {
            1: {
                'X':
                    {
                        'X': 11,
                        'Y': 0
                    },
                'Y':
                    {
                        'X': 7,
                        'Y': 7
                    },
            },
            2: {
                'X':
                    {
                        'X': 10,
                        'Y': 0
                    },
                'Y':
                    {
                        'X': 7,
                        'Y': 7
                    },
            },
        },
    }



class Subsession(BaseSubsession):

    def creating_session(self):
        # this is run before the start of every round
        round_in_interaction = Constants.round_in_interactions[self.round_number-1]
        interaction_number = Constants.interactions[self.round_number-1]
        treatment = Constants.treatments[interaction_number-1]

        # print((interaction_number,round_in_interaction,treatment))

        # setting random paying rounds
        if Constants.num_paying_rounds > 0:
            if round_in_interaction == 1:
                self.session.vars['paying_rounds'] = random.sample(
                    range(1,Constants.interaction_length[interaction_number-1]+1),
                    Constants.num_paying_rounds)

        for p in self.get_players(): # set interaction number and round number
            p.interaction_number = interaction_number
            p.round_in_interaction = round_in_interaction
            p.treatment = treatment
            p.paying_round = 1
            # print((p.participant.id_in_session, p.interaction_number, p.round_in_interaction, p.treatment))
            if Constants.num_paying_rounds > 0 and not (round_in_interaction in self.session.vars['paying_rounds']):
                p.paying_round = 0

        if round_in_interaction == 1: # at the start of each interaction, reshuffle group
            self.group_randomly()
        elif treatment != 'fixed':
            self.group_randomly()
        else:  # otherwise, group structure is the same as in the previous round
            self.group_like_round(self.round_number-1)

        # print('Session paying round',self.session.vars['paying_rounds'] )


class Group(BaseGroup):
    def interact(self):
        p1,p2 = self.get_players()
        p1.my_id = p1.participant.id_in_session
        p2.my_id = p2.participant.id_in_session
        p1.partner_id = p2.my_id
        p2.partner_id = p1.my_id

        # first calculate payoff
        p1.other_action = p2.action
        p2.other_action = p1.action
        p1.potential_payoff = (Constants.payoff_matrix[p1.interaction_number][p1.id_in_group][p1.action][p1.other_action])
        p2.potential_payoff = (Constants.payoff_matrix[p2.interaction_number][p2.id_in_group][p2.action][p2.other_action])
        p1.other_payoff = p2.potential_payoff
        p2.other_payoff = p1.potential_payoff

        if p1.paying_round == 1:
            p1.payoff = p1.potential_payoff
            p2.payoff = p2.potential_payoff

        # print((self.round_number,p1.payoff,p2.payoff))

        p1.cum_payoff = sum([p.payoff for p in p1.in_all_rounds()
                             if p.interaction_number == p1.interaction_number])
        p2.cum_payoff = sum([p.payoff for p in p2.in_all_rounds()
                             if p.interaction_number == p1.interaction_number])

        # update payoff for Part I in terms of real currency
        # p1.participant.vars['real_payoff_PartI'] = p1.cum_payoff * self.session.config['real_world_currency_per_point']
        # p2.participant.vars['real_payoff_PartI'] = p2.cum_payoff * self.session.config['real_world_currency_per_point']

        # print((p1.participant.id_in_session,p1.action,p1.payoff,p1.signal,p2.participant.id_in_session,p2.action,p2.payoff,p2.signal))


class Player(BasePlayer):
    my_id = models.PositiveIntegerField()
    interaction_number = models.PositiveIntegerField()
    round_in_interaction = models.PositiveIntegerField()
    paying_round = models.PositiveIntegerField()
    treatment = models.StringField()

    action = models.StringField(
        choices=['X', 'Y'],
        doc="""This player's action""",
        widget=widgets.RadioSelect()
    )
    potential_payoff = models.CurrencyField()
    cum_payoff = models.CurrencyField()

    partner_id = models.PositiveIntegerField()
    other_action = models.StringField(choices=['X','Y'])
    other_payoff = models.CurrencyField()

    def get_partner(self):
        return self.get_others_in_group()[0]

