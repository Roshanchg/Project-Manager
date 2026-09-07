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
import app.schemas.checklists as CHECKLISTSCHEMA


import re 


userDep=Annotated[User,Depends(get_current_user)]
router=APIRouter()

@router.get("/checklists/{card_id}")
def getMyLists(session:SessionDep,user:userDep,card_id:UUID):
    cardChecklists=db.getChecklistsFromCard(session=session,cardId=card_id)
    checklists=[]
    for cl in checklists:
        checklists.append(
            CHECKLISTSCHEMA.ShowChecklist(
                id=cl.id,
                name=cl.name,
            )
        )
    return checklists
    
@router.post("/checklists/{card_id}/new")
def createNewList(session:SessionDep,user:userDep,crChecklist:CHECKLISTSCHEMA.CreateChecklist,card_id:UUID):
    workspace_id=db.getWorkspaceIdFrom(session=session,option=db.ID_OPTIONS.CARD,id=card_id)
    if not workspace_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"Could not find workspace for this card")
    if canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id):
        newChecklist=Checklist(
            id=uuid.uuid4(),
            **crChecklist.model_dump(),
            card_id=card_id
        )
        db.insertChecklist(session=session,checklist=newChecklist)
        return {"message":"Added new Checklist"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have enough permission to add a checklist on this workspace.")


@router.put("/checklists/{card_id}/update")
def updateList(session:SessionDep,user:userDep,upChecklist:CHECKLISTSCHEMA.UpdateChecklist,card_id:UUID):
    if CHECKLISTSCHEMA.isValidUpdate(upChecklist):
        workspace_id=db.getWorkspaceIdFrom(session=session,option=db.ID_OPTIONS.CARD,id=card_id)
        if not workspace_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,"Could not find workspace for this card")
        if canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id):
            db.updateChecklist(session=session,checklistId=upChecklist.id,data=upChecklist.model_dump(
                exclude={"id","card_id"},
                exclude_none=True
            ))
            return {"message":"Checklist Updated"}
        else: 
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have enough permission to edit Checklists in this workspace.")
    else:
        raise HTTPException(406,"Invalid Update Field")

@router.delete("/checklists/{card_id}/delete")
def removeList(session:SessionDep,user:userDep,card_id:UUID,checklist_id:UUID):
    workspace_id=db.getWorkspaceIdFrom(session=session,option=db.ID_OPTIONS.CARD,id=card_id)
    if not workspace_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"Could not find workspace for this card")
    if(canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id)):
        db.removeChecklist(session=session,checklistId=card_id)
        return {"message":"Removed the Checklist"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have the permission to remove Checklists in this workspace.")