import json
import boto3
from Utils.Helpers import Utilities
from botocore.exceptions import ClientError

class Module(object):

    def __init__(self, module_values):
        self.module_values = module_values

    def inactivate(self, iam, username, accesskeyid):
        '''
        Inactivate the access keys.
        '''
        iam.update_access_key(
            UserName=username,
            AccessKeyId=accesskeyid,
            Status='Inactive'
        )
        print('Successfully inactivated {0},{1}'.format(username, accesskeyid))

    def execute(self):
        '''
        You need to specify one or more user ids.

        A user can have up to 2 access key ids.
        This iterates through their keys and makes
        all of them inactive.
        '''

        iam = boto3.client('iam')

        for username in self.module_values:
            paginator = iam.get_paginator('list_access_keys')

            username_info = paginator.paginate(
                UserName=username
                )

            for result in username_info:
                keys = result['AccessKeyMetadata']

                for keyid in keys:
                    # Check to see if it's already inactive. If it is, just skip it.
                    if keyid['Status'] == 'Active':
                        username = keyid['UserName']
                        accesskeyid = keyid['AccessKeyId']
                    
                        self.inactivate(iam, username, accesskeyid)