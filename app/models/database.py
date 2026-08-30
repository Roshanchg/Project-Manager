from fastapi import Depends

import app.config as config
from sqlmodel import create_engine,SQLModel,Session,select
from app.models.tables import * 
from typing import Annotated

_engine=None
def get_engine():
    global _engine
    if _engine==None:
        if(config.DB_ENGINE_NAME=="sqlite"):
            sqlite_file_name=config.DB_FILE_NAME
            sqlite_url=f"sqlite:///{sqlite_file_name}"
            connect_args={"check_same_thread":False}
            engine=create_engine(sqlite_url,connect_args=connect_args)
            _engine=engine
    return _engine

def init_db():
    engine=get_engine
    if(engine==None):
        raise(BaseException("No Engine Found"))
    else:
        SQLModel.metadata.create_all(engine)  # type: ignore 
    

def get_session():
    engine=get_engine()
    with Session(engine) as session:
        yield session
        
SessionDep=Annotated[Session,Depends(get_session)]

def getUsers(session:Session,offset:int=0,limit:int =10,):
    users=session.exec(select(User).offset(offset).limit(limit)).all()
    return users

def getUserFromId(session:Session,userID:UUID)->User| None:
    user=session.get(User,userID)
    return user

def getUserFromEmail(session:Session,email:str)->User|None:
    if len(email)<5:
        return
    user=session.exec(select(User).where(User.email==email)).first()
    return user

def removeUser(session:Session,userId:UUID):
    user=getUserFromId(session=session,userID=userId)
    if(user==None):
        return
    session.delete(user)
    session.commit()

def updateUser(session:Session,userId:UUID,data:dict)->User|None:
    user=getUserFromId(session=session,userID=userId)
    if user==None:
        return
    allowedKeys={"email","password_hash","full_name"}
    filtered= {k:v for k,v in data.items() if k in allowedKeys}
    
    for k,v in filtered.items():
        setattr(user,k,v)
    session.commit()
    session.refresh(user)
    return user
    

def getWorkspaces(session:Session,offset:int =0,limit: int=10):
    workspaces=session.exec(select(Workspace).offset(offset).limit(limit)).all()
    return workspaces

def getWorkspaceFromId(session:Session,workspaceId:UUID)->Workspace |None:
    workspace=session.get(Workspace,workspaceId)
    return workspace

def removeWorkspace(session:Session,workspaceId:UUID):
    workspace=getWorkspaceFromId(session=session,workspaceId=workspaceId)
    if workspace==None:
        return
    session.delete(workspace)
    session.commit()

def updateWorkspace(session:Session,workspaceId:UUID,data:dict)->Workspace|None:
    workspace=getWorkspaceFromId(session=session,workspaceId=workspaceId)
    if workspace==None:
        return
    allowedKeys={"name","color"}
    filtered= {k:v for k,v in data.items() if k in allowedKeys}
    for k,v in filtered.items():
        setattr(workspace,k,v)
    session.commit()
    session.refresh(workspace)
    return workspace



def getWorkspaceMember(session:Session,offset:int =0,limit: int=10):
    workspace_members=session.exec(select(WorkspaceMember).offset(offset).limit(limit)).all()
    return workspace_members

def getWorkmemberFromUserId(session:Session,userId:UUID):
    stmt=select(User.id,User.email,User.full_name).join(WorkspaceMember).join(Workspace).where(WorkspaceMember.user_id==userId)
    userWorkspaces=session.exec(stmt).all()
    return userWorkspaces
    
def getWorkspaceMemberFromID(session:Session,userId:UUID,workspaceId:UUID)->WorkspaceMember|None:
    workspaceMember= session.get(WorkspaceMember,(WorkspaceMember.user_id==userId,WorkspaceMember.workspace_id==workspaceId) )
    return workspaceMember

def removeWorkspaceMember(session:Session,userId:UUID,workspaceId:UUID):
    workspaceMember=getWorkspaceMemberFromID(session=session,userId=userId,workspaceId=workspaceId)
    if workspaceMember==None:
        return
    session.delete(workspaceMember)
    session.commit()

def updateWorkspaceMember(session:Session,userId:UUID,workspaceId:UUID,data:dict)->WorkspaceMember|None:
    workspaceMember=getWorkspaceMemberFromID(session=session,userId=userId,workspaceId=workspaceId)
    if workspaceMember==None:
        return
    allowedKeys={"role"}
    filtered= {k:v for k,v in data.items() if k in allowedKeys}
    for k,v in filtered.items():
        if k=="role":
            if v not in WorkspaceRole:
                continue    
        setattr(workspaceMember,k,v)
    session.commit()
    session.refresh(workspaceMember)
    return workspaceMember




def getBoards(session:Session,offset:int =0,limit: int=10):
    boards=session.exec(select(Board).offset(offset).limit(limit)).all()
    return boards

def getBoardFromId(session:Session,boardId:UUID)-> Board|None:
    board=session.get(Board,Board.id==boardId)
    return board

def getBoardsOfWorkspace(session:Session,workspaceId:UUID):
    stmt=select(Board).where(Board.workspace_id==workspaceId)
    boards=session.exec(stmt).all()
    return boards

