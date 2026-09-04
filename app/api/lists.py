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
import app.schemas.boards as BOARDSCHEMA


import re 


userDep=Annotated[User,Depends(get_current_user)]

router=APIRouter()

@router.get("/boards/{workspace_id}")
def getMyBoards(session:SessionDep,user:userDep,workspace_id:UUID):
    userBoards=db.getBoardsOfWorkspace(session=session,workspaceId=workspace_id)
    boardLists=[]
    for board in userBoards:
        boardLists.append(
            BOARDSCHEMA.ShowBoard(
                id=board.id,
                name=board.name,
                bg_img_path=board.bg_img_path
            )
        )
    return boardLists
    
@router.post("/boards/{workspace_id}/new")
def createNewBoard(session:SessionDep,user:userDep,crBoard:BOARDSCHEMA.CreateBoard,workspace_id:UUID):
    if canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id):
        newBoard=Board(
            id=uuid.uuid4(),
            **crBoard.model_dump(),
            workspace_id=workspace_id
        )
        db.insertBoard(session=session,board=newBoard)
        return {"message":"Added new Board"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have enough permission to add board on this workspace.")


@router.put("/boards/{workspace_id}/update")
def updateBoard(session:SessionDep,user:userDep,upBoard:BOARDSCHEMA.UpdateBoard,workspace_id:UUID):
    if BOARDSCHEMA.isValidUpdate(board=upBoard):
        if canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id):
            db.updateBoard(session=session,boardId=upBoard.id,data=upBoard.model_dump(
                exclude={"id","workspace_id"},
                exclude_none=True
            ))
            return {"message":"Board Updated"}
        else: 
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have enough permission to edit boards in this workspace.")
    else:
        raise HTTPException(406,"Invalid Update Field")

@router.delete("/boards/{workspace_id}/delete")
def removeBoard(session:SessionDep,user:userDep,workspace_id:UUID,board_id:UUID):
    if(canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id)):
        db.removeBoard(session=session,boardId=board_id)
        return {"message":"Removed the board"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have the permission to remove boards in this workspace.")