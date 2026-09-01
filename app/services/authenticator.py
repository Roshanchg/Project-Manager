import app.models.database as db
from app.models.tables import *
import app.utils.utils as utils
from sqlmodel import Session
from fastapi import HTTPException,status
import app.schemas.users as USERSCHEMA

def authenticate(session:Session,email:str,password:str):
    user=db.getUserFromEmail(session=session,email=email)
    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Email Not Registered")
    auth=utils.matchHash(cipher=user.password_hash,string=password)
    if auth:
        print("Valid Credentials Authenticating.")
        return user
    return 

def RegisterUser(session:Session,formUser:USERSCHEMA.CreateUser):
    user=db.getUserFromEmail(session=session,email=formUser.email)
    if user!=None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User Already Exists")
    
    user=User(
        **formUser.model_dump(exclude={"password"}),
        password_hash=utils.hashString(formUser.password)
    ) 
    db.insertUser(session=session,user=user)
    print("New User Registered")