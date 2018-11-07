from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import math

author = 'Huanren Zhang'

doc = """
Coopetition game: trade-off between value co-creation and value appropriation
"""

def get_share(p1,p2):
    if p1==0 and p2 ==0:
        return 1/2
    else:
        return p1/(p1+p2)

class Constants(BaseConstants):
    name_in_url = 'coopetition_mturk'
    instructions_template = 'coopetition_mturk/Instructions_template.html'
    breakdowns_template = 'coopetition_mturk/Breakdowns_template.html'
    history_template = 'coopetition_mturk//History.html'
    historyall_template = 'coopetition_mturk//HistoryAllRounds.html'
    history_previous_template = 'coopetition_mturk//History_previous.html'
    historyall_previous_template = 'coopetition_mturk//HistoryAllRounds_previous.html'
    otherhistory_template = 'coopetition_mturk//OtherHistory.html'
    extra_info = 'coopetition_mturk//WaitingInfo.html'

    players_per_group = 2

    A_values = [0,60]

    interactions = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    ]
    round_in_interactions = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    ]
    interaction_length = [10, 10]

    interactions = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    ]
    round_in_interactions = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    ]
    interaction_length = [15, 15]

    # interactions = [
    #     1, 1, 1,
    #     2, 2, 2,
    # ]
    # round_in_interactions = [
    #     1, 2, 3,
    #     1, 2, 3,
    # ]
    #
    # interaction_length = [3, 3]

    num_rounds = sum(interaction_length) # change num_rounds for testing purpose, but need to make sure that number_sequence


class Subsession(BaseSubsession):

    def creating_session(self):
        # this is run before the start of every round
        round_in_interaction = Constants.round_in_interactions[self.round_number-1]
        interaction_number = Constants.interactions[self.round_number-1]
        # set the treatment variable
        treatment = self.session.config['treatment']


        for p in self.get_players(): # set interaction number and round number
            p.interaction_number = interaction_number
            p.round_in_interaction = round_in_interaction
            p.treatment = treatment
            p.condition = p.treatment[:3]
            if p.condition=='Fix':
                ## a random number between 1 and 200 (inclusive)
                p.rand_num = int(math.ceil(random.random()*200))
            elif p.condition=='Var':
                ## a random number between 1 and 110 (inclusive)
                p.rand_num = int(math.ceil(random.random()*110))
            if p.treatment[3] == '0':
                p.A = Constants.A_values[p.interaction_number-1]
            else:
                p.A = Constants.A_values[2-p.interaction_number]


class Group(BaseGroup):
    def interact(self):
        ## note that Group.get_players() get all the players in the group, ordered by id_in_group
        p1,p2 = self.get_players()
        p1.my_id = p1.participant.id_in_session
        p2.my_id = p2.participant.id_in_session
        p1.partner_id = p2.my_id
        p2.partner_id = p1.my_id
        p2.rand_num = p1.rand_num

        # first calculate payoff
        p1.other_endowment = p2.endowment
        p2.other_endowment = p1.endowment
        p1.other_a1 = p2.a1
        p1.other_a2 = p2.a2
        p1.other_a3 = p2.a3
        p2.other_a1 = p1.a1
        p2.other_a2 = p1.a2
        p2.other_a3 = p1.a3

        ## endownment for player 1 is 20 in the asymmetric treatment
        if p1.condition =='Det':
            p1.pie = p1.a1*p2.a1 + p1.A
            p2.pie = p1.a1*p2.a1 + p2.A
        elif p1.condition =='Asm':
            p1.pie = p1.a1*p2.a1/2 + p1.A
            p2.pie = p1.a1*p2.a1/2 + p2.A
        elif p1.condition =='Fix':
            p1.successful = p1.rand_num <= 100
            p2.successful = p1.successful
            if p1.successful: # investment is a success
                p1.pie = 2*p1.a1*p2.a1 + p1.A
                p2.pie = p1.pie
            else:
                p1.pie = p1.A
                p2.pie = p1.pie
        elif p1.condition =='Var':
            p1.successful = p1.rand_num <= p1.a1*p2.a1
            p2.successful = p1.successful
            if p1.successful: # investment is a success
                p1.pie = 110 + p1.A
                p2.pie = p1.pie
            else:
                p1.pie = p1.A
                p2.pie = p1.pie

        p1.pie_share = round(get_share(p1.a2,p2.a2),2)
        p2.pie_share = round(get_share(p2.a2,p1.a2),2)
        p1.potential_payoff = p1.pie*p1.pie_share + p1.a3
        p2.potential_payoff = p2.pie*p2.pie_share + p2.a3
        if p1.timed_out:
            p1.payoff = 0
        else:
            p1.payoff = p1.potential_payoff
        if p2.timed_out:
            p2.payoff = 0
        else:
            p2.payoff = p2.potential_payoff

        p1.cum_payoff = sum([p.payoff for p in p1.in_all_rounds()
                                      if p.interaction_number == p1.interaction_number])
        p2.cum_payoff = sum([p.payoff for p in p2.in_all_rounds()
                             if p.interaction_number == p1.interaction_number])

        p1.other_payoff = p2.potential_payoff
        p2.other_payoff = p1.potential_payoff
        p1.other_share = p2.pie_share
        p2.other_share = p1.pie_share

        # print((self.round_number,p1.payoff,p2.payoff))

        # update payoff for Part I in terms of real currency
        # p1.participant.vars['real_payoff_PartI'] = p1.cum_payoff * self.session.config['real_world_currency_per_point']
        # p2.participant.vars['real_payoff_PartI'] = p2.cum_payoff * self.session.config['real_world_currency_per_point']

        # print((p1.participant.id_in_session,p1.action,p1.payoff,p1.signal,p2.participant.id_in_session,p2.action,p2.payoff,p2.signal))

class Player(BasePlayer):
    my_id = models.PositiveIntegerField()
    treatment = models.StringField()
    condition = models.StringField()
    A = models.IntegerField()
    interaction_number = models.PositiveIntegerField()
    round_in_interaction = models.PositiveIntegerField()
    ## role for asymmetric treatment. role=1 means endowment = 10 (B player), role=2 means endowment = 20 (A player)
    role = models.StringField()

    endowment = models.IntegerField()
    a1 = models.IntegerField(min=0, max=20)
    a2 = models.IntegerField(min=0, max=20)
    a3 = models.IntegerField(min=0, max=20)
    pie = models.FloatField()
    pie_share = models.FloatField(min=0, max=1)
    ## here we use potential_payoff to record the payoff, the real payoff will be set to 0 if a time_out happened.
    potential_payoff = models.CurrencyField()
    timed_out = models.BooleanField()
    cum_payoff = models.CurrencyField()

    partner_id = models.PositiveIntegerField()
    other_endowment = models.IntegerField()
    other_a1 = models.IntegerField(min=0, max=20)
    other_a2 = models.IntegerField(min=0, max=20)
    other_a3 = models.IntegerField(min=0, max=20)
    other_share = models.FloatField(min=0, max=1)
    other_payoff = models.CurrencyField()
    other_cum_payoff = models.CurrencyField()
    rand_num = models.PositiveIntegerField(max=200)
    successful = models.BooleanField()

    def get_partner(self):
        return self.get_others_in_group()[0]

