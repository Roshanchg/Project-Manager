from contextlib import asynccontextmanager
from sqlmodel import SQLModel,create_engine,Session
from fastapi import FastAPI,APIRouter,Depends
from app import config as config
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.models import database
from typing import Annotated
from app.models import database as db

SessionDep=Annotated[Session,Depends(db.get_session)]
      
    
@asynccontextmanager
async def lifespan(app:FastAPI):
    db.init_db()
    yield
    
    
app=FastAPI(
    title=config.PROJECT_NAME,
    lifespan=lifespan
)
app.mount("/static",
          StaticFiles(directory=config.STATIC_DIR))

templates=Jinja2Templates(directory=config.TEMPLATES_DIR)
