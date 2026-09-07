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
import app.schemas.cards as CARDSCHEMA


import re 


userDep=Annotated[User,Depends(get_current_user)]
router=APIRouter()

@router.get("/cards/{list_id}")
def getMyLists(session:SessionDep,user:userDep,list_id:UUID):
    listCards=db.getCardsFromList(session=session,listId=list_id)
    cards=[]
    for l in listCards:
        cards.append(
            CARDSCHEMA.ShowCard(
                id=l.id,
                name=l.name,
                desc=l.desc,
                severity=l.severity,
                tag=l.tag,
                due_date=l.due_date
            )
        )
    return cards
    
@router.post("/cards/{list_id}/new")
def createNewList(session:SessionDep,user:userDep,crCard:CARDSCHEMA.CreateCard,list_id:UUID):
    workspace_id=db.getWorkspaceIdFrom(session=session,option=db.ID_OPTIONS.LIST,id=list_id)
    if not workspace_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"Could not find workspace for this list")
    if canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id):
        newCard=Card(
            id=uuid.uuid4(),
            **crCard.model_dump(),
            list_id=list_id
        )
        db.insertCard(session=session,card=newCard)
        return {"message":"Added new Card"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have enough permission to add a card on this workspace.")


@router.put("/cards/{list_id}/update")
def updateList(session:SessionDep,user:userDep,upCard:CARDSCHEMA.UpdateCard,list_id:UUID):
    if CARDSCHEMA.isValidUpdate(upCard):
        workspace_id=db.getWorkspaceIdFrom(session=session,option=db.ID_OPTIONS.LIST,id=list_id)
        if not workspace_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,"Could not find workspace for this list")
        if canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id):
            db.updateCard(session=session,cardId=upCard.id,data=upCard.model_dump(
                exclude={"id","list_id"},
                exclude_none=True
            ))
            return {"message":"Card Updated"}
        else: 
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have enough permission to edit cards in this workspace.")
    else:
        raise HTTPException(406,"Invalid Update Field")

@router.delete("/cards/{list_id}/delete")
def removeList(session:SessionDep,user:userDep,list_id:UUID,card_id:UUID):
    workspace_id=db.getWorkspaceIdFrom(session=session,option=db.ID_OPTIONS.LIST,id=list_id)
    if not workspace_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"Could not find workspace for this list")
    if(canUpdateWorkspace(session=session,user_id=user.id,workspace_id=workspace_id)):
        db.removeCard(session=session,cardId=card_id)
        return {"message":"Removed the Card"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"User doesnot have the permission to remove Cards in this workspace.")