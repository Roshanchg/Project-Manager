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
import app.schemas.checklistItems as ITEMSCHEMA


import re 


userDep=Annotated[User,Depends(get_current_user)]
router=APIRouter()

@router.get("/checklistitems/{checklist_id}")
def getMyLists(session:SessionDep,user:userDep,checklist_id:UUID):
    checklistChecklistItems=db.getCheckListItemsOfChecklist(session=session,checklistId=checklist_id)
    items=[]
    for l in checklistChecklistItems:
        items.append(
            ITEMSCHEMA.ShowChecklistItem(
                id=l.id,
                val=l.val,
                position=l.position,
                checked=l.checked,
                checked_by=l.checked_by
            )
        )
    return items
    
@router.post("/checklistitems/{checklist_id}/new")
def createNewList(session:SessionDep,user:userDep,crChecklistItem:ITEMSCHEMA.CreateChecklistItem,checklist_id:UUID):
    workspace_id=db.getWorkspaceIdFrom(session=session,option=db.ID_OPTIONS.CHECKLIST,id=checklist_id)
    if not workspace_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"Could not find workspace for this checklist")
    if canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id):
        newChecklistItem=ChecklistItem(
            id=uuid.uuid4(),
            **crChecklistItem.model_dump(),
            checklist_id=checklist_id
        )
        db.insertChecklistItem(session=session,checklistItem=newChecklistItem)
        return {"message":"Added new ChecklistItem"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have enough permission to add a checklist item on this workspace.")


@router.put("/checklistitems/{checklist_id}/update")
def updateList(session:SessionDep,user:userDep,upChecklistItem:ITEMSCHEMA.UpdateChecklistItem,checklist_id:UUID):
    if ITEMSCHEMA.isValidUpdate(upChecklistItem):
        workspace_id=db.getWorkspaceIdFrom(session=session,option=db.ID_OPTIONS.CHECKLIST,id=checklist_id)
        if not workspace_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,"Could not find workspace for this checklist")
        if canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id):
            db.updateChecklistItem(session=session,checklistItemId=upChecklistItem.id,data=upChecklistItem.model_dump(
                exclude={"id","checklist_id"},
                exclude_none=True
            ))
            return {"message":"Checklist Item Updated"}
        else: 
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have enough permission to edit checklist items in this workspace.")
    else:
        raise HTTPException(406,"Invalid Update Field")

@router.delete("/checklistitems/{checklist_id}/delete")
def removeList(session:SessionDep,user:userDep,checklist_id:UUID,checklistitem_id:UUID):
    workspace_id=db.getWorkspaceIdFrom(session=session,option=db.ID_OPTIONS.CHECKLIST,id=checklist_id)
    if not workspace_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"Could not find workspace for this checklist")
    if(canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id)):
        db.removeChecklistItem(session=session,checklistItemId=checklistitem_id)
        return {"message":"Removed the checklist item"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have the permission to remove checklist items in this workspace.")