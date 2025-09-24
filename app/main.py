from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Generator, Optional
from pydantic import BaseModel
from sqlalchemy import Boolean, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import asynccontextmanager
from .config import settings
from .routes import user
from .database import init_db, dispose_engine
from .routes import user as user_routes


# Security Config 
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

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the User Authentication API with JWT!"}