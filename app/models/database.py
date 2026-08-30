from fastapi import Depends

import app.config as config
from sqlmodel import create_engine,SQLModel,Session
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
   pass

def get_session():
    engine=get_engine()
    with Session(engine) as session:
        yield session

def create_db():
    SQLModel.metadata.create_all(engine)  