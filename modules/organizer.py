
from pydantic import BaseModel,validator
from .db import db,db_session
from fastapi import Depends
from .security import get_api_key,API_KEY

class Model(BaseModel):
    number:int
    @validator("number")
    def validate_number(cls,v):
        if len(str(v))!=10:
            raise ValueError(f'Invalid phone number. Must be 10 digits long (including area code)')
        return v

def register_organizer(body:Model,api_key:APIKey=Depends(get_api_key)):
    """
    Registers phone number with event creation priviledges

        Body:
            number: phone number digits (with area code)
    """    
    phone_number = f'+1{body.number}'
    with db_session:
        user = db.User.get(phone_number=phone_number)
        if not user:
            user = db.User(phone_number=phone_number,is_organizer=True)
            db.commit()
            response = "event organizer user added succesfully"
        else: 
            if user.is_organizer:
                response = "user was already an event organizer"
            else:
                user.is_organizer = True
                db.commit()
                response = "existing user set to event organizer"
    return response
    
