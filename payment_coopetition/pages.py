from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import boto3


class EndInfo(Page):
    timeout_seconds = 30
    # quiz bonus is part of the bonus, but not part of the "experiment_payoff"
    # final_payment = experiment_payment + participation_fee + quiz_bonus
    # bonus is the money to be sent to the participants (participation fee is sent automatically by Amazon)

    def vars_for_template(self):
        if 'quiz_bonus' in self.session.config:
            quiz_bonus = self.session.config['quiz_bonus']
        else:
            quiz_bonus = 0
        if 'coopetition_payoff' in self.participant.vars:
            coopetition_payoff = self.participant.vars['coopetition_payoff']
        else:
            coopetition_payoff = 0

        coopetition_payment = int(float(coopetition_payoff)*self.session.config['real_world_currency_per_point']*100)/100

        print(self.participant.vars)
        return {
            'qualified': self.participant.vars['qualified'],
            'matched': self.participant.vars['matched'],
            'coopetition_payoff': coopetition_payoff,
            'coopetition_payment': coopetition_payment,
            'participation_fee': self.session.config['participation_fee'],
            'quiz_bonus': quiz_bonus,
            'final_payment':  self.participant.payoff_plus_participation_fee(),
        }

    def before_next_page(self):
        if ('workerid' in self.participant.vars) and (not self.session.config['debug']):
            access_key_id = self.session.config['access_key_id']
            secret_access_key = self.session.config['secret_access_key']
            workerid = self.participant.vars['workerid']
            if self.session.config['sandbox']:  # sandbox
                Qid = self.session.config['Qid_sandbox']
                Qid2 = self.session.config['Qid2_sandbox']
                mturk = boto3.client(
                    service_name='mturk',
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    region_name='us-east-1',
                    endpoint_url="https://mturk-requester-sandbox.us-east-1.amazonaws.com",
                )
            else:  # live production
                Qid = self.session.config['Qid']
                Qid2 = self.session.config['Qid2']
                mturk = boto3.client(
                    service_name='mturk',
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    region_name='us-east-1',
                )

            if self.participant.vars['matched']: # if successfully completed coopetition task
                mturk.associate_qualification_with_worker(
                    QualificationTypeId=Qid,
                    WorkerId=workerid,
                    IntegerValue=2, # value 3 represent included in data analysis
                    SendNotification=False
                )
            else:
                mturk.associate_qualification_with_worker(
                    QualificationTypeId=Qid2,
                    WorkerId=workerid,
                    IntegerValue=1, # complete simple survey (EET)
                    SendNotification=False
                )



page_sequence = [
    EndInfo,
]
