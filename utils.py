# crud/mechanic
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException
import jwt
from jose import JWTError
from passlib.context import CryptContext
from config import ALGORITHM, SECRET_KEY
from database import SessionLocal
from models import UsersTable
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import status

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# security
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_access_token(username: str, user_id: int, first_name: str, last_name: str, expires_delta: timedelta):
    encode = {
        "sub": username,
        "id": user_id,
        "first_name": first_name,
        "last_name": last_name
    }
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(db: Session, username: str, password: str):
    db_user = db.query(UsersTable).filter(UsersTable.username == username).first()
    if not db_user or not bcrypt_context.verify(password, db_user.hashed_password):
        return False
    return db_user

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user."
            )
        db_user = db.query(UsersTable).filter(UsersTable.id == user_id).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user."
            )
        return {
            "id": db_user.id,
            "username": db_user.username,
            "first_name": db_user.first_name,
            "last_name": db_user.last_name,
            "role": db_user.role
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user"
        )

# end