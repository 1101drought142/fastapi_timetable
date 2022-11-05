from __future__ import division
from fastapi import FastAPI
from common_logic import boolean_format
import asyncio
from database import connection, crud
from datetime import datetime

app = FastAPI()
db = connection.DbConection()
crd = crud.CRUD(db.get_session())

@app.middleware("http")
async def check_pass(request, call_next):
    """if request.query_params["pass"] != "pass":
        return {"error"}"""
    response = await call_next(request)
    return response

@app.get("/api/users/")
async def all_users():
    return crd.get_all_users()

@app.post("/api/users/")
async def create_user(name, login, public, description, password, age, telegram_id):
    
    return crd.create_user(
        name, 
        login,
        await boolean_format(public), 
        description, 
        password, 
        age, 
        telegram_id
    )

@app.post("/api/auth")
async def check_auth(login, password):
    try:
        return crd.auth(login, password)
    except:
        return {"False"}


@app.post("/api/events/")
async def create_event(user_id, time, name, comment, alert, duration):

    
    try:
        return crd.create_event(
            user_id, 
            datetime.fromisoformat(time), 
            name, 
            comment, 
            await boolean_format(alert),
            datetime.fromisoformat(duration),
        )
    except:
        return {"False"}
    