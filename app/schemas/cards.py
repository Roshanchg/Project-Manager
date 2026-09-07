from pydantic import Field,BaseModel
from uuid import UUID
from app.models.database import WorkspaceRole
from fastapi import HTTPException,status
from app.dependencies import validateColor
from datetime import datetime,timezone

class CreateCard(BaseModel):
    name:str=Field(min_length=3,max_length=100)
    desc:str|None = Field()
    severity: str = Field(default="Low",max_length=20)
    tag:str = Field(default="No Tag",max_length=20)
    due_date:datetime =Field()

class ShowCard(BaseModel):
    id:UUID
    name:str
    desc:str |None
    severity:str
    tag:str | None
    due_date:datetime
    
class UpdateCard(BaseModel):
    id:UUID
    name:str|None=Field(None,min_length=3,max_length=100)
    desc:str|None = Field()
    severity: str|None = Field(default="Low",max_length=20)
    tag:str|None = Field(default="No Tag",max_length=20)
    due_date:datetime |None =Field()
    
    

def isValidUpdate(card:UpdateCard):
    if card.name!=None and (len(card.name)<3 and len(card.name)>100):
        raise HTTPException(status.HTTP_406,"Invalid Name Field")
    if card.severity!=None and len(card.severity)>20:
        raise HTTPException(status.HTTP_406,"Invalid Severity Field")
    if card.tag!=None and len(card.tag)>20:
        raise HTTPException(status.HTTP_406,"Invalid Tag Field")
    else:
        return True
    

