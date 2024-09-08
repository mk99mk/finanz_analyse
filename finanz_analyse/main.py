from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from finanz_analyse.api.router import get_router

app = FastAPI()

app.include_router(get_router())

BUILD = Path(__file__).parent.parent / "finanz_analyse_skeleton/build"
app.mount("/", StaticFiles(directory=str(BUILD), html=True), name="static")