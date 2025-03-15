from fastapi import FastAPI,Depends,Path,HTTPException,Request
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse
from models import Base,ToDo
from database import engine,SessionLocal
from routers.auth import router as auth_router
from routers.todo import router as todo_router
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
import os

app=FastAPI(debug=True)

script_dir=os.path.dirname(__file__)
st_abs_file_path=os.path.join(script_dir,"static/")

app.mount("/static",StaticFiles(directory=st_abs_file_path),name="static")

@app.get("/")
def read_root(request: Request):
    return RedirectResponse(url="/todo/todo-page",status_code=status.HTTP_302_FOUND)


app.include_router(auth_router)
app.include_router(todo_router)

Base.metadata.create_all(bind=engine)