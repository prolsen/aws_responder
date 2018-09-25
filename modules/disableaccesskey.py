import boto3
import json
from Utils.Helpers import Utilities

class Module(object):

    def __init__(self, module_values):
        self.module_values = module_values

    def execute(self):
        '''
        Makes the access key id provided inactive.
        '''
    
        if len(self.module_values[0]) == 20:
            iam = boto3.client('iam')

            response = iam.update_access_key(
                AccessKeyId=self.module_values[0],
                Status='Inactive'
                )
    
        else:
            return('Failed. Are you sure you entered the correct access key?')
            exit(0)
        
        return('Success')