def removeBoard(session:Session,boardId:UUID):
    board=getBoardFromId(session=session,boardId=boardId)
    if board==None:
        return
    session.delete(board)
    session.commit()

def updateBoard(session:Session,boardId:UUID,data:dict)->Board|None:
    board=getBoardFromId(session=session,boardId=boardId)
    if board==None:
        return
    allowedKeys={"name","bg_img_path","workspace_id"}
    filtered= {k:v for k,v in data.items() if k in allowedKeys}
    for k,v in filtered.items():
        setattr(board,k,v)
    session.commit()
    session.refresh(board)
    return board



def getLists(session:Session,offset:int =0,limit: int=10):
    lists=session.exec(select(Lists).offset(offset).limit(limit)).all()
    return lists

def getListFromId(session:Session,listId:UUID)->Lists|None:
    _list=session.get(Lists,Lists.id==listId)
    return _list

def getAllListOfBoard(session:Session,boardId:UUID):
    stmt=select(Lists).where(Lists.board_id==boardId)
    _lists=session.exec(stmt).all()
    return _lists

def removeList(session:Session,listId:UUID):
    _list=getListFromId(session=session,listId=listId)
    if _list==None:
        return
    session.delete(_list)
    session.commit()

def updateList(session:Session,listId:UUID,data:dict)->Lists|None:
    _list=getListFromId(session=session,listId=listId)
    if _list==None:
        return
    allowedKeys={"name","board_id","position"}
    filtered= {k:v for k,v in data.items() if k in allowedKeys}
    for k,v in filtered.items():
        setattr(_list,k,v)
    session.commit()
    session.refresh(_list)
    return _list




def getCards(session:Session,offset:int =0,limit: int=10):
    cards=session.exec(select(User).offset(offset).limit(limit)).all()
    return cards

def getCardFromId(session:Session,cardId:UUID)->Card|None:
    card=session.get(Card,Card.id==cardId)
    return card

def getCardsFromList(session:Session,listId:UUID):
    stmt=select(Card).where(Card.list_id==listId)
    cards=session.exec(stmt).all()
    return cards

def removeCard(session:Session,cardId:UUID):
    card=getCardFromId(session=session,cardId=cardId)
    if card==None:
        return
    session.delete(card)
    session.commit()

def updateCard(session:Session,cardId:UUID,data:dict)->Card|None:
    card=getCardFromId(session=session,cardId=cardId)
    if card==None:
        return
    allowedKeys={"name","desc","severity","tag","due_date","list_id"}
    filtered= {k:v for k,v in data.items() if k in allowedKeys}
    for k,v in filtered.items():
        setattr(card,k,v)
    session.commit()
    session.refresh(card)
    return card




def getChecklists(session:Session,offset:int =0,limit: int=10):
    checklists=session.exec(select(Checklist).offset(offset).limit(limit)).all()
    return checklists

def getChecklistFromId(session:Session,checklistId:UUID)->Checklist |None:
    return session.get(Checklist,Checklist.id==checklistId)

def getChecklistsFromCard(session:Session,cardId:UUID):
    stmt=select(Checklist).where(Checklist.card_id==cardId)
    return session.exec(stmt)

def removeChecklist(session:Session,checklistId:UUID):
    checklist=getChecklistFromId(session=session,checklistId=checklistId)
    if checklist==None:
        return
    session.delete(checklist)
    session.commit()

def updateCHecklist(session:Session,checklistId:UUID,data:dict)->Checklist|None:
    checklist=getChecklistFromId(session=session,checklistId=checklistId)
    if checklist==None:
        return
    allowedKeys={"name","card_id"}
    filtered= {k:v for k,v in data.items() if k in allowedKeys}
    for k,v in filtered.items():
        setattr(checklist,k,v)
    session.commit()
    session.refresh(checklist)
    return checklist






def getCheclistItems(session:Session,offset:int =0,limit: int=10):
    checklist_items=session.exec(select(ChecklistItem).offset(offset).limit(limit)).all()
    return checklist_items

def getChecklistItemFromId(session:Session,checklistItemId:UUID)->ChecklistItem|None:
    return session.get(ChecklistItem,ChecklistItem.id==checklistItemId)

def getCheckListItemsOfChecklist(session:Session,checklistId:UUID):
    stmt=select(ChecklistItem,ChecklistItem.checklist_id==checklistId)
    return session.exec(stmt)

def removeChecklistItem(session:Session,checklistItemId:UUID):
    checklistItem=getChecklistItemFromId(session=session,checklistItemId=checklistItemId)
    if checklistItem==None:
        return
    session.delete(checklistItem)
    session.commit()

def updateChecklistItem(session:Session,checklistItemId:UUID,data:dict)->ChecklistItem|None:
    checklistItem=getChecklistItemFromId(session=session,checklistItemId=checklistItemId)
    if checklistItem==None:
        return
    allowedKeys={"checklist_id","val","position","checked","checked_by"}
    filtered= {k:v for k,v in data.items() if k in allowedKeys}
    for k,v in filtered.items():
        setattr(checklistItem,k,v)
    session.commit()
    session.refresh(checklistItem)
    return checklistItem

