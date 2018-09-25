import json
import boto3
from Utils.Helpers import Utilities
from botocore.exceptions import ClientError

class Module(object):

    def __init__(self, module_values):
        self.module_values = module_values

    def inactivate(self, iam, accesskeyDict):
        '''
        Inactivate the access keys.
        '''
        userList = []

        for k,v in accesskeyDict.items():
            accesskeyid = k
            username = v

            iam.update_access_key(
                UserName=username,
                AccessKeyId=accesskeyid,
                Status='Inactive'
            )

            users = dict(UserName=username, AccessKeyId=accesskeyid, Result="Successful")

            userList.append(users)

        return(json.dumps(userList, indent=4))
        

    def execute(self):
        '''
        You need to specify one or more user ids.

        A user can have up to 2 access key ids.
        This iterates through their keys and makes
        all of them inactive.
        '''

        iam = boto3.client('iam')

        accesskeyDict = {}

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
                        
                        accesskeyDict[accesskeyid] = username
        
        return(self.inactivate(iam, accesskeyDict))