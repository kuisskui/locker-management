from fastapi import FastAPI, Body
import uvicorn
from typing import Union, Optional, List
from pydantic import BaseModel
from datetime import datetime


class Locker(BaseModel):
    id: Union[int, str]
    user_id: Union[int, str]
    items: List[str]
    start: datetime
    end: datetime


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
    uvicorn.run(app, host="0.0.0.0", port=8080)
