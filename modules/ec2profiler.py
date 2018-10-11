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

        response = ec2_client.describe_instances(
            DryRun=dryrun
        )

        instances = Utilities().yieldInstances(response)