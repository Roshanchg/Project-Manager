from fastapi import FastAPI,Depends,Query,APIRouter,Request,HTTPException,status
from typing import Annotated
from sqlmodel import Session
import app.models.database as db
import app.schemas.users as USERSCHEMA
from app import config as config
import app.services.authenticator as Auth
from app.dependencies import SessionDep
from uuid import UUID
from fastapi.responses import Response
from app.api.helpers import get_current_user,get_user_from_ref_token
from app.models.tables import *
from app.services import sessions as ses

router=APIRouter()

@router.get("/users")
def getUsers(session:SessionDep,
                   limit:Annotated[int,Query(le=10)]=10,
                   offset:Annotated[int,Query(ge=0)]=0):
    return db.getUsers(session=session,limit=limit,offset=offset)


@router.post("/register")
def register(session:SessionDep,user_model:USERSCHEMA.CreateUser):
    Auth.RegisterUser(session=session,formUser=user_model)
    return {"success":True}

@router.delete("/deleteUser")
def removeUser(session:SessionDep,userId:UUID):
    db.removeUser(session=session,userId=userId)
    return {"success":True}

@router.put("/updateUser")
def updateUser(session:SessionDep,user:USERSCHEMA.UpdateUser):
    
    return user
@router.get("/me")
def get_me(session:SessionDep,current_user:Annotated[User,Depends(get_current_user)]):
    return current_user
    
@router.post("/login")
def login(session:SessionDep,response:Response,credentials:USERSCHEMA.LoginUser):
    # Auth here
    user=Auth.authenticate(session=session,
                           email=credentials.email,
                           password=credentials.password)
    if not user:
        raise HTTPException(404,"User Does Not Exist")
    tokenTuple=ses.create_new_session(session=session,userId=user.id) 
    if not tokenTuple:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE,"Could not create new session token")
    accessToken,refreshToken=tokenTuple
    response.set_cookie("access_token",accessToken,httponly=True,secure=True,max_age=900)
    response.set_cookie("refresh_token",refreshToken,httponly=True,secure=True,max_age=604800)
    return {"message":"Logged In"}

@router.get("/refresh")
def refreshAuth(session:SessionDep,response:Response,request:Request,current_user:Annotated[User,Depends(get_user_from_ref_token)]):    
    ref_token=request.cookies.get("refresh_token")
    if not ref_token:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,"No Refresh Token In Cookies")
    newaccessToken=ses.refresh_access_token(session=session,refresh_token=ref_token)
    if not newaccessToken:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,"Unable to Refresh the token")
    response.set_cookie("access_token",newaccessToken,httponly=True,secure=True,max_age=900)
    return {"message":"New Access Token Set"}

@router.get("/logout")
def logoutUser(session:SessionDep,request:Request,response:Response):
    refreshToken=request.cookies.get("refresh_token")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    if refreshToken:
        ses.removeSessionFromRef(session=session,refresh_token=refreshToken)
    return {"message":"Logged Out"}
    
