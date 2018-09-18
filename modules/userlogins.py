import boto3
import json
from Utils.Helpers import Utilities

class Module(object):

    def __init__(self, values):
        self.values = values

    def execute(self):
        '''
        List the IAM users and then return their
        UserId, Creation date, and last time the users
        used their passwords. Null if never.
        '''
        iam = boto3.client('iam')
        response = iam.list_users()

        encode_date = Utilities().encode_date

        userDict = []
        
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

            userDict.append(users)

        return(json.dumps(userDict, indent=4))