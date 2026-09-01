from fastapi import FastAPI,Depends,Query,APIRouter
from typing import Annotated
from sqlmodel import Session
import app.models.database as db
from app import config as config


router=APIRouter()