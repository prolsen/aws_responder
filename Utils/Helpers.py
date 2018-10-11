import boto3
from botocore.exceptions import ClientError
from datetime import date, datetime

class Utilities(object):

    def __init__(self):
        pass

    def encode_date(self, timestamp):
        '''
        https://protect-us.mimecast.com/s/ktPaCyP2B4ur5QzDcZfRUy?domain=stackoverflow.com
        '''
        if isinstance(timestamp, (datetime, date)):
            return timestamp.isoformat()
        raise TypeError ("Type %s not serializable" % type(timestamp))

    def str_to_bool(self, drystring):
        '''
        https://stackoverflow.com/questions/21732123/convert-true-false-value-read-from-file-to-boolean/41611608
        '''
        if drystring == 'True':
            return True
        elif drystring == 'False':
            return False
        else:
            print('Did you forget to specify the DryRun arguement --dryrun True|False')
            exit(0)

    def yieldInstances(self, dryrun):
        ec2_client = boto3.client('ec2')

        try:
            response = ec2_client.describe_instances(
                DryRun=dryrun
            )

        except ClientError as e:
            if e.response['Error']['Code'] == 'DryRunOperation':
                print(e.response['Error']['Message'])
                exit(0)

        for instances in response['Reservations']:
            for instance in instances['Instances']:
                yield(instance)