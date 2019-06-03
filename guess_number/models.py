from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency
)
import random

doc = """
a.k.a. Keynesian beauty contest.

Players all guess a number; whoever guesses closest to
p of the average wins.

See https://en.wikipedia.org/wiki/Guess_2/3_of_the_average
"""


class Constants(BaseConstants):
    players_per_group = None
    num_rounds = 3
    p = 2/3 # the value of p in p-beauty context
    name_in_url = 'guess_number'

    jackpot = 12
    guess_max = 100

    instructions_template = 'guess_number/Instructions.html'


class Subsession(BaseSubsession):
    def creating_session(self):
        # this is run before the start of every round
        # self.group_randomly()
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round  # pick a random round for payment
            self.session.vars['num_subjects'] = len(self.get_players())


class Group(BaseGroup):
    average = models.FloatField()
    correct_number = models.FloatField()
    best_guess = models.PositiveIntegerField()
    num_winners = models.PositiveIntegerField()

    def set_payoffs(self):
        players = self.get_players()
        guesses = [player.guess for player in players]
        the_average = sum(guesses) / len(players)
        self.average = round(the_average,2)
        self.correct_number = round(Constants.p * the_average, 2)
        self.best_guess = min(guesses,
                              key=lambda guess: abs(guess - self.correct_number))

        winners = [player for player in players if player.guess == self.best_guess]
        self.num_winners = len(winners)

        # set winners and payoffs
        for player in winners:
            player.is_winner = True
            if self.round_number == self.session.vars['paying_round']:
                player.payoff = Constants.jackpot / self.num_winners / self.session.config['real_world_currency_per_point']

        if self.round_number == self.session.vars['paying_round']:
            self.session.vars['num_winners'] = self.num_winners
            for player in players:
                player.participant.vars['is_winner'] = player.is_winner
                # print(player.participant.vars)

    def correct_number_history(self):
        return [g.correct_number for g in self.in_previous_rounds()]

    def average_number_history(self):
        return [g.average for g in self.in_previous_rounds()]


class Player(BasePlayer):
    guess = models.PositiveIntegerField(max=Constants.guess_max)
    is_winner = models.BooleanField(initial=False)
