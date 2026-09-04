from pydantic import Field,BaseModel
from uuid import UUID
from app.models.database import WorkspaceRole
from fastapi import HTTPException,status
from app.dependencies import validateColor

class CreateBoard(BaseModel):
    name:str=Field(default="Untitled",min_length=5,max_length=100)
    bg_img_path:str|None= Field(default=None)


class ShowBoard(BaseModel):
    id:UUID
    name:str
    bg_img_path: str|None
    
class UpdateBoard(BaseModel):
    id:UUID
    name:str| None=Field(None,min_length=5,max_length=100)
    bg_img_path:str | None= Field(None)
    
    

def isValidUpdate(board:UpdateBoard):
    if board.name!=None and (len(board.name)<5 and len(board.name)>100):
        raise HTTPException(status.HTTP_406,"Invalid Name Field")
    else:
        return True
    
    
