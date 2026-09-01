from pydantic import BaseModel,Field
from uuid import UUID
from app.dependencies import validateEmail
from fastapi import HTTPException,status


class ResponseUser(BaseModel):
    id: UUID 
    email: str 
    full_name: str

class CreateUser(BaseModel):
    email:str =Field(min_length=5)
    password:str = Field(min_length=8)
    full_name:str=Field(min_length=3)
    
class UpdateUser(BaseModel):
    email:str |None = Field(None,min_length=5)
    password:str | None = Field(None,min_length=8)
    full_name:str | None =Field(None,min_length=3)

class LoginUser(BaseModel):
    email:str =Field(min_length=5)
    password:str =Field(min_length=8)
    
def isValidUpdateUser(user:UpdateUser)->bool:
    if (user.email!=None and validateEmail(user.email)):
        raise HTTPException(status.HTTP_403_FORBIDDEN,"Invalid Email value")
    if (user.full_name!=None and (len(user.full_name)>=5 and len(user.full_name)<=100)):
        raise HTTPException(status.HTTP_403_FORBIDDEN,"Invalid Full Name value")
    if (user.password!=None and len(user.password)>=8 ):
        raise HTTPException(status.HTTP_403_FORBIDDEN,"Short password")
    return True
        