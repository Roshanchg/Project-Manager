from pydantic import Field,BaseModel
from uuid import UUID
from app.models.database import WorkspaceRole
from fastapi import HTTPException,status
from app.dependencies import validateColor

class CreateWorkspace(BaseModel):
    name:str=Field(default="Untitled",min_length=5,max_length=100)
    color:str= Field(default="#FFFFFF",max_length=7,min_length=7,pattern="^#[0-9a-fA-F]{6}$")


class ShowWorkspace(BaseModel):
    id:UUID
    name:str
    color:str
    role:WorkspaceRole
    
class UpdateWorkspace(BaseModel):
    id:UUID
    name:str| None=Field(None,min_length=5,max_length=100)
    color:str | None= Field(None,max_length=7,min_length=7,pattern="^#[0-9a-fA-F]{6}$")
    
    
    
def validUpdateWorkspace(upWorkspace:UpdateWorkspace)->bool:
    if ((upWorkspace.color!= None) and  (not validateColor(upWorkspace.color))):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,"Invalid Color Field")
    if ( (upWorkspace.name!=None) and not (len(upWorkspace.name)>=5 and len(upWorkspace.name)<=100)):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,"Invalid Name Field")
    return True