from fastapi import Request
from typing import Annotated
from app.dependencies import SessionDep
from fastapi import HTTPException,status
from jose import jwt,JWTError
from app.config import SECRET_KEY, ALGORITHM
from uuid import UUID
from app.models import database as db
from app.models.tables import *
import app.services.sessions as ses
from sqlmodel import Session
import app.schemas.users as USERSCHEMA
import app.schemas.workspaces as WORKSPACESCHEMA

def get_current_user(request:Request,session:SessionDep)->User:
    token=request.cookies.get("access_token")
    if not token:
        user=get_user_from_ref_token(request=request,session=session)
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Not Authenticated")
        else:
            return user
    try: 
        user_id=ses.validate_token(token=token)
        if not user_id:
            raise HTTPException(401,"User not found")
        user=db.getUserFromId(session=session,userID=user_id)
        if not user:
            raise HTTPException(401,"User not found")
        return user
    except (JWTError,ValueError):
        raise HTTPException(401,"Invalid Token")


def get_user_from_ref_token(request:Request,session:SessionDep)->User:
    token=request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Not Authenticated")
    try: 
        user_id=ses.validate_token(token=token)
        if not user_id:
            raise HTTPException(401,"User not found")
        user=db.getUserFromId(session=session,userID=user_id)
        if not user:
            raise HTTPException(401,"User not found")
        return user
    except (JWTError,ValueError):
        raise HTTPException(401,"Invalid Token")
    

    


def canRemoveWorkspace(session:Session,user_id:UUID,workspace_id:UUID)->bool:
    workspace=db.getWorkspaceMemberFromID(session=session,userId=user_id,workspaceId=workspace_id)
    if not workspace:
        return False
    if workspace.role!=WorkspaceRole.OWNER:
        return  False
    return True

def canUpdateWorkspace(session:Session,user_id:UUID,workspace_id:UUID)->bool:
    workspace=db.getWorkspaceMemberFromID(session=session,userId=user_id,workspaceId=workspace_id)
    if not workspace:
        return False
    if (workspace.role==WorkspaceRole.OWNER)or (workspace.role==WorkspaceRole.ADMIN):
        return  True
    return False



