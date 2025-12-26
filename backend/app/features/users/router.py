from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_platform_admin
from .schemas import UserRead
from .service import UserService

router = APIRouter()
user_service = UserService()

@router.get("/users/me", response_model=UserRead)
def read_users_me(current_user: UserRead = Depends(get_current_user)):
    return current_user

@router.get("/platform/admin/users", response_model=List[UserRead])
def read_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: UserRead = Depends(get_current_platform_admin)
):
    """
    Get all users. Only for platform administrators.
    """
    return user_service.get_all_users(db, skip=skip, limit=limit)
