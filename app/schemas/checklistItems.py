from pydantic import Field,BaseModel
from uuid import UUID
from app.models.database import WorkspaceRole
from fastapi import HTTPException,status
from app.dependencies import validateColor
from datetime import datetime,timezone

class CreateChecklistItem(BaseModel):
    val: str =Field(min_length=3)
    position:int = Field(default=0)

class ShowChecklistItem(BaseModel):
    id:UUID
    val: str =Field(min_length=3)
    position:int 
    checked: bool 
    checked_by: UUID | None =Field(None)
    
class UpdateChecklistItem(BaseModel):
    id:UUID
    val: str | None = Field(None,min_length=3)
    position:int | None = Field(None)
    checked: bool | None = Field(default=False)
    checked_by: UUID | None =Field(default=None)
    
    

def isValidUpdate(checklistItem:UpdateChecklistItem):
    if checklistItem.val!=None and (len(checklistItem.val)<3):
        raise HTTPException(status.HTTP_406,"Invalid Name Field")
    else:
        return True
    

