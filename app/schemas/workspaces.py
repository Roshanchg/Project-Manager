from pydantic import Field,BaseModel
from uuid import UUID
from app.models.database import WorkspaceRole
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
    name:str
    color:str
    