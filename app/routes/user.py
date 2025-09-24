from fastapi import APIRouter, HTTPException, Depends, status
from ..schemas import UserCreate, UserResponse, Token, TokenData, UserUpdate
from ..models import User
from ..database import get_db
from sqlalchemy.orm import Session
from ..core.security import hash_password, verify_password
from ..constants import  ROLES

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[UserResponse])
async def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    """Get all users"""
    print("🍀🍀🍀 User DB session:", db)
    print(f"🍀🍀🍀 User: {User}")
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
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

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Lấy các field được gửi lên
    update_data = user.model_dump(exclude_unset=True)

    # 1) Xử lý password (đừng set thuộc tính 'password' lên model)
    if "password" in update_data:
        db_user.hashed_pwd = hash_password(update_data["password"])
        update_data.pop("password")

    # 2) Xử lý email (check trùng trước rồi mới set)
    if "email" in update_data:
        value = update_data["email"]
        existing = db.query(User).filter(User.email == value, User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered by another user")
        db_user.email = value
        update_data.pop("email")

    # 3) Xử lý role (validate whitelist)
    if "role" in update_data:
        value = update_data["role"]
        if value not in ROLES:
            raise HTTPException(
                status_code=400,
                detail="Role must be one of: " + ", ".join(ROLES),
            )
        db_user.role = value
        update_data.pop("role")

    # 4) Set các field còn lại (name, is_active, ... nếu có)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return None