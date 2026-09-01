from pydantic import BaseModel,Field
from uuid import UUID
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