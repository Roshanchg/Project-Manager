from fastapi import FastAPI,Depends,Query,APIRouter,Request,HTTPException,status
from typing import Annotated
from sqlmodel import Session
import app.models.database as db
import app.schemas.users as USERSCHEMA
from app import config as config
import app.services.authenticator as Auth
from app.dependencies import SessionDep,validateColor
from uuid import UUID
from fastapi.responses import Response
from app.api.helpers import get_current_user,get_user_from_ref_token,canRemoveWorkspace,canUpdateWorkspace
from app.models.tables import *
from app.services import sessions as ses
import app.schemas.workspaces as WORKSPACESCHEMA
import uuid 
import re 

router=APIRouter()

userDep=Annotated[User,Depends(get_current_user)]

@router.get("/user/Workspace")
def getMyWorkspaces(session:SessionDep,user:userDep):
    userWorkspaces=db.getWorkspacesFromUserId(session=session,userId=user.id)
    workspaceList=[]
    for (id,name,color,role) in userWorkspaces:
        workspaceList.append(
            WORKSPACESCHEMA.ShowWorkspace(
                id=id,
                name=name,color=color,role=WorkspaceRole(role)
            )
        )
    return workspaceList
    
@router.post("/user/Workspace/new")
def createNewWorkspace(session:SessionDep,user:userDep,crWorkspace:WORKSPACESCHEMA.CreateWorkspace):
    totalWorkspaces=db.getUserWorkspaceCount(session=session,userId=user.id)
    if totalWorkspaces>=5:
        raise HTTPException(status.HTTP_403_FORBIDDEN,"Only 5 workspaces are allowed per user.")
    newWorkspace=Workspace(
        id=uuid.uuid4(),
        **crWorkspace.model_dump()
    )
    role=WorkspaceRole.OWNER
    newWorkspaceMember=WorkspaceMember(
        workspace_id=newWorkspace.id,
        user_id=user.id,
        role=role
    )
    db.insertWorkspaceMember(session=session,workspaceMember=newWorkspaceMember,workspace=newWorkspace)
    
    return {"message":"Added new workspace"}


@router.put("/user/Workspace/update")
def updateWorkspace(session:SessionDep,user:userDep,upWorkspace:WORKSPACESCHEMA.UpdateWorkspace):
    if WORKSPACESCHEMA.validUpdateWorkspace(upWorkspace=upWorkspace):
        if canUpdateWorkspace(session=session,user_id=user.id,workspace_id=upWorkspace.id):
            db.updateWorkspace(session=session,workspaceId=upWorkspace.id,data=upWorkspace.model_dump(
                exclude={"id"},
                exclude_none=True
            ))
            return {"message":"Workspace Updated"}
        else: 
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have enough permission to edit this workspace.")

@router.delete("/users/Workspace/delete")
def removeWorkspace(session:SessionDep,user:userDep,workspace_id:UUID):
    if(canRemoveWorkspace(session=session,user_id=user.id,workspace_id=workspace_id)):
        db.removeWorkspace(session=session,workspaceId=workspace_id)
        return {"message":"Removed the workspace"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have the permission to remove this workspace.")