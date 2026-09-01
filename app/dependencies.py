from typing import Annotated
from fastapi import Depends
import app.models.database as db 
from sqlmodel import Session
from app.models.tables import *

SessionDep=Annotated[Session,Depends(db.get_session)]


def validateEmail(email:str)->bool:
    return True
