from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from passlib.context import CryptContext
from typing import Generator, Optional
from pydantic import BaseModel
from sqlalchemy import Boolean, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import asynccontextmanager
from .routes import user

# Security Config 
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
TOKEN_EXPIRE = settings.access_token_expire_minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

engine = create_engine(settings.database_url_sqlite, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, nullable=False, default="user")
    hashed_pwd = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

# API Models
class UserCreate(BaseModel):
    name: str
    email: str
    role: str | None = "user"
    password: str

class UserRespone(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("🍀🍀🍀 Database connected and tables created.")
    yield
    engine.dispose()
    print("🍀🍀🍀 Database connection closed.")  


app = FastAPI(lifespan=lifespan, title="User Authentication with JWT", version="1.0.0")
app.include_router(user.router)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the User Authentication API with JWT!"}