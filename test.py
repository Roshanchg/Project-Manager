from fastapi import FastAPI,Query,Body,Cookie,Header,Form,File,UploadFile,HTTPException,Depends,Request
from pydantic import BaseModel,Field
from enum import Enum
from typing import Annotated,Literal
from sqlmodel import Field,Session,SQLModel,create_engine,select
import os
import aiofiles
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates

class Hero(SQLModel,table=True):
    id:int | None=Field(default=None,primary_key=True)
    name: str=Field(index=True)
    age:int | None=Field(default=None,index=True)
    secret_name:str
    
sqlite_file_name="database.db"
sqlite_url=f"sqlite:///{sqlite_file_name}"

connect_args={"check_same_thread":False}
engine=create_engine(sqlite_url,connect_args=connect_args)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
SessionDep=Annotated[Session,Depends(get_session)]

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_table()
    yield

app=FastAPI(lifespan=lifespan)
app.mount("/frontend/static",StaticFiles(directory="frontend/static"),name="static")

templates=Jinja2Templates(directory="frontend/html")

@app.get("/",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse(name="index.html",request=request)


class Item(BaseModel):
    name:str
    price:float
    is_offer:bool | None =None

class ValidName(str,Enum):
    roshan="roshan"
    noroshan="noroshan"

class FilterParams(BaseModel):
    model_config={"extra":"forbid"}
    limit:int=Field(100,gt=1,le=100)
    order_by:Literal["created","updated"]
    tags:list[str]=[]



@app.post("/heroes/")
def create_hero(hero:Hero,session:SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/heroes/")
def read_heroes(session:SessionDep,
                offset:int=0,
                limit:Annotated[int,Query(le=10)]=10,)-> list[Hero]:
    heroes=session.exec(select(Hero).offset(offset).limit(limit)).all()
    print(type(heroes))
    return heroes # pyright: ignore[reportReturnType]

@app.get("/error/")
async def showErr():
    raise HTTPException(status_code=400,detail="Fuck You")

@app.post("/fileUp/")
async def uploadFile(file:UploadFile):
    os.makedirs("uploads",exist_ok=True)
    file_path=f"uploads/{file.filename}"
    async with aiofiles.open(file_path,'wb')as out_file:
        content=await file.read()
        await out_file.write(content)    
    return None

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id:int,session:SessionDep):
    hero=session.get(Hero,hero_id)
    if not hero:
        raise HTTPException(status_code=404,detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok":True}

@app.post("/login/")
async def login(username:Annotated[str,Form()],password:Annotated[str,Form()]):
    return {"username":username}

@app.get("/head/")
async def head(user_agent:Annotated[str|None,Header()]=None):
    return {"User-Agent":user_agent}


@app.post("/filter/")
async def filter_shit(filter_query:Annotated[FilterParams,Query()],body:Annotated[int,Body()]):
    return filter_query,body

@app.put("/items/{item_id}")
def update_item(item_id:int,item:Item):
    return {**item.model_dump(),"item_id":item_id}

@app.get("/test/")
async def test_func(q:Annotated[str|None,Query(title="Random Title",max_length=50)]=None):
    return {'q':q}


@app.get("/items/")
async def read_items(q:Annotated[list[str]|None,Query()]=None):    
    return q

@app.get("/cookie/")
async def cook(ads_id:Annotated[str|None,Cookie()]=None):
    return {'ads_id':ads_id}