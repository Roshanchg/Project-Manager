from pydantic import Field,BaseModel
from uuid import UUID
from app.models.database import WorkspaceRole
from fastapi import HTTPException,status
from app.dependencies import validateColor

class CreateList(BaseModel):
    name:str=Field(default="Untitled",min_length=5,max_length=100)
    position:str|None= Field(default=None)


class ShowList(BaseModel):
    id:UUID
    name:str
    position:int
    
class UpdateList(BaseModel):
    id:UUID
    name:str| None=Field(None,min_length=5,max_length=100)
    position:str | None= Field(None)
    
    

def isValidUpdate(_list:UpdateList):
    if _list.name!=None and (len(_list.name)<5 and len(_list.name)>100):
        raise HTTPException(status.HTTP_406,"Invalid Name Field")
    else:
        return True
    

