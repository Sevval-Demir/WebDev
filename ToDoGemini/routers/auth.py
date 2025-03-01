from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.testing import db
from starlette import status

from database import SessionLocal
from models import User
from passlib.context import CryptContext
router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str

def authenticate_user(username:str,password:str):
    user=db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user



@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request:CreateUserRequest):
    user=User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        is_active=True,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(user)
    db.commit()