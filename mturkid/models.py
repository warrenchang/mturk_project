from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import boto3
from os import environ


author = 'Huanren Zhang'

doc = """
Ask MTurk workers to input a valid ID, and assign qualification to prevent from retakes
"""


class Constants(BaseConstants):
    name_in_url = 'mturkid'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        pass
        # if self.session.config['sandbox']:
        #     mturk = boto3.client(
        #         service_name='mturk',
        #         aws_access_key_id="AKIATXHDW3IQG3MRKVGD",
        #         aws_secret_access_key="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",
        #         region_name='us-east-1',
        #         endpoint_url="https://mturk-requester-sandbox.us-east-1.amazonaws.com",
        #     )
        # else:
        #     mturk = boto3.client(
        #         service_name='mturk',
        #         aws_access_key_id="AKIATXHDW3IQG3MRKVGD",
        #         aws_secret_access_key="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",
        #         region_name='us-east-1',
        #     )
        # print(mturk)
        # self.session.vars['mturk'] = mturk


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ## needs to change server and qualificaiton types before the experiment
    workerid = models.StringField()
    consent = models.BooleanField()
    independent = models.BooleanField()

    def workerid_error_message(self, value):
        print('value is', value, self.session.config['access_key_id'])
        if not self.session.config['debug']:
            access_key_id = self.session.config['access_key_id']
            secret_access_key = self.session.config['secret_access_key']
            print('access_key_id',access_key_id, environ.get('AWS_ACCESS_KEY_ID'))
            print('secret_access_key',secret_access_key, environ.get('AWS_SECRET_ACCESS_KEY'))
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
            try:
                mturk.associate_qualification_with_worker(
                    QualificationTypeId=Qid,
                    WorkerId=value,
                    IntegerValue=0,
                    SendNotification=False
                )
            except Exception as e:
                print(e, value,Qid,)
                return 'Please input a valid Worker ID.'
