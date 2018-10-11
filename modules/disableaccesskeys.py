import json
import boto3
from Utils.Helpers import Utilities
from botocore.exceptions import ClientError

class Module(object):

    def __init__(self, dryrun, instanceids, sgids, vpcids, usernames, \
                            accesskeyids, values):
        self.usernames = usernames
        self.dryrun = dryrun

    def inactivate(self, iam_client, accesskeyDict):
        '''
        Inactivate the access keys.
        '''
        userList = []

        for k,v in accesskeyDict.items():
            accesskeyid = k
            username = v

            iam_client.update_access_key(
                UserName=username,
                AccessKeyId=accesskeyid,
                Status='Inactive'
            )

            users = dict(UserName=username, AccessKeyId=accesskeyid, \
                    Result="Successful"
                    )
            
            userList.append(users)
        
        if len(userList) == 0:
            exit(0)
        else:
            return(json.dumps(userList, indent=4))
        

    def execute(self):
        '''
        You need to specify one or more user ids.

        A user can have up to 2 access key ids.
        This iterates through their keys and makes
        all of them inactive.
        '''
        iam_client = boto3.client('iam')
        #dryrun = Utilities().str_to_bool(self.dryrun)
        accesskeyDict = {}

        for username in self.usernames:
            paginator = iam_client.get_paginator('list_access_keys')

            username_info = paginator.paginate(
                UserName=username
                )

            for result in username_info:
                #print(result)
                keys = result['AccessKeyMetadata']

                for keyid in keys:
                    # Check to see if it's already inactive. If it is, just skip it.
                    if keyid['Status'] == 'Active':
                        username = keyid['UserName']
                        accesskeyid = keyid['AccessKeyId']
                        
                        accesskeyDict[accesskeyid] = username
                    else:
                        print('{0},{1} is already inactive'.format(keyid['UserName'], \
                                                                    keyid['AccessKeyId']))
                        continue
        
        return(self.inactivate(iam_client, accesskeyDict))