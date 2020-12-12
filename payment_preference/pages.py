from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import boto3


class EndInfo(Page):
    timeout_seconds = 30

    def vars_for_template(self):
        participation_fee = self.session.config['participation_fee']
        final_payment = self.participant.payoff_plus_participation_fee()
        print(self.participant.vars)
        payoff_info = [
            ('Allocation task','To be determined.'),
            # ('Coin tossing task 1', str(c(self.participant.vars['lying1_payoff']))),
            ("Lottery Task 1", str(c(self.participant.vars['lottery1_payoff']))),
            ("Lottery Task 2", str(c(self.participant.vars['lottery2_payoff']))),
            # ('Number guessing task', str(c(self.participant.vars['lying2_payoff']))),
            ("Urn Gamble 1", str(c(self.participant.vars['ambiguity_payoff_info'][0][-1]))),
            ("Urn Gamble 2", str(c(self.participant.vars['ambiguity_payoff_info'][1][-1]))),
            ("Guessing Ball Number", str(c(self.participant.vars['ballnumber_payoff']))),
            # ('Coin tossing task 2', str(c(self.participant.vars['lying3_payoff']))),
            ('Solving puzzles', str(c(self.participant.vars['ravens_payoff']))),
            ('Logical questions', str(c(self.participant.vars['crt_payoff'])),)
        ]

        return {
            'payoff_info': payoff_info,
            'participation_fee': participation_fee,
            'payoff_in_points': self.participant.payoff,
            'bonus_payment': final_payment - participation_fee,
            'final_payment':  final_payment,
        }

    def before_next_page(self):
        if ('workerid' in self.participant.vars)and(not self.session.config['debug']):
            access_key_id = self.session.config['access_key_id']
            secret_access_key = self.session.config['secret_access_key']
            workerid = self.participant.vars['workerid']
            if self.session.config['sandbox']:  # sandbox
                Qid = self.session.config['Qid_sandbox']
                mturk = boto3.client(
                    service_name='mturk',
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    region_name='us-east-1',
                    endpoint_url="https://mturk-requester-sandbox.us-east-1.amazonaws.com",
                )
            else:  # live production
                Qid = self.session.config['Qid']
                mturk = boto3.client(
                    service_name='mturk',
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    region_name='us-east-1',
                )

            mturk.associate_qualification_with_worker(
                QualificationTypeId=Qid,
                WorkerId=workerid,
                IntegerValue=3, # value 3 represent included in data analysis
                SendNotification=False
            )


page_sequence = [
    EndInfo,
]
