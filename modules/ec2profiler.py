import json
import boto3
from Utils.Helpers import Utilities
from botocore.exceptions import ClientError

class Module(object):

    def __init__(self, dryrun, instanceids, sgids, vpcids, usernames, \
                            accesskeyids, values):
        
        self.dryrun = dryrun

    def execute(self):
        '''
        Not sure what I want to do with this yet.
        '''

        ec2_client = boto3.client('ec2')

        dryrun = Utilities().str_to_bool(self.dryrun)

        try:
            response = ec2_client.describe_instances(
                DryRun=dryrun
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DryRunOperation':
                print(e.response['Error']['Message'])
                exit(0)