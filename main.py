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
MONGO_DB_URL = f"mongodb://{username}:{urllib.parse.quote(password)}@mongo.exceed19.online"
MONGO_DB_PORT = 8443

FORMAT_DATETIME = "%Y/%m/%d %H:%M"

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


@app.get("/lockerId/{locker_id}")
def locker(locker_id: str):
    '''
    show a locker
    '''
    information = collection.find({"id": locker_id}, {"_id": False})
    
    var = list(information)[0]
    print(var)
    
    start_string = var["start"]
    end_string = var["end"]
    start_object = datetime.strptime(start_string, FORMAT_DATETIME)
    now_object = datetime.now()
    end_object = datetime.strptime(end_string, FORMAT_DATETIME)
    duration = (end_object - now_object) / timedelta(seconds=60)

    dict_info = {f"Locker": var["id"], "duration": duration}
    return dict_info


@app.post("/{locker_id}/reserve/")
def reserve(locker_id: int, locker: Locker):
    '''
    จอง
    '''
    return {"Item id": locker_id}


@app.post("/{locker_id}/return_item")
def return_item():
    '''
    return Item
    '''
    pass


@app.get("/{locker_id}/return_item/payment/")
def payment():
    '''
    '''
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
