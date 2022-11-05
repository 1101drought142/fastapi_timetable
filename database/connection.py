
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .models import *



Base = declarative_base()

metadata_obj = MetaData()

class DbConection:
    def __init__(self):    
        URL = ""
        self.engine = create_engine(URL, echo=True, future=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.create_tables()
    
    def create_tables(self):
        User.__table__.create(bind=self.engine, checkfirst=True)
        Event.__table__.create(bind=self.engine, checkfirst=True)

    def get_session(self):
        return self.SessionLocal
