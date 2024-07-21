from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import SessionLocal
from models import UsersTable
from schemas import CreateUserSchema, TokenSchema
from utils import bcrypt_context, authenticate_user, create_access_token
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(db: db_dependency,create_user_schema: CreateUserSchema):
    try:
        create_user_model = UsersTable(
        username=create_user_schema.username,
        hashed_password=bcrypt_context.hash(create_user_schema.password),
        first_name=create_user_schema.first_name,
        last_name=create_user_schema.last_name,
        role=create_user_schema.role,
        phone_num=create_user_schema.phone_num
    )
        db.add(create_user_model)
        db.commit()
        return {"message":f"Successfuly registed {create_user_schema.first_name} {create_user_schema.last_name}"}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or phone_num  already exists")



@router.post('/token/', response_model=TokenSchema)
async def signin_by_access_token(db: db_dependency, data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user.username, user.id, user.first_name, user.last_name, timedelta(minutes=10))

    return {
        'access_token': token,
        'token_type': 'bearer'
    }
