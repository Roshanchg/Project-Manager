from sqlmodel import SQLModel, Field
import pydantic
import uuid
from enum import Enum
from uuid import UUID as UUID
from datetime import datetime,timezone
class User(SQLModel, table=True):
    __tablename__="users" # pyright: ignore[reportAssignmentType]
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    email: str = Field(nullable=False, index=True, unique=True)
    password_hash: str = Field(nullable=False)
    full_name: str = Field(nullable=False, min_length=3)

class Workspace(SQLModel, table=True):
    __tablename__="workspaces" # pyright: ignore[reportAssignmentType]
    id: UUID  = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(min_length=5, max_length=100, index=True)
    color: str = Field(default="#FFFFFF",
                      max_length=7,
                      min_length=7,
                      regex=r"^#[0-9a-fA-F]{6}$")

class WorkspaceRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"

class WorkspaceMember(SQLModel,table=True):
    __tablename__="workspace_member" # pyright: ignore[reportAssignmentType]
    workspace_id:UUID=Field(foreign_key="workspaces.id",primary_key=True,ondelete="CASCADE")
    user_id:UUID =Field(foreign_key="users.id",primary_key=True,ondelete="CASCADE")
    role:WorkspaceRole=Field(default=WorkspaceRole.MEMBER)

class Board(SQLModel, table=True):
    __tablename__="boards" # pyright: ignore[reportAssignmentType]
    id: UUID= Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(min_length=3)
    bg_img_path: str | None= Field()
    workspace_id: UUID = Field(foreign_key="workspaces.id",index=True,ondelete="CASCADE")


class Lists(SQLModel,table=True):
    __tablename__="lists" # pyright: ignore[reportAssignmentType]
    id:UUID =Field(default_factory=uuid.uuid4,primary_key=True)
    name:str =Field(min_length=3)
    board_id: UUID =Field(foreign_key="boards.id",index=True,ondelete="CASCADE")
    position:int =Field(default=0)

class Checklist(SQLModel,table=True):
    __tablename__="checklists" #pyright: ignore
    id: UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    name:str =Field(default="Checklist",min_length=1)
    card_id:UUID=Field(foreign_key="cards.id",index=True,ondelete="CASCADE")

class ChecklistItem(SQLModel,table=True):
    __tablename__="checklist_items" #pyright: ignore
    id: UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    checklist_id: UUID = Field(foreign_key="checklists.id",index=True,ondelete="CASCADE")
    val: str =Field(min_length=3)
    position:int = Field(default=0)
    checked: bool = Field(default=False)
    checked_by: UUID | None =Field(foreign_key="users.id",index=True,ondelete="SET NULL")

class Card(SQLModel,table=True):
    __tablename__="cards" # pyright: ignore[reportAssignmentType]
    id: UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    name:str =Field(min_length=3)
    desc:str|None = Field()
    severity: str = Field(default="Low",max_length=20)
    tag:str = Field(default="No Tag",max_length=20)
    due_date:datetime =Field(default_factory=lambda:datetime.now(timezone.utc))
    list_id: UUID =Field(foreign_key="lists.id",index=True,ondelete="CASCADE")