
import logging
from datetime import datetime
import os

class Bucket:
    """
    Places numeric values into discret buckets
    """
    
    @staticmethod
    def date(date,seconds):
        """
        places a date object into a bucket based on how many seconds
        """

        #convert time into epoch time (seconds)
        rough_epoch = int(date.strftime('%s'))

        round_epoch = rough_epoch - (rough_epoch % seconds)

        round_date = datetime.fromtimestamp(round_epoch).strftime('%c')
        
        return round_date


