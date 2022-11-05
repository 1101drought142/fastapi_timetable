from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256
Base = declarative_base()

class User(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True, unique=True)
    name = Column(String, index=True)
    age = Column(Integer)
    telegram_id = Column(String, unique=True)
    public = Column(Boolean)
    description = Column(String)
    hash_password = Column(String)

    #confirmed = Column(Boolean)

    def set_password(self, password):
        self.hash_password = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.hash_password)

    events = relationship("Event")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    time = Column(DateTime, index=True, unique=True)
    name = Column(String)
    comment = Column(String)
    alert = Column(Boolean)
    duration = Column(DateTime, index=True, unique=True)
    #confirmed = Column(Boolean)