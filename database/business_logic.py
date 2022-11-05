from datetime import datetime, timedelta
from .models import *
from sqlalchemy import and_
import pytz

class TimeCheck:

    def __init__(self, time, duration, session):
        self.time = time
        self.duration = duration
        self.session = session
        

    def check_if_time_is_valid_or_false(self, time: datetime):
        if not(time.second == 0):
            return False
        elif not(time.minute % 15 == 0):
            return False
        else:
            return True

    def check_if_duration_valid_or_false(self):
        if (self.duration - self.time > timedelta(seconds=0)):
            return True
        else: 
            return False

    def check_if_time_is_taken_or_false(self):
        taken_time = self.session.query(Event).filter( and_(Event.time >= self.time, Event.duration <= self.duration) ).count()
        if (taken_time > 0):
            return False
        else:
            return True

    def check_if_time_is_current(self):
        utc = pytz.timezone('Europe/London') 
        
        if (datetime.now(utc).replace(tzinfo=utc) > self.time.replace(tzinfo=utc)):
            return False
        else:
            return True

    def check(self):
        self.check_if_time_is_current()
        if not(self.check_if_time_is_valid_or_false( self.time ) and self.check_if_time_is_valid_or_false(self.duration)):
            return False
        elif not(self.check_if_duration_valid_or_false()):
            return False
        elif not(self.check_if_time_is_taken_or_false()):
            return False
        elif not(self.check_if_time_is_current()):
            return False
        else:
            return True

        