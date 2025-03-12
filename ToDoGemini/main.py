from fastapi import FastAPI,Depends,Path,HTTPException
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from starlette import status
from models import Base,ToDo
from database import engine,SessionLocal
from typing import Annotated
from routers.auth import router as auth_router
from routers.todo import router as todo_router
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm


app=FastAPI()

app.include_router(auth_router)
app.include_router(todo_router)

Base.metadata.create_all(bind=engine)