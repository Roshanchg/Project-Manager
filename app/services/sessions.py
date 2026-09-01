from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from app.config import SECRET_KEY,ALGORITHM
from uuid import UUID
from app.models import database as db
from sqlmodel import Session
from app.models.tables import Refresh_Tokens as TokenTable

def create_access_token(user_id:UUID)->str:
    expire=datetime.now(timezone.utc)+timedelta(minutes=15)
    return jwt.encode(
        {"sub":str(user_id),"exp":expire},
        SECRET_KEY, # type: ignore
        algorithm=ALGORITHM # type: ignore
    )

def create_refresh_token(user_id:UUID)->str:
    expire=datetime.now(timezone.utc)+timedelta(days=7)
    return jwt.encode(
        {"sub":str(user_id),"exp":expire},
        SECRET_KEY, #type: ignore
        algorithm=ALGORITHM #type: ignore
    )
    

def validate_token(token:str)->UUID|None:
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]) #type: ignore
        user_id=UUID(payload.get("sub"))
        if not user_id:
            return None
        return user_id
    except JWTError,ValueError:
        return None

def refresh_access_token(session:Session,refresh_token:str)->str |None:
    user_id=validate_token(refresh_token)
    if not user_id:
        return 
    refTokenObj=db.getTokenObjOfToken(session=session,tokenString=refresh_token)
    if not refTokenObj:
        return 
    expires_aware=refTokenObj.expires_at.replace(tzinfo=timezone.utc)
    if expires_aware<=datetime.now(timezone.utc):
        db.removeRefreshToken(session=session,refreshTokenId=refTokenObj.id)
        return 
    newAccessToken=create_access_token(user_id=user_id)
    return newAccessToken
    
    
def create_new_session(session:Session,userId:UUID)->tuple[str,str]|None:
    accessTokenStr=create_access_token(user_id=userId)
    refreshTokenStr=create_refresh_token(user_id=userId)
    refTokenObj=TokenTable(
        token=refreshTokenStr,
        user_id=userId,
        expires_at=datetime.now(timezone.utc)+timedelta(days=7)
    )
    db.insertRefreshToken(session=session,refreshToken=refTokenObj)
    return (accessTokenStr,refreshTokenStr)

def removeSessionFromRef(session:Session,refresh_token:str ):
    refToken=db.getTokenObjOfToken(session=session,tokenString=refresh_token)
    if refToken:
        print("REFERENCE",refToken.id)
        db.removeRefreshToken(session=session,refreshTokenId=refToken.id)

def removeSessionOfUser(session:Session,user:UUID):
    pass