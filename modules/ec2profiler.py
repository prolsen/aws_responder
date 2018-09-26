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
        Undecided.....
        '''

        ec2_client = boto3.client('ec2')

        dryrun = Utilities().str_to_bool(self.dryrun)

        response = ec2_client.describe_instances(
            DryRun=dryrun
        )

        for instances in response['Reservations']:
            for instance in instances['Instances']:
                return(instance)