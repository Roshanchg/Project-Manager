from pydantic import Field,BaseModel
from uuid import UUID
from app.models.database import WorkspaceRole
from fastapi import HTTPException,status
from app.dependencies import validateColor
from datetime import datetime,timezone

class CreateChecklist(BaseModel):
    name:str =Field(default="Checklist",min_length=1)

class ShowChecklist(BaseModel):
    id:UUID
    name:str
        
class UpdateChecklist(BaseModel):
    id:UUID
    name:str|None=Field(None,min_length=1,max_length=100)

def isValidUpdate(checklist:UpdateChecklist):
    if checklist.name!=None and (len(checklist.name)<1 and len(checklist.name)>100):
        raise HTTPException(status.HTTP_406,"Invalid Name Field.")
    else:
        return True
    

