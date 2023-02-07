from fastapi import FastAPI, Body
import uvicorn
from typing import Union, Optional, List
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import os
import urllib
from dotenv import load_dotenv

load_dotenv('sample.env')

# {
#     "id" : "2",
#     "items" : ["key"],
#     "user_id" : 0,
#     "start" : "2000-01-01 00:00:00",
#     "end" : "2000-01-01 00:00:00"
# }

DATABASE_NAME = "exceed01"
COLLECTION_NAME = "locket-management"
username = os.getenv("user")
password = urllib.parse.quote(os.getenv('password'))
MONGO_DB_URL = f"mongodb://{username}:{password}@mongo.exceed19.online"
MONGO_DB_PORT = 8443


class Locker(BaseModel):
    id: Union[int, str]
    user_id: Union[int, str]
    items: List[str]
    start: datetime
    end: datetime

client = MongoClient(f"{MONGO_DB_URL}:{MONGO_DB_PORT}/?authMechanism=DEFAULT")

db = client[DATABASE_NAME]

collection = db[COLLECTION_NAME]

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "pick a locker"}


@app.get("/{locker_id}/")
def locker(locker_id):
    '''
    show a locker
    '''
    return collection.find({"id": locker_id})


@app.post("/{locker_id}/reserve/")
def reserve(locker_id: int, locker: Locker):
    '''
    จอง
    '''
    collection.update_one({"id": locker_id}, {"$set": {"user_id": locker.id, "items": locker.items,"start": locker.start, "end": locker.end}}, upsert=True)
    return {"Item id": locker_id}
    # return {"Item id": locker_id,"test1": locker.id, "test2": locker.items,"test3":locker.start}


@app.post("/{locker_id}/return_item")
def return_item(locker_id):
    '''
    return Item
    '''
    collection.update_one({"id":locker_id}, {"$set": {"user_id": "", "items": {},"start": "", "end": ""}}, upsert=True)
    return collection.find({"id": locker_id}, {"_id": False})
    

@app.get("/{locker_id}/return_item/payment/")
def payment():
    '''
    '''
    pass
    # > 2 hours + 5*time(h)
    # จ่ายเงินเกิน > เงินทอน
    # กเิน ค่าปรับ 10 min 20 baht
    


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
