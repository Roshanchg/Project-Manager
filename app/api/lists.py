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
import uuid 
import app.schemas.lists as LISTSCHEMA


import re 


userDep=Annotated[User,Depends(get_current_user)]
router=APIRouter()

@router.get("/lists/{board_id}")
def getMyLists(session:SessionDep,user:userDep,board_id:UUID):
    boardLists=db.getAllListOfBoard(session=session,boardId=board_id)
    lists=[]
    for l in boardLists:
        lists.append(
            LISTSCHEMA.ShowList(
                id=l.id,
                name=l.name,
                position=l.position
            )
        )
    return boardLists
    
@router.post("/lists/{board_id}/new")
def createNewList(session:SessionDep,user:userDep,crList:LISTSCHEMA.CreateList,board_id:UUID):
    workspace_id=db.getWorkspaceIdFrom(session=session,option=db.ID_OPTIONS.BOARD,id=board_id)
    if not workspace_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"Could not find workspace for this board")
    if canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id):
        newList=Lists(
            id=uuid.uuid4(),
            **crList.model_dump(),
            board_id=board_id
        )
        db.insertList(session=session,_list=newList)
        return {"message":"Added new list"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have enough permission to add a list on this workspace.")


@router.put("/list/{board_id}/update")
def updateList(session:SessionDep,user:userDep,upList:LISTSCHEMA.UpdateList,board_id:UUID):
    if LISTSCHEMA.isValidUpdate(upList):
        workspace_id=db.getWorkspaceIdFrom(session=session,option=db.ID_OPTIONS.BOARD,id=board_id)
        if not workspace_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,"Could not find workspace for this board")
        if canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id):
            db.updateList(session=session,listId=upList.id,data=upList.model_dump(
                exclude={"id","board_id"},
                exclude_none=True
            ))
            return {"message":"Board Updated"}
        else: 
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have enough permission to edit lists in this workspace.")
    else:
        raise HTTPException(406,"Invalid Update Field")

@router.delete("/list/{board_id}/delete")
def removeList(session:SessionDep,user:userDep,board_id:UUID,list_id:UUID):
    workspace_id=db.getWorkspaceIdFrom(session=session,option=db.ID_OPTIONS.BOARD,id=board_id)
    if not workspace_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"Could not find workspace for this board")
    if(canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id)):
        db.removeList(session=session,listId=list_id)
        return {"message":"Removed the List"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have the permission to remove Lists in this workspace.")