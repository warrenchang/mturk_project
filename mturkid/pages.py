from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import boto3


class WorkerID(Page):

    form_model = 'player'
    form_fields = ['workerid']

    def before_next_page(self):
        if not self.timeout_happened:
            if not self.session.config['debug']:
                access_key_id = self.session.config['access_key_id']
                secret_access_key = self.session.config['secret_access_key']
                if self.session.config['sandbox']: # sandbox
                    Qid = self.session.config['Qid_sandbox']
                    mturk = boto3.client(
                        service_name='mturk',
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key,
                        region_name='us-east-1',
                        endpoint_url="https://mturk-requester-sandbox.us-east-1.amazonaws.com",
                    )
                else: # live production
                    Qid = self.session.config['Qid']
                    mturk = boto3.client(
                        service_name='mturk',
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key,
                        region_name='us-east-1',
                    )

                mturk.associate_qualification_with_worker(
                    QualificationTypeId=Qid,
                    WorkerId=self.player.workerid,
                    IntegerValue=0,
                    SendNotification=False
                )

            self.participant.vars['workerid'] = self.player.workerid


class StartPage(Page):
    # timeout_seconds = 120

    def vars_for_template(self):
        return {
            'avg_payment': self.session.config['avg_payment'],
            'max_payment': self.session.config['max_payment'],
            'exchange_rate': int(round(1 / self.session.config['real_world_currency_per_point'])),
            'participation_fee': self.session.config['participation_fee'],
        }


class Consent(Page):
    # timeout_seconds = 120
    form_model = 'player'
    form_fields = ['consent','independent']


page_sequence = [
    WorkerID,
    StartPage,
    Consent,
]
