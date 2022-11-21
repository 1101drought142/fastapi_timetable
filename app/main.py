from fastapi import FastAPI, HTTPException, Depends
from database import connection, models
from datetime import datetime
from sqlalchemy import and_
from .business_logic import TimeCheck
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = ""
ALGORITH = "HS256"

app = FastAPI()
db = connection.DbConection()
session = db.get_session()()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token/")

@app.middleware("http")
async def check_pass(request, call_next):
    """if request.query_params["pass"] != "pass":
        return {"error"}"""
    response = await call_next(request)
    return response

@app.get("/api/users/", status_code=200)
def all_users(token: str = Depends(oauth2_scheme)):

    if (token):
        return session.query(models.User).filter_by(public=True).all()
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

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

@app.post("/api/token/", status_code=200)
def check_auth(form_data: OAuth2PasswordRequestForm = Depends()):

    temp_user = session.query(models.User).filter_by(login=form_data.username).first()
    if not(temp_user):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not(temp_user.check_password(form_data.password)):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    else:
        return {"access_token": temp_user.login, "token_type": "bearer"}

@app.get("/api/events/", status_code=200)
def get_events(start_time: datetime, end_time:datetime, user_id:int, public:bool):
    
    taken_time = session.query(models.Event).filter( and_(models.Event.time >= start_time, models.Event.duration <= end_time, models.Event.user_id == user_id) ).all()
    return taken_time

@app.post("/api/events/", status_code=201)
def create_event(user_id:int, time:datetime, name:str, comment:str, alert:bool, duration:datetime):

    try:
        TimeCheck(time, duration, session).create_check_or_error()
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
def delete_event(event_id:int):
    deleted_event = session.query(models.Event).get(event_id)
    if deleted_event:
        session.delete(deleted_event)
        session.commit()
        session.close
    else: 
        raise HTTPException(status_code=404, detail="No Event with such id")
    return deleted_event