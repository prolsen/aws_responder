import json
import boto3
from Utils.Helpers import Utilities
from botocore.exceptions import ClientError

class Module(object):

    def __init__(self, dryrun, instanceid, sgid, vpcid, username, \
                            accesskeyid, values):
        pass

    def execute(self):
        '''
        List the IAM users and then return their
        UserId, Creation date, and last time the users
        used their passwords. Null if never.
        '''
        iam = boto3.client('iam')
        response = iam.list_users()

        encode_date = Utilities().encode_date

        userList = []
        
        for user in response['Users']:
            username = user['UserName']
            user_id = user['UserId']
            ctime = encode_date(user['CreateDate'])
            
            try:
                pass_last_used = encode_date(user['PasswordLastUsed'])
            except KeyError:
                pass_last_used = None
                
            users = dict(UserName=username, UserId=user_id, CreateDate=ctime, \
                        PasswordLastUsed=pass_last_used)

            userList.append(users)

        return(json.dumps(userList, indent=4))