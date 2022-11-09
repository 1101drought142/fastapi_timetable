from fastapi import FastAPI, HTTPException
from database import connection, models
from datetime import datetime
from sqlalchemy import and_
from business_logic import TimeCheck

app = FastAPI()
db = connection.DbConection()
session = db.get_session()()

@app.middleware("http")
async def check_pass(request, call_next):
    """if request.query_params["pass"] != "pass":
        return {"error"}"""
    response = await call_next(request)
    return response

@app.get("/api/users/", status_code=200)
def all_users():
    return session.query(models.User).filter_by(public=True).all()

@app.post("/api/users/", status_code=201)
def create_user(name:str, login:str, public:bool, description:str, password:str, age:int, telegram_id:str):
    temp_user = models.User(
        name = name,
        age = age,
        login = login, 
        public= public, 
        description = description, 
        telegram_id = telegram_id,
    )
    temp_user.set_password(password=password)
    session.add(
        temp_user
    )
    session.commit()
    return temp_user

@app.post("/api/users/auth/", status_code=200)
def check_auth(login:str, password:str):
    temp_user = session.query(models.User).filter_by(login=login).first()
    return temp_user.check_password(password)

@app.get("/api/events/", status_code=200)
def get_events(start_time: datetime, end_time:datetime, user_id:int, public:bool):
    taken_time = session.query(models.Event).filter( and_(models.Event.time >= start_time, models.Event.duration <= end_time, models.Event.user_id == user_id) ).all()
    return taken_time

@app.post("/api/events/", status_code=201)
def create_event(user_id:int, time:datetime, name:str, comment:str, alert:bool, duration:datetime):

    try:
        TimeCheck(time, duration, session).check_or_error()
    except ValueError as e:
        return HTTPException(status_code=412, detail=f"Given time is incorrect. {str(e)}")
    except Exception:
        return HTTPException(status_code=500, detail="Server Error")

    temp_event = models.Event(
        user_id = user_id,
        time = time,
        name = name,
        comment = comment,
        alert = alert,
        duration = duration
    )

    session.add(
        temp_event
    )

    session.commit()
    return temp_event

@app.delete("/api/events/")
async def delete_event(event_id:int):
    deleted_event = session.query(models.Event).get(event_id)
    if deleted_event:
        session.delete(deleted_event)
        session.commit()
        session.close
    else: 
        raise HTTPException(status_code=404, detail="No Event with such id")
    return deleted_event