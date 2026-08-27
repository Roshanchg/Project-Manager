from fastapi import FastAPI,APIRouter
from app import config as config
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
app=FastAPI(
    title=config.PROJECT_NAME
)
app.mount("/static",
          StaticFiles(directory=config.STATIC_DIR))

templates=Jinja2Templates(directory=config.TEMPLATES_DIR)

