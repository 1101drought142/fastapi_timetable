from .models import *
from .business_logic import TimeCheck

class CRUD:
    def __init__(self, session):
        self.session = session()
    
    def create_user(self, name:str, login:str, public:bool, description:str, password:str ,age: int, telegram_id: int):    
        temp_user = User(
            name = name,
            age = age,
            login = login, 
            public= public, 
            description = description, 
            telegram_id = telegram_id,
        )
        temp_user.set_password(password=password)
        self.session.add(
            temp_user
        )
        self.session.commit()
        return '', 200

    def get_all_users(self):
        return self.session.query(User).filter_by(public=True).all()

    def auth(self, login, password):
        temp_user = self.session.query(User).filter_by(login=login).first()
        return temp_user.check_password(password)

    def return_login(self, telegram_id):
        pass
        #send login to telegram

    def create_event(self, user_id, time, name, comment, alert, duration):
        
        if not(TimeCheck(time, duration, self.session).check()):
            raise ValueError
        
        temp_event = Event(
            user_id = user_id,
            time = time,
            name = name,
            comment = comment,
            alert = alert,
            duration = duration
        )
        self.session.add(
            temp_event
        )
        self.session.commit()
        return '', 200

    def get_events(self, user_id, time, name, comment, alert):
        pass

    def delete_event(self, event_id):
        pass