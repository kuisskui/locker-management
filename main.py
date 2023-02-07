from fastapi import FastAPI, Body
import uvicorn
from typing import Union, Optional, List
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
import urllib
from dotenv import load_dotenv

load_dotenv('.env')

DATABASE_NAME = "exceed01"
COLLECTION_NAME = "locker-management"
username = os.getenv("user")
password = urllib.parse.quote(os.getenv('password'))
MONGO_DB_URL = f"mongodb://{username}:{password}@mongo.exceed19.online"
MONGO_DB_PORT = 8443

FORMAT_DATETIME = "%Y/%m/%d %H:%M"


class Locker(BaseModel):
    id: Union[int, str]
    user_id: Union[int, str]
    items: List[str]
    start: datetime
    end: datetime


class Item(BaseModel):
    user_id: Union[int, str]
    amount: int


client = MongoClient(f"{MONGO_DB_URL}:{MONGO_DB_PORT}/?authMechanism=DEFAULT")

db = client[DATABASE_NAME]

collection = db[COLLECTION_NAME]

app = FastAPI()


@app.get("/")
def root():
    return {"msg": "pick a locker"}


@app.get("/{locker_id}/")
def locker():
    '''
    show a locker
    '''
    return {"msg": "test"}


@app.post("/{locker_id}/reserve/")
def reserve(locker_id: int, locker: Locker):
    '''
    จอง
    '''

    return {"Item id": locker_id}


@app.post("/lockerId/{locker_id}")
def return_item(locker_id: str):
    '''
    return Item
    '''

    info = collection.find({"id": locker_id}, {"_id": False})
    var = list(info)[0]
    end_date = var['end']
    start_date = var['start']

    start_obj = datetime.strptime(start_date, FORMAT_DATETIME)
    end_obj = datetime.strptime(end_date, FORMAT_DATETIME)
    reserve_time = (end_obj - start_obj).seconds
    receive_time = (end_obj - datetime.now()).seconds
    
    charge = 0
    if reserve_time/60/60 > 2:
        charge = round(reserve_time/60/60 - 2)*5
        
    late = 0
    if datetime.now() > end_obj:
        late = round(receive_time/60/10)*20
        
    total = charge + late
    return {"Change": total}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
