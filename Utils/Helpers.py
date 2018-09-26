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