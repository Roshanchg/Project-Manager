from pathlib import Path
from dotenv import load_dotenv
import os
rootdir=Path(__file__).parent.parent.resolve()
appdir=Path(__file__).parent.resolve()
load_dotenv(dotenv_path=rootdir.joinpath(".env"))

PROJECT_NAME="Project Manager"
STATIC_DIR="app/static"
TEMPLATES_DIR="app/templates"

DB_ENGINE_NAME=os.getenv("DB_ENGINE_NAME")
if DB_ENGINE_NAME=="sqlite":
    DB_FILE_NAME=os.getenv("DB_FILE_NAME")
else:
    DB_HOST=os.getenv("DB_HOST")
    DB_PORT=os.getenv("DB_PORT")
    DB_NAME=os.getenv("DB_NAME")
    DB_USERNAME=os.getenv("DB_USERNAME")
    DB_PASSWORD=os.getenv("DB_PASSWORD")