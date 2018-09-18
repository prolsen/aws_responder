from datetime import date, datetime

class Utilities(object):

    def __init__(self):
        pass

    def encode_date(self, timestamp):
        """https://protect-us.mimecast.com/s/ktPaCyP2B4ur5QzDcZfRUy?domain=stackoverflow.com"""
        if isinstance(timestamp, (datetime, date)):
            return timestamp.isoformat()
        raise TypeError ("Type %s not serializable" % type(timestamp))