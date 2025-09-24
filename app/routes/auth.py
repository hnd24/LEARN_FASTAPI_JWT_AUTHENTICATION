from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import Annotated    
from ..schemas import UserLogin, Token, UserResponse, UserCreate
from ..models import User
from ..core.security import get_current_active_user, hash_password, verify_password, create_access_token
from ..core.config import settings
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: Annotated[UserLogin, Body()], db: Annotated[Session, Depends(get_db)]):
    """Register a new user"""
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED,)
async def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    """Create a new user"""
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        role=user.role or "user",
        hashed_pwd=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user