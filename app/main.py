# app/main.py
from datetime import timedelta
from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models import User
from .core.config import settings
from .routes import user, auth
from .database import get_db, init_db, dispose_engine
from .schemas import UserResponse, Token as TokenSchema
from .core.security import create_access_token, get_current_active_user, verify_password

# Security Config (nếu cần dùng ở đây)
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
TOKEN_EXPIRE = settings.access_token_expire_minutes

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("🍀🍀🍀 Database connected and tables created.")
    yield
    dispose_engine()
    print("🍀🍀🍀 Database connection closed.")

app = FastAPI(lifespan=lifespan, title="User Authentication with JWT", version="1.0.0")
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the User Authentication API with JWT!"}

# current_user là User (ORM). Response model là UserResponse (Pydantic)
@app.get("/profile", response_model=UserResponse, tags=["Profile"])
async def profile(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@app.get("/verify-token", tags=["Auth"])
async def verify_token(current_user: Annotated[User, Depends(get_current_active_user)]):
    return {"valid": True, "user": UserResponse.model_validate(current_user)}

# Trả về schema Token chuẩn
@app.post("/token", response_model=TokenSchema, tags=["Auth"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Authenticate user and return a JWT access token.
    OAuth2PasswordRequestForm dùng field 'username' (không phải 'email').
    """
    # Lưu ý: OAuth2PasswordRequestForm -> username, password
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.email)},  # hoặc user.email nếu bạn muốn
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
