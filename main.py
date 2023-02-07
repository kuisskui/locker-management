from fastapi import FastAPI, Body
import uvicorn
from typing import Union, Optional, List
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
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

FORMAT_DATETIME = "%y/%m/%d %H:%M"


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


@app.post("/{locker_id}/return_item/")
def return_item(locker_id: str, itm: Item):
    '''
    return Item
    '''
    print(itm.user_id)

    info = list(collection.find({"user_id": str(itm.user_id)}, {"_id": False}))
    print(info)
    var = info[0]
    receive_date = datetime.now()
    end_date = var['end']
    start_date = var['start']
    print(start_date, end_date)
    # start_obj = start_date.strptime(start_date, FORMAT_DATETIME)
    # end_obj = end_date.strptime(end_date, FORMAT_DATETIME)
    duration = end_date - start_date
    receive_duration = end_date - receive_date
    if duration < receive_duration:
        pass
    if receive_duration > datetime.timestamp:
        pass
    return {"Change": receive_duration, "amount": itm.amount}


@app.get("/{locker_id}/return_item/payment/")
def payment():
    '''
    '''
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
