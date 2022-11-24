from datetime import datetime, timedelta
from database import models
from sqlalchemy import and_
import pytz
import redis
from .common_logic import generate_random_string

SECRET_KEY = ""
ALGORITH = "HS256"

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
        taken_time = self.session.query(models.Event).filter( and_(models.Event.time >= self.time, models.Event.duration <= self.duration) ).count()
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

    def create_check_or_error(self):
        
        if not(self.check_if_time_is_valid_or_false( self.time ) and self.check_if_time_is_valid_or_false(self.duration)):
            raise ValueError("It needs to be split by 15 minutes")
        elif not(self.check_if_duration_valid_or_false()):
            raise ValueError("End time is earlier than start time")
        elif not(self.check_if_time_is_taken_or_false()):
            raise ValueError("Time period is already taken")
        elif not(self.check_if_time_is_current()):
            raise ValueError("Time period is in past")
        else:
            return True



class Auth():

    #jwt tokens
    def create_roken():
        pass
    
    def verify_tokens():
        pass
    
    # idea to try, token in redis
    """
    r = redis.Redis(host='localhost', port=6379, db=0)    
    def create_token(login : str):
        temp_random_string = generate_random_string()
        if (r.set(temp_random_string, login)):
            return temp_random_string

    def verify_token(token):
        temp_login = r.get(token)
        if (temp_login):
            return temp_login"""


    