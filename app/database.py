from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator
from .config import settings

# Engine (SQLite cần check_same_thread=False)
engine = create_engine(
    settings.database_url_sqlite,
    connect_args={"check_same_thread": False} ,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Dependency cho FastAPI: mở/đóng session mỗi request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """Tạo bảng nếu chưa có."""
    from app import models  # đảm bảo models được import để metadata biết các bảng
    Base.metadata.create_all(bind=engine)

def dispose_engine() -> None:
    """Đóng connection pool khi app shutdown."""
    engine.dispose()
