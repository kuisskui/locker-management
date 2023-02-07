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

# {
#     "id" : "2",
#     "items" : ["key"],
#     "user_id" : 0,
#     "start" : "2000-01-01 00:00:00",
#     "end" : "2000-01-01 00:00:00"
# }

DATABASE_NAME = "exceed01"
COLLECTION_NAME = "locker-management"
username = os.getenv("user")
password = os.getenv('password')
MONGO_DB_URL = f"mongodb://{username}:{password}@mongo.exceed19.online"
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
def reserve(locker_id: str, user_id: str = Body(), items: List = Body(), start: str = Body(), end: str = Body()):
    '''
    จอง
    '''
    print(user_id, items)
    collection.update_one({"id": locker_id}, {"$set": {"user_id": user_id, "items": items,"start": start, "end": end}})
    return {"message": "reserved"}
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
    


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
