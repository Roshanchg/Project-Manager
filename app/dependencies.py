from typing import Annotated
from fastapi import Depends
import app.models.database as db 
from sqlmodel import Session
from app.models.tables import *
import re

SessionDep=Annotated[Session,Depends(db.get_session)]

def validateEmail(email:str)->bool:
    return True

def validateColor(color:str)->bool:
    colorPattern=r"^#[0-9a-fA-F]{6}$"
    return bool(re.fullmatch(colorPattern,string=color))
