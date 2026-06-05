from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from app.database import engine
from app.models.models import Base
from app.routers import auth, ingredientes, recetas
from dotenv import load_dotenv

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Generador de Recetas", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(ingredientes.router)
app.include_router(recetas.router)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